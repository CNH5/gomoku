import json
from typing import Union

from src.ai import ai_chessman
from src.ai.zobrist import zobrist
from src import config as CONFIG
from src.gomoku import Point, get_point
from src.gomoku.checkerboard import Checkerboard
from src.gomoku.chessman import BLACK_CHESSMAN, WHITE_CHESSMAN, Chessman
from src.gomoku.renju.util import get_renju_5, check_forbidden

row, col = CONFIG.row_points, CONFIG.col_points  # 行数和列数
forbidden_moves = CONFIG.forbidden_moves  # 是否启用禁手
infinity_repentance = CONFIG.infinity_repentance  # 是否无限悔棋
checkerboard = Checkerboard(row, col, forbidden_moves)  # 棋盘
start = False  # 游戏是否已经开始
forbidden_win = False  # 因为禁手获胜
winner: Union[Chessman, None] = None  # 获胜者
win_points = []  # 导致获胜的点


def load_data():
    """
    加载上次的记录
    """
    global start, row, col, forbidden_moves, forbidden_win, win_points, winner, checkerboard, infinity_repentance
    with open(CONFIG.LAST_GAME_PATH) as f:
        last_data = json.load(f)
        if start := last_data["start"]:
            row = last_data["row"]
            col = last_data["col"]
            forbidden_moves = last_data["forbidden_moves"]

            checkerboard = Checkerboard(
                row, col, forbidden_moves,
                set(Point(p["X"], p["Y"]) for p in last_data["forbidden_points"])
            )
            forbidden_win = last_data["forbidden_win"]
            infinity_repentance = last_data["infinity_repentance"]

            if last_data["winner"] == "black":
                winner = BLACK_CHESSMAN
            elif last_data["winner"] == "white":
                winner = WHITE_CHESSMAN

            black_records, white_records, win_points = [], [], []
            for p in last_data["black_records"]:
                point = Point(p["X"], p["Y"])
                checkerboard.place(point, BLACK_CHESSMAN.piece(), simulation=True)
                black_records.append(point)

            for p in last_data["white_records"]:
                point = Point(p["X"], p["Y"])
                checkerboard.place(point, WHITE_CHESSMAN.piece(), simulation=True)
                white_records.append(point)

            win_points = [Point(p["X"], p["Y"]) for p in last_data["win_points"]]

            BLACK_CHESSMAN.reset(last_data["black_repentance_times"], black_records)
            WHITE_CHESSMAN.reset(last_data["white_repentance_times"], white_records)

            checkerboard.recalibration()  # 重新校准连珠
            zobrist.reset(row, col)


def save():
    if BLACK_CHESSMAN.__eq__(winner):
        w = "black"
    elif WHITE_CHESSMAN.__eq__(winner):
        w = "white"
    else:
        w = None

    with open(CONFIG.LAST_GAME_PATH, "w") as f:
        json.dump({
            "start": start,
            "winner": w,
            "forbidden_win": forbidden_win,
            "win_points": [{
                "X": p.X,
                "Y": p.Y
            } for p in win_points],

            "row": row,
            "col": col,
            "forbidden_moves": forbidden_moves,
            "infinity_repentance": infinity_repentance,

            "black_repentance_times": BLACK_CHESSMAN.repentance_times,
            "black_records": [{
                "X": p.X,
                "Y": p.Y
            } for p in BLACK_CHESSMAN.records()],

            "white_repentance_times": WHITE_CHESSMAN.repentance_times,
            "white_records": [{
                "X": p.X,
                "Y": p.Y
            } for p in WHITE_CHESSMAN.records()],
            "forbidden_points": [{
                "X": p.X,
                "Y": p.Y
            } for p in checkerboard.forbidden_points()]
        }, f)


def is_player_now():
    """
    判断当前应不应当是玩家操作
    """
    return ((not CONFIG.ai_enabled or CONFIG.ai_is_black ^ is_black_now()) and not ai_chessman.thinking) or \
           (winner is not None and winner.can_repentance())


def reset():
    """
    重置游戏
    """
    global row, col, winner, forbidden_moves, start, forbidden_win, win_points, infinity_repentance
    row, col = CONFIG.row_points, CONFIG.col_points
    forbidden_moves = CONFIG.forbidden_moves
    infinity_repentance = CONFIG.infinity_repentance
    winner = None
    start = forbidden_win = False
    win_points = []
    BLACK_CHESSMAN.reset(CONFIG.repentance_times)
    WHITE_CHESSMAN.reset(CONFIG.repentance_times)
    checkerboard.reset(row, col)
    zobrist.reset(row, col)


def is_black_now(cb=None):
    """
    判断当前是不是先手方要下子
    棋子数量为偶数是黑方
    棋子数量为奇数是白方
    """
    jud_cb = checkerboard if cb is None else cb
    return jud_cb.piece_count() % 2 == 0


def get_piece(is_black):
    """
    获取棋手的棋子
    """
    return BLACK_CHESSMAN.piece() if is_black else WHITE_CHESSMAN.piece()


def now_chessman(cb=None) -> Chessman:
    """
    获取当前应该落子的棋手
    """
    return BLACK_CHESSMAN if is_black_now(cb) else WHITE_CHESSMAN


def last_chessman(cb=None):
    return WHITE_CHESSMAN if is_black_now(cb) else BLACK_CHESSMAN


def can_place(point: Point) -> bool:
    """
    判断是否能够落子
    """
    return checkerboard.can_place(point) and winner is None and not is_draw()


def place(point: Point, chessman: Chessman):
    """
    放置棋子
    :param point: 放置的点
    :param chessman: 要落子的棋手
    """
    if checkerboard.can_place(point) and now_chessman().__eq__(chessman):
        checkerboard.place(point, chessman.piece())
        chessman.add_record(point)
        global start
        if not start:
            start = True
        check_win(point)  # 检查是否能获胜
    else:
        print(checkerboard)
        raise ValueError("放置失败！ " + str(point))


def repentance(chessman: Chessman):
    """
    执行悔棋操作
    应当是轮到谁操作谁能够悔棋,并且平局之后不能再悔棋
    :param
        chessman: 要悔棋的棋手
    """
    if chessman.can_repentance() and not is_draw():
        # 消耗一次悔棋次数
        chessman.use_repentance()
        global winner, forbidden_win, win_points
        if winner is not None:
            # 如果已经获胜，那就撤销胜利
            winner = None
            win_points = []
            forbidden_win = False
            # 已经获胜那就是获胜方有操作权，移除对应棋子
            if is_black_now():
                checkerboard.remove_piece(WHITE_CHESSMAN.pop_record())
            else:
                checkerboard.remove_piece(BLACK_CHESSMAN.pop_record())
        else:
            # 两边都移除一个记录
            checkerboard.remove_piece(BLACK_CHESSMAN.pop_record())
            checkerboard.remove_piece(WHITE_CHESSMAN.pop_record())

        if is_black_now() and WHITE_CHESSMAN.len_records() > 0:
            return WHITE_CHESSMAN.last_point()
        elif not is_black_now():
            return BLACK_CHESSMAN.last_point()
    return None


def check_win(last_point: Point = None):
    """
    根据上一次落子的位置，判断是否胜利
    :return:
        is_: 是否因为禁手获胜
        [Point]: 导致胜利的点
    """
    chessman = last_chessman()
    if chessman.len_records() == 0:
        return
    elif last_point is not None:
        last_point = chessman.last_point()
    piece_is_black = checkerboard.get_piece(point=last_point) == BLACK_CHESSMAN.piece()
    # 获取连珠
    renju_5, rot = get_renju_5(checkerboard, last_point, chessman.piece())

    # 判胜
    global winner, win_points, forbidden_win
    if len(renju_5) > 0:
        # 存在5连，直接判断落子方获胜
        winner = BLACK_CHESSMAN if piece_is_black else WHITE_CHESSMAN
        for point, i in renju_5:
            win_points += [get_point(point, i, k) for k in range(1, 6)]

    if len(rot) > 0:
        # 长连
        if not (piece_is_black and forbidden_moves and len(renju_5) > 0):
            for point, i, length in rot:
                win_points += [get_point(point, i, k) for k in range(1, length - 1)]

        if piece_is_black and forbidden_moves and len(renju_5) == 0:
            # 长连禁手，无五连，白方获胜
            forbidden_win = True
            winner = WHITE_CHESSMAN
        else:
            winner = BLACK_CHESSMAN if piece_is_black else WHITE_CHESSMAN

    elif piece_is_black and forbidden_moves:
        # 没有五连和长连，判断是不是禁手点
        forbidden_win, reason = check_forbidden(
            checkerboard=checkerboard,
            point=last_point,
            get_reason=True,
            place_piece=False,
        )
        if forbidden_win:
            winner, win_points = WHITE_CHESSMAN, reason


def is_draw() -> bool:
    """
    判断是否平局,也就是棋盘满没满
    """
    is_full = row * col <= checkerboard.piece_count()
    return is_full


load_data()  # 初始化
