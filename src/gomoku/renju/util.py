from collections import namedtuple
from copy import deepcopy

from src.gomoku import Point, X_MARK, NONE_MARK, get_point, RIGHT, LOWER_RIGHT, LOWER, game, BLOCK_MARK, UPPER_RIGHT
from src.gomoku.renju.types import renju_live_3, renju4, f_renju_live3, f_renju4, renju5, renju5_, f_renju_sleep_3, \
    f_renju_sleep2, f_renju_live2, renju_live_2, renju_sleep_2, renju_sleep_3

Location = namedtuple('Location', ['point', "i", "renju"])
Location_5 = namedtuple('Location_5', ['point', 'i'])
Location_5_ = namedtuple("Location_5_", ["point", "i", "length"])

key_i = (("right", RIGHT), ("lower", LOWER), ("lower_right", LOWER_RIGHT), ("upper_right", UPPER_RIGHT))
key_r = (
    ("live3", renju_live_3), ("renju4", renju4), ("live2", renju_live_2),
    ("sleep2", renju_sleep_2), ("sleep3", renju_sleep_3)
)
f_key_r = (
    ("live3", f_renju_live3), ("renju4", f_renju4), ("live2", f_renju_live2),
    ("sleep2", f_renju_sleep2), ("sleep3", f_renju_sleep_3)
)


def get_renju_5(checkerboard, point: Point, x_piece: int):
    """
    获取五连以及长连
    """
    shapes, mark = checkerboard.point_shape(point, x_piece), checkerboard.get_mark(x_piece, point=point)
    renju_5, rot = [], []
    for i in range(4):
        i_ = i + 4
        line_shape = shapes[i] + mark + "".join(reversed(shapes[i_]))
        # 获取五连
        for match in renju5.finditer(line_shape):
            span = match.span()
            renju_5.append(Location_5(get_point(point, i, len(shapes[i]) - span[0]), i_))
        # 获取长连
        for match in renju5_.finditer(line_shape):
            span = match.span()
            rot.append(Location_5_(get_point(point, i, len(shapes[i]) - span[0]), i_, span[1] - span[0]))
    return renju_5, rot


def get_f_renju_34(checkerboard, point: Point):
    """
    禁手状态下,
    如果点上已经有棋子，那就是获取放置棋子之后新增的活三和四;
    如果点上没有棋子，那就获取点周围的活三和四
    """
    shapes = checkerboard.point_shape(point, game.BLACK_CHESSMAN.piece())
    live3, old_live3, renju_4, old_renju4 = [], [], [], []
    for i in range(4):
        i_ = i + 4  # 反方向的下标
        line_shape = shapes[i] + X_MARK + "".join(reversed(shapes[i_]))
        old_shape = shapes[i] + NONE_MARK + "".join(reversed(shapes[i_]))
        # 统计活三的数量和位置
        for renju in f_renju_live3:
            for match in renju.finditer(line_shape):
                live3.append(Location(get_point(point, i, len(shapes[i]) - match.span()[0]), i_, renju))
            for match in renju.finditer(old_shape):
                old_live3.append(Location(get_point(point, i, len(shapes[i]) - match.span()[0]), i_, renju))
        # 统计四的数量和位置
        for renju in f_renju4:
            for match in renju.finditer(line_shape):
                renju_4.append(Location(get_point(point, i, len(shapes[i]) - match.span()[0]), i_, renju))
            for match in renju.finditer(old_shape):
                old_renju4.append(Location(get_point(point, i, len(shapes[i]) - match.span()[0]), i_, renju))

    def get_effective_renju(locations: list[Location]):
        """
        获取有效的连珠
        """
        effective_renju = []
        for loc in locations:
            for p in loc.renju.get_build_points(loc.point, loc.i):
                is_p = check_forbidden(checkerboard, p, backup=False)[0]
                if not is_p:  # 不是禁手点
                    effective_renju.append(loc)
                    break
        return effective_renju

    if len(live3 := list(set(live3) - set(old_live3))) >= 2:
        live3 = get_effective_renju(live3)

    if len(renju_4 := list(set(renju_4) - set(old_renju4))) >= 2:
        renju_4 = get_effective_renju(renju_4)
    return live3, renju_4


def get_renju_34(checkerboard, point: Point, x_piece: int):
    """
    获取无禁手下的活三和四
    """
    shapes, have_piece = checkerboard.point_shape(point, x_piece), checkerboard.have_piece(point)
    live_3, old_live3, renju_4, old_renju4 = [], [], [], []
    for i in range(4):
        i_ = i + 4  # 反方向的下标
        line_shape = shapes[i] + X_MARK + "".join(reversed(shapes[i_]))
        old_shape = shapes[i] + NONE_MARK + "".join(reversed(shapes[i_]))
        # 统计活三的数量和位置
        for renju in renju_live_3:
            if have_piece:
                for match in renju.finditer(line_shape):
                    live_3.append(Location(get_point(point, i, len(shapes[i]) - match.span()[0]), i_, renju))

            old_live3 += [
                Location(get_point(point, i, len(shapes[i]) - match.span()[0]), i_, renju)
                for match in renju.finditer(old_shape)
            ]
        # 统计四的数量和位置
        for renju in renju4:
            if have_piece:
                for match in renju.finditer(line_shape):
                    renju_4.append(Location(get_point(point, i, len(shapes[i]) - match.span()[0]), i_, renju))
            for match in renju.finditer(old_shape):
                old_renju4.append(Location(get_point(point, i, len(shapes[i]) - match.span()[0]), i_, renju))
    if have_piece:
        return list(set(live_3) - set(old_live3)), list(set(renju_4) - set(old_renju4))  # 去重
    else:
        return old_live3, old_renju4


def get_mark(old_cb, new_cb, point, x_piece):
    def mark(piece):
        if piece == 0:
            if new_cb.forbidden_points().__contains__(point) and game.BLACK_CHESSMAN.piece() == x_piece:
                return BLOCK_MARK
            else:
                return NONE_MARK
        elif piece == x_piece:
            return X_MARK
        else:
            return BLOCK_MARK

    old_piece, new_piece = old_cb.get_piece(point=point), new_cb.get_piece(point=point)

    if new_piece == old_piece == 0:
        # 点变禁手点或禁手点被解除的情况
        if x_piece == game.WHITE_CHESSMAN.piece():
            return NONE_MARK, NONE_MARK
        elif x_piece == game.BLACK_CHESSMAN.piece():
            # 黑方禁手点发生变动
            if new_cb.forbidden_points().__contains__(point):
                # 变为禁手点
                return NONE_MARK, BLOCK_MARK
            else:
                # 禁手点解禁
                return BLOCK_MARK, NONE_MARK
        else:
            return BLOCK_MARK, BLOCK_MARK

    return mark(old_piece), mark(new_piece)


def get_renju(old_cb, new_cb, point: Point, x_piece: int):
    add = {
        "sleep2": set(),
        "live2": set(),
        "sleep3": set(),
        "live3": set(),
        "renju4": set(),
    }
    loss = {
        "sleep2": set(),
        "live2": set(),
        "sleep3": set(),
        "live3": set(),
        "renju4": set(),
    }
    old_shapes = old_cb.point_shape(point, x_piece)
    new_shapes = new_cb.point_shape(point, x_piece)

    old_mark, new_mark = get_mark(old_cb, new_cb, point, x_piece)
    if old_mark == new_mark:
        return add, loss

    for i in range(4):
        i_ = i + 4
        old_shape = old_shapes[i] + old_mark + "".join(reversed(old_shapes[i_]))
        new_shape = new_shapes[i] + new_mark + "".join(reversed(new_shapes[i_]))
        for key, rs in key_r:
            for renju in rs:
                new = set(
                    Location(get_point(point, i, len(old_shapes[i]) - match.span()[0]), i_, renju)
                    for match in renju.finditer(new_shape)
                )
                old = set(
                    Location(get_point(point, i, len(new_shapes[i]) - match.span()[0]), i_, renju)
                    for match in renju.finditer(old_shape)
                )
                add[key] = add[key] | (new - old)
                loss[key] = loss[key] | (old - new)
    return add, loss


def get_f_renju(old_cb, new_cb, point: Point):
    """
    获取在禁手条件下point周围的新旧连珠
    :param old_cb: 旧棋盘
    :param new_cb: 新棋盘
    :param point: 坐标
    """
    add = {
        "sleep2": set(),
        "live2": set(),
        "sleep3": set(),
        "live3": set(),
        "renju4": set(),
    }
    loss = {
        "sleep2": set(),
        "live2": set(),
        "sleep3": set(),
        "live3": set(),
        "renju4": set(),
    }
    x_piece = game.BLACK_CHESSMAN.piece()
    old_shapes = old_cb.point_shape(point, x_piece, consider_forbidden=True)
    new_shapes = new_cb.point_shape(point, x_piece, consider_forbidden=True)

    old_mark, new_mark = get_mark(old_cb, new_cb, point, x_piece)

    if old_mark == new_mark:
        return add, loss

    for i in range(4):
        i_ = i + 4
        old_shape = old_shapes[i] + old_mark + "".join(reversed(old_shapes[i_]))
        new_shape = new_shapes[i] + new_mark + "".join(reversed(new_shapes[i_]))
        for key, rs in f_key_r:
            for renju in rs:
                new = set(
                    Location(get_point(point, i, len(new_shapes[i]) - match.span()[0]), i_, renju)
                    for match in renju.finditer(new_shape)
                )
                old = set(
                    Location(get_point(point, i, len(old_shapes[i]) - match.span()[0]), i_, renju)
                    for match in renju.finditer(old_shape)
                )
                add[key] = add[key] | (new - old)  # 新增的连珠
                loss[key] = loss[key] | (old - new)  # 减少的连珠
    return add, loss


# @lru_cache(maxsize=2048)  # 没啥必要，变化频率太高了
def check_forbidden(checkerboard, point: Point, get_reason=False, place_piece=True, backup=True):
    """
    判断这个点是不是禁手点
    :returns
        is_: 如果这个点是禁手点，则为True，否则返回False.
        points: [Point],
            在 get_reason 为 True 时，返回导致了禁手的点，否则返回 [].
    """
    if checkerboard.get_piece(point=point) != checkerboard.none_piece() and place_piece:
        return False, set()
    if backup:
        checkerboard = deepcopy(checkerboard)
    if place_piece:
        checkerboard.place(point, game.BLACK_CHESSMAN.piece(), simulation=True)
    # 获取连珠
    live_3, renju_4 = get_f_renju_34(checkerboard, point)
    renju_5, rot = get_renju_5(checkerboard, point, game.BLACK_CHESSMAN.piece())
    # 判断是否禁手
    points = set()  # 导致禁手的坐标
    if len(renju_5) == 0:
        # 没有五连
        # 存在两个活三
        if is_33 := len(live_3) >= 2:
            if get_reason:
                for loc3 in live_3:
                    points = points | set(loc3.renju.get_shape_points(loc3.point, loc3.i))
        # 存在两个四
        if is_44 := len(renju_4) >= 2:
            if get_reason:
                for loc4 in renju_4:
                    points = points | set(loc4.renju.get_shape_points(loc4.point, loc4.i))
        # 判断长连
        if is_rot := len(rot) > 0:
            if get_reason:  # 长连没有固定形状，只能这么搞..
                for i, start, end in rot:
                    points = points | set(get_point(point, i, k) for k in range(1, start - end - 1))
        is_ = is_33 or is_44 or is_rot
    else:
        # 有五连
        is_ = False
    # 移除棋子
    if place_piece:
        checkerboard.remove_piece(point, simulation=True)
    return is_, points


def is_forbidden(live_3, renju_4, renju_5, rot):
    if len(renju_5) == 0:
        return len(live_3) > 2 or len(renju_4) > 2 or len(rot) > 0
    else:
        return False


def get_all(checkerboard, piece: int, is_black: bool):
    lines_shape = checkerboard.get_all_lines_shape(piece, is_black and checkerboard.forbidden_moves)
    all_renju = {
        "sleep2": [],
        "live2": [],
        "sleep3": [],
        "live3": [],
        "renju4": [],
    }

    def analysis(line_key: str, loc_i: int, renju_live2, renju_sleep2, renju_live3, renju_sleep3, renju_4):
        for p0, shape in lines_shape[line_key]:
            for renju in renju_live2:  # 活二
                for match in renju.finditer(shape):
                    all_renju["live2"].append(Location(get_point(p0, loc_i, match.span()[0] - 1), loc_i, renju))
            for renju in renju_sleep2:  # 眠二
                for match in renju.finditer(shape):
                    all_renju["sleep2"].append(Location(get_point(p0, loc_i, match.span()[0] - 1), loc_i, renju))
            for renju in renju_live3:  # 活三
                for match in renju.finditer(shape):
                    all_renju["live3"].append(Location(get_point(p0, loc_i, match.span()[0] - 1), loc_i, renju))
            for renju in renju_sleep3:  # 眠三
                for match in renju.finditer(shape):
                    all_renju["sleep3"].append(Location(get_point(p0, loc_i, match.span()[0] - 1), loc_i, renju))
            for renju in renju_4:  # 四连
                for match in renju.finditer(shape):
                    all_renju["renju4"].append(Location(get_point(p0, loc_i, match.span()[0] - 1), loc_i, renju))

    if checkerboard.forbidden_moves and is_black:
        for key, i in key_i:
            analysis(key, i, f_renju_live2, f_renju_sleep2, f_renju_live3, f_renju_sleep_3, f_renju4)
    else:
        for key, i in key_i:
            analysis(key, i, renju_live_2, renju_sleep_2, renju_live_3, renju_sleep_3, renju4)
    return all_renju


def black_all_renju(checkerboard):
    return get_all(checkerboard, game.BLACK_CHESSMAN.piece(), True)


def white_all_renju(checkerboard):
    return get_all(checkerboard, game.WHITE_CHESSMAN.piece(), False)


def get_all_renju(checkerboard):
    black_all = black_all_renju(checkerboard)
    white_all = white_all_renju(checkerboard)
    return black_all, white_all
