from collections import namedtuple

Direction = namedtuple("Direction", ["dx", "dy"])
Point = namedtuple('Point', ['X', "Y"])

direction = (
    Direction(-1, 0),  # 0-上
    Direction(-1, -1),  # 1-左上
    Direction(0, -1),  # 2-左
    Direction(1, -1),  # 3-左下
    Direction(1, 0),  # 4-下
    Direction(1, 1),  # 5-右下
    Direction(0, 1),  # 6-右
    Direction(-1, 1)  # 7-右上
)
UPPER, UPPER_LEFT, LEFT, LOWER_LEFT, LOWER, LOWER_RIGHT, RIGHT, UPPER_RIGHT = 0, 1, 2, 3, 4, 5, 6, 7
BLOCK_MARK = "|"
NONE_MARK = "o"
X_MARK = "x"


def get_point(point: Point, i, distance):
    """
    获取坐标
    :param point: 初始坐标
    :param i: 偏移方向
    :param distance: 距离
    """
    return Point(point.X + direction[i].dx * distance, point.Y + direction[i].dy * distance)
