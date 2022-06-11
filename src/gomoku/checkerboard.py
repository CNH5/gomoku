from collections import namedtuple
from copy import deepcopy

import numpy as np

from src.ai.zobrist import zobrist
from src.gomoku import direction, Point, NONE_MARK, BLOCK_MARK, X_MARK, get_point, \
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
                self.forbidden_point = forbidden_points
            self.checkerboard = checkerboard
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

        def update(self, change_point: Point, new_piece: int):
            """
            更新禁手点和连珠,在更新棋子前调用
            """
            old_cb = deepcopy(self.checkerboard)
            old_piece = self.checkerboard.get_piece(point=change_point)
            if new_piece == self.checkerboard.none_piece():  # 模拟
                self.checkerboard.remove_piece(change_point, simulation=True)
                if check_forbidden(self.checkerboard, change_point, backup=False)[0]:
                    # 移除棋子,并且棋子所在的地方原来就是禁手点
                    self.forbidden_point = self.forbidden_point | {change_point}
            else:
                # 放置在禁手点上，禁手点取消
                self.forbidden_point = self.forbidden_point - {change_point}
                self.checkerboard.place(change_point, new_piece, simulation=True)

            # self.forbidden_point = set(
            #     p for p in self.forbidden_point if check_forbidden(self.checkerboard, p, backup=False)[0]
            # )
            # 有必要考虑极端情况吗?放在一条线上就能直接更新了

            # 放置或移除棋子之后修改的点
            updated_points = self.__update_forbidden_point(self.checkerboard, change_point)  # 关联点及禁手点

            for cp in updated_points:
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
            shape = new_cb.shape()
            update_points = [point]
            for dx, dy in direction:
                k = 0
                for i in range(1, max(shape[0], shape[1])):
                    p = Point(point.X + i * dx, point.Y + i * dy)
                    if not new_cb.in_area(point=p) or k >= 2:
                        break
                    if new_cb.get_piece(point=p) == new_cb.none_piece():
                        if check_forbidden(new_cb, p, backup=False)[0]:
                            s = self.forbidden_point | {p}
                            if len(s) > len(self.forbidden_point):  # 新增禁手点
                                self.forbidden_point = s
                                update_points += self.__update_forbidden_point(new_cb, p, False)
                        else:
                            s = self.forbidden_point - {p}
                            if len(s) < len(self.forbidden_point):  # 禁手点减少
                                self.forbidden_point = s
                                update_points += self.__update_forbidden_point(new_cb, p, False)
                        k += 1
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

        def recalibration(self):
            """
            重新获取连珠
            """
            black, white = get_all_renju(self.checkerboard)
            self.renju_black = black
            self.renju_white = white

        def reset(self):
            self.forbidden_point = set()
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
        return self._attribute.forbidden_point

    def renju_black(self) -> dict[str, list]:
        return self._attribute.renju_black

    def renju_white(self) -> dict[str, list]:
        return self._attribute.renju_white

    def recalibration(self):
        self._attribute.recalibration()

    @staticmethod
    def none_piece():
        return 0

    def shape(self):
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
        return self._piece_num

    def can_place(self, point: Point):
        """
        判断这个位置是否能落子
        :return: 能落子返回True，不能落子返回False
        """
        return self.in_area(point=point) and self._board[point.X][point.Y] == self._none_piece

    def place(self, point: Point, piece: int, simulation=False):
        """
        放置棋子
        """
        if self.can_place(point):
            if not simulation:
                self._attribute.update(point, piece)
                zobrist.go(point, not game.is_black_now(self))
            self._piece_num += 1
            self._board[point.X][point.Y] = piece
        else:
            raise ValueError("棋子放置失败-_-!")

    def remove_piece(self, point: Point, simulation=False):
        """
        移除该点上的棋子
        """
        if not self.can_place(point):
            if not simulation:
                self._attribute.update(point, self._none_piece)
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

    def get_edge_points(self) -> [Point]:
        """
        获取边界点
        """
        points = []
        for i in range(self._board.shape[0]):
            for j in range(self._board.shape[1]):
                p = Point(i, j)
                if self.get_piece(point=p) != self._none_piece:
                    continue
                for dx in range(-2, 3):  # 5x5
                    x = i + dx
                    if 0 <= x < self._board.shape[0]:
                        for dy in range(-2, 3):
                            y = j + dy
                            if 0 <= y < self._board.shape[1] and self.get_piece(x=x, y=y) != self._none_piece:
                                points.append(p)
                                break
        return points

    def point_shape(self, point: Point, x_piece: int, consider_forbidden=False):
        """
        获取point处的棋子形状
        :param point: 要获取形状的坐标
        :param x_piece: 目标棋子
        :param consider_forbidden 是否考虑禁手
        """
        shapes = []
        for dx, dy in direction:
            shape = ""
            n = 0  # 统计连续出现的空位的数量
            for k in range(1, max(self._board.shape[0], self._board.shape[1])):
                if n >= 4:  # 连续出现4个空位，没有必要继续往下了
                    break
                p = Point(point.X + dx * k, point.Y + dy * k)
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
                if self._attribute.forbidden_point.__contains__(Point(i, j)) and consider_forbidden:
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
                if self._attribute.forbidden_point.__contains__(Point(i, j)) and consider_forbidden:
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

                if self._attribute.forbidden_point.__contains__(p1) and consider_forbidden:
                    shape1 += BLOCK_MARK
                else:
                    shape1 += self.get_mark(piece, point=p1)
                if self.get_piece(point=p1) == self._none_piece:
                    if e1 == 0:
                        s1 = d + 1
                else:
                    e1 = d + 1

                if self._attribute.forbidden_point.__contains__(p2) and consider_forbidden:
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

                if self._attribute.forbidden_point.__contains__(p1) and consider_forbidden:
                    shape1 += BLOCK_MARK
                else:
                    shape1 += self.get_mark(piece, point=p1)
                if self.get_piece(point=p1) == self._none_piece:
                    if e1 == 0:
                        s1 = d + 1
                else:
                    e1 = d + 1

                if self._attribute.forbidden_point.__contains__(p2) and consider_forbidden:
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

    def have_piece(self, point):
        return self.get_piece(point=point) != self.none_piece()

    def __str__(self):
        return f"checkerboard:\n{self._board}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        # 直接把整个棋盘的值弄成字符串...
        return hash(zobrist.code)
