from collections import namedtuple
from copy import deepcopy

import numpy as np

from src.ai.zobrist import zobrist
from src.gomoku import Point, NONE_MARK, BLOCK_MARK, X_MARK, get_point, \
    LOWER_RIGHT, RIGHT, LOWER, game, UPPER_RIGHT
from src.gomoku.renju.util import check_forbidden, get_f_renju, get_renju, get_all_renju
from src.gomoku.chessman import BLACK_CHESSMAN, WHITE_CHESSMAN

LineShape = namedtuple("LineShape", ["start_point", "shape"])


class Checkerboard:
    def __init__(self, row, col, forbidden_moves: bool, forbidden_points=None):
        """
        棋盘类
        :param row: 行数
        :param col: 列数
        :raise ValueError 当行和列都小于5时，肯定会平局，所以行和列必须大于等于5
        """
        if row < 5 and col < 5:
            raise ValueError("棋盘大小不能小于5x5!")
        self._board = np.zeros((row, col), dtype=int)  # 棋盘
        self._none_piece = 0
        self._piece_num = 0
        self.forbidden_moves = forbidden_moves
        self._attribute = self._Attribute(self, forbidden_points)

    class _Attribute:
        """
        棋盘中的属性
        """

        def __init__(self, checkerboard, forbidden_points=None):
            if forbidden_points is None:
                self.forbidden_point = set()
            else:
                self.forbidden_point = forbidden_points  # 禁手点
            self.checkerboard = checkerboard  # 绑定的棋盘
            self.edge_points = set()  # 边界点
            self.renju_black = {  # 黑方连珠
                "sleep2": [],
                "live2": [],
                "sleep3": [],
                "live3": [],
                "renju4": [],
            }
            self.renju_white = {  # 白方连珠
                "sleep2": [],
                "live2": [],
                "sleep3": [],
                "live3": [],
                "renju4": [],
            }

        def update(self, change_point: Point, new_piece: int, update_edge=True):
            """
            更新禁手点和连珠,在更新棋子前调用
            """
            old_cb = deepcopy(self.checkerboard)
            old_piece = self.checkerboard.get_piece(point=change_point)  # 原来的棋子

            if new_piece == self.checkerboard.none_piece():  # 模拟
                self.checkerboard.remove_piece(change_point, simulation=True)
                if check_forbidden(self.checkerboard, change_point, backup=False)[0]:
                    # 移除棋子,并且棋子所在的地方原来就是禁手点
                    self.forbidden_point = self.forbidden_point | {change_point}
            else:
                # 放置在禁手点上，禁手点取消
                self.forbidden_point = self.forbidden_point - {change_point}
                self.checkerboard.place(change_point, new_piece, simulation=True)
            # 貌似没有必要考虑极端情况
            # self.forbidden_point = set(
            #     p for p in self.forbidden_point if check_forbidden(self.checkerboard, p, backup=False)[0]
            # )
            # 更新边界点
            if update_edge:
                self.__update_edge_points(change_point, new_piece)
            # 放置或移除棋子之后修改的点
            updated_points = self.__update_forbidden_point(self.checkerboard, change_point)  # 关联点及禁手点

            for cp in updated_points:  # 根据关联更新的点更新周围连珠
                self.__update_renju(old_cb, self.checkerboard, cp)

            if new_piece == self.checkerboard.none_piece():  # 还原
                self.checkerboard.place(change_point, old_piece, simulation=True)
            else:
                self.checkerboard.remove_piece(change_point, simulation=True)

        def __update_forbidden_point(self, new_cb, point, back_up=True):
            """
            更新点周围的禁手点
            还有bug，禁手点再套上禁手有可能导致误判
            """
            if back_up:
                new_cb = deepcopy(new_cb)
            update_points = [point]
            for i in range(8):  # 8个方向
                k = 0
                for d in range(1, max(new_cb.shape())):
                    p = get_point(point, i, d)
                    if not new_cb.in_area(point=p) or k >= 2:
                        break
                    if new_cb.get_piece(point=p) == new_cb.none_piece():  # 只考虑周围的空点
                        forbidden = check_forbidden(new_cb, p, backup=False)[0]  # 这个点是不是禁手点
                        contain = self.forbidden_point.__contains__(p)  # 这个点是否在原来的禁手点中

                        if forbidden and not contain:  # 新增禁手点
                            self.forbidden_point = self.forbidden_point | {p}
                            update_points += self.__update_forbidden_point(new_cb, p, False)

                        elif not forbidden and contain:  # 禁手点被解除
                            self.forbidden_point = self.forbidden_point - {p}
                            update_points += self.__update_forbidden_point(new_cb, p, False)
                        k += 1
                    else:
                        k = 0
            return update_points

        def __update_renju(self, old_cb, new_cb, point):
            """
            更新点周围的连珠
            """
            if self.checkerboard.forbidden_moves:
                black_add, black_loss = get_f_renju(old_cb, new_cb, point)
            else:
                black_add, black_loss = get_renju(old_cb, new_cb, point, BLACK_CHESSMAN.piece())
            white_add, white_loss = get_renju(old_cb, new_cb, point, WHITE_CHESSMAN.piece())
            for key in self.renju_white.keys():
                self.renju_white[key] = list((set(self.renju_white[key]) - white_loss[key]) | white_add[key])
                self.renju_black[key] = list((set(self.renju_black[key]) - black_loss[key]) | black_add[key])

        def __update_edge_points(self, change_point: Point, new_piece: int):
            """
            更新边界点
            """
            # 棋盘的形状
            shape = self.checkerboard.shape()
            # 新棋子是否为空棋子,若为空则代表移除棋子，否则代表放置棋子
            if not (piece_is_none := new_piece == Checkerboard.none_piece()):
                # 放置棋子，移除放置的点
                self.edge_points = self.edge_points - {change_point}

            for dx in range(-2, 3):  # 5x5
                if 0 <= (x := change_point.X + dx) < shape[0]:  # 偏移的x值在棋盘上
                    for dy in range(-2, 3):
                        if 0 <= (y := change_point.Y + dy) < shape[1]:  # 偏移的y值在棋盘上
                            if self.checkerboard.get_piece(x=x, y=y) == Checkerboard.none_piece():  # 偏移位置不为空
                                if not piece_is_none:
                                    # 放置棋子，边界点只可能增加
                                    self.edge_points = self.edge_points | {Point(x, y)}
                                elif not self.checkerboard.has_neighbor(x=x, y=y):
                                    # 移除棋子，边界点只可能减少
                                    self.edge_points = self.edge_points - {Point(x, y)}

        def __reset_edge_points(self):
            """
            重新校准边界点
            """
            self.edge_points = set()
            shape = self.checkerboard.shape()  # 重置边界点
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if self.checkerboard.get_piece(x=i, y=j) != Checkerboard.none_piece():
                        continue
                    if self.checkerboard.has_neighbor(x=i, y=j):
                        self.edge_points = self.edge_points | {Point(i, j)}

        def recalibration(self):
            """
            重新校准属性
            """
            self.renju_black, self.renju_white = get_all_renju(self.checkerboard)
            self.__reset_edge_points()

        def reset(self):
            """
            重置属性
            """
            self.forbidden_point = set()
            self.edge_points = set()
            self.renju_black = {
                "sleep2": [],
                "live2": [],
                "sleep3": [],
                "live3": [],
                "renju4": [],
            }
            self.renju_white = {
                "sleep2": [],
                "live2": [],
                "sleep3": [],
                "live3": [],
                "renju4": [],
            }

    def forbidden_points(self) -> set[Point]:
        """
        获取棋盘上的禁手点
        """
        return self._attribute.forbidden_point

    def renju_black(self) -> dict[str, list]:
        """
        获取黑方的连珠
        """
        return self._attribute.renju_black

    def renju_white(self) -> dict[str, list]:
        """
        获取白方的连珠
        """
        return self._attribute.renju_white

    def edge_points(self) -> [Point]:
        """
        获取边界点
        """
        return self._attribute.edge_points

    def recalibration(self):
        """
        重新校准连珠
        """
        self._attribute.recalibration()

    @staticmethod
    def none_piece():
        return 0

    def shape(self):
        """
        获取棋盘的大小
        """
        return self._board.shape

    def reset(self, row, col):
        """
        重置棋盘
        """
        self._board = np.zeros((row, col))
        self._piece_num = 0
        self._attribute.reset()

    def in_area(self, **args):
        """
        判断这个点是不是在棋盘上
        """

        def f(x, y):
            return self._board.shape[0] > x >= 0 and self._board.shape[1] > y >= 0

        if len(args) == 1:
            return f(args["point"].X, args["point"].Y)
        elif len(args) == 2:
            return f(args["x"], args["y"])
        else:
            return False

    def piece_count(self):
        """
        获取棋盘上棋子的数量
        """
        return self._piece_num

    def can_place(self, point: Point):
        """
        判断这个位置是否能落子
        :return: 能落子返回True，不能落子返回False
        """
        return self.in_area(point=point) and self.get_piece(point=point) == self._none_piece

    def place(self, point: Point, piece: int, simulation=False, update_edge=True):
        """
        放置棋子
        """
        if self.can_place(point):
            if not simulation:
                self._attribute.update(point, piece, update_edge=update_edge)
                zobrist.go(point, not game.is_black_now(self))
            self._piece_num += 1
            self._board[point.X][point.Y] = piece
        else:
            raise ValueError("棋子放置失败-_-!")

    def remove_piece(self, point: Point, simulation=False, update_edge=True):
        """
        移除该点上的棋子
        """
        if not self.can_place(point):
            if not simulation:
                self._attribute.update(point, self._none_piece,update_edge=update_edge)
                zobrist.go(point, game.is_black_now(self))  # 没必要在不必须的地方更新这个
            self._piece_num -= 1
            self._board[point.X, point.Y] = self._none_piece

    def get_piece(self, **args) -> int:
        """
        获取point上的棋子
        args = {"point": Point} 或 args = {"x": int, "y": int}
        """
        if len(args) == 1:
            return self._board[args["point"].X, args["point"].Y]
        elif len(args) == 2:
            return self._board[args["x"], args["y"]]
        else:
            return self.none_piece()

    def point_shape(self, point: Point, x_piece: int, consider_forbidden=False):
        """
        获取point处的棋子形状
        :param point: 要获取形状的坐标
        :param x_piece: 目标棋子
        :param consider_forbidden 是否考虑禁手
        """
        shapes = []
        for i in range(8):
            shape = ""
            n = 0  # 统计连续出现的空位的数量
            for k in range(1, max(self._board.shape)):
                if n >= 4:  # 连续出现4个空位，没有必要继续往下了
                    break
                p = get_point(point, i, k)
                if self.in_area(point=p):
                    piece = self.get_piece(point=p)
                    if piece == self._none_piece:
                        if consider_forbidden and self._attribute.forbidden_point.__contains__(p):
                            shape = BLOCK_MARK + shape
                            break
                        else:
                            shape = NONE_MARK + shape
                            n += 1
                        continue
                    else:
                        n = 0
                    if piece == x_piece:
                        shape = X_MARK + shape
                    else:
                        shape = BLOCK_MARK + shape
                        break
                else:
                    shape = BLOCK_MARK + shape
                    break
            shapes.append(shape)
        return shapes

    def get_all_lines_shape(self, piece, consider_forbidden):
        """
        获取棋盘上所有阴线和阳线的形状
        :param piece: 目标棋子的值
        :param consider_forbidden 是否考虑禁手点
        """
        shapes = {
            "right": [],  # 左到右
            "lower": [],  # 上到下
            "lower_right": [],  # 左上到右下
            "upper_right": [],  # 右上到左下
        }
        # 横向阳线
        for i in range(self._board.shape[0]):
            shape = BLOCK_MARK
            s, e = 0, 0  # 这个方向上第一个棋子和最后一个棋子的下标
            for j in range(self._board.shape[1]):
                if consider_forbidden and self._attribute.forbidden_point.__contains__(Point(i, j)):
                    shape += BLOCK_MARK
                else:
                    shape += self.get_mark(piece, x=i, y=j)
                if self.get_piece(x=i, y=j) == self._none_piece:
                    if e == 0:
                        s = j + 1
                else:
                    e = j
            s, e = max(0, s - 3), e + 5
            shape += BLOCK_MARK
            shapes["right"].append(LineShape(get_point(Point(i, 0), RIGHT, s), shape[s: e]))
        # 纵向阳线
        for j in range(self._board.shape[1]):
            shape = BLOCK_MARK
            s, e = 0, 0  # 这个方向上第一个棋子和最后一个棋子的下标
            for i in range(self._board.shape[1]):
                if consider_forbidden and self._attribute.forbidden_point.__contains__(Point(i, j)):
                    shape += BLOCK_MARK
                else:
                    shape += self.get_mark(piece, x=i, y=j)
                if self.get_piece(x=i, y=j) == self._none_piece:
                    if e == 0:
                        s = i + 1
                else:
                    e = i
            s, e = max(0, s - 3), e + 5
            shape += BLOCK_MARK
            shapes["lower"].append(LineShape(get_point(Point(0, j), LOWER, s), shape[s: e]))
        # 按照纵轴获取形状
        for i in range(self._board.shape[0] - 6):  # 太短的阴线没有意义
            p1_0, p2_0 = Point(i, 0), Point(self._board.shape[0] - i - 1, 0)  # 初始点
            shape1, shape2 = BLOCK_MARK, BLOCK_MARK
            s1, e1, s2, e2 = 0, 0, 0, 0

            for d in range(min(self._board.shape[0] - i, self._board.shape[1] - 1)):
                p1, p2 = get_point(p1_0, LOWER_RIGHT, d), get_point(p2_0, UPPER_RIGHT, d)

                if consider_forbidden and self._attribute.forbidden_point.__contains__(p1):
                    shape1 += BLOCK_MARK
                else:
                    shape1 += self.get_mark(piece, point=p1)
                if self.get_piece(point=p1) == self._none_piece:
                    if e1 == 0:
                        s1 = d + 1
                else:
                    e1 = d + 1

                if consider_forbidden and self._attribute.forbidden_point.__contains__(p2):
                    shape2 += BLOCK_MARK
                else:
                    shape2 += self.get_mark(piece, point=p2)
                if self.get_piece(point=p2) == self._none_piece:
                    if e2 == 0:
                        s2 = d + 1
                else:
                    e2 = d + 1
            s1, e1 = max(0, s1 - 3), e1 + 5
            s2, e2 = max(0, s2 - 3), e2 + 5
            shape1, shape2 = shape1 + BLOCK_MARK, shape2 + BLOCK_MARK
            shapes["lower_right"].append(LineShape(get_point(p1_0, LOWER_RIGHT, s1), shape1[s1:e1]))
            shapes["upper_right"].append(LineShape(get_point(p2_0, UPPER_RIGHT, s2), shape2[s2:e2]))
        # 按照横轴获取形状
        for j in range(1, self._board.shape[1] - 6):
            p1_0, p2_0 = Point(0, j), Point(self._board.shape[0] - 1, j)  # 初始点
            shape1, shape2 = BLOCK_MARK, BLOCK_MARK
            s1, e1, s2, e2 = 0, 0, 0, 0

            for d in range(min(self._board.shape[1] - j, self._board.shape[0] - 1)):
                p1, p2 = get_point(p1_0, LOWER_RIGHT, d), get_point(p2_0, UPPER_RIGHT, d)

                if consider_forbidden and self._attribute.forbidden_point.__contains__(p1):
                    shape1 += BLOCK_MARK
                else:
                    shape1 += self.get_mark(piece, point=p1)
                if self.get_piece(point=p1) == self._none_piece:
                    if e1 == 0:
                        s1 = d + 1
                else:
                    e1 = d + 1

                if consider_forbidden and self._attribute.forbidden_point.__contains__(p2):
                    shape2 += BLOCK_MARK
                else:
                    shape2 += self.get_mark(piece, point=p2)
                if self.get_piece(point=p2) == self._none_piece:
                    if e2 == 0:
                        s2 = d + 1
                else:
                    e2 = d + 1
            s1, e1 = max(0, s1 - 3), e1 + 5  # 左闭右开...4-1 和 4+1
            s2, e2 = max(0, s2 - 3), e2 + 5
            shape1, shape2 = shape1 + BLOCK_MARK, shape2 + BLOCK_MARK
            shapes["lower_right"].append(LineShape(get_point(p1_0, LOWER_RIGHT, s1), shape1[s1:e1]))
            shapes["upper_right"].append(LineShape(get_point(p2_0, UPPER_RIGHT, s2), shape2[s2:e2]))
        return shapes

    def get_mark(self, x_piece: int, **args):
        """
        获取点对应棋子的标志
        args = {"point": Point} 或 args = {"x": int, "y": int}
        """
        if len(args) == 1:
            piece = self.get_piece(point=args["point"])
        elif len(args) == 2:
            piece = self.get_piece(x=args["x"], y=args["y"])
        else:
            piece = self._none_piece
        if piece == x_piece:
            return X_MARK
        elif piece == self._none_piece:
            return NONE_MARK
        else:
            return BLOCK_MARK

    def has_neighbor(self, **args):
        """
        判断点周围是否有棋子
        """
        if len(args) == 1:
            x, y = args["point"].X, args["point"].Y
        elif len(args) == 2:
            x, y = args["x"], args["y"]
        else:
            return False

        for dx in range(-2, 3):  # 点周围5x5的区域
            if 0 <= (x1 := x + dx) < self._board.shape[0]:  # 偏移的x值是否在棋盘上
                for dy in range(-2, 3):
                    if 0 <= (y1 := y + dy) < self._board.shape[1]:
                        if self.get_piece(x=x1, y=y1) != Checkerboard.none_piece():
                            return True
        return False

    def have_piece(self, point):
        return self.get_piece(point=point) != self.none_piece()

    def __hash__(self):
        # zobrist和棋形相对应，可以用这个代替哈希值
        return hash(zobrist.code)
