from collections import namedtuple
from enum import Enum, unique

Point = namedtuple('Point', ['X', "Y"])

Direction = namedtuple("Direction", ["dx", "dy"])
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
BLOCK_MARK, NONE_MARK, X_MARK = "|", "o", "x"  # 三种符号标记的


@unique
class Direction(Enum):
    """
    八个方向的枚举类
    """

    class _OneDirection:
        """
        表示一个方向
        """

        def __init__(self, dx: int, dy: int):
            self._dx, self._dy = dx, dy

        def get_point(self, start: Point, d):
            return Point(start.X + self._dx * d, start.Y + self._dy * d)

    # 上
    UPPER = _OneDirection(-1, 0)
    # 左上
    UPPER_LEFT = _OneDirection(-1, -1)
    # 左
    LEFT = _OneDirection(0, -1)
    # 左下
    LOWER_LEFT = _OneDirection(1, -1)
    # 下
    LOWER = _OneDirection(1, 0)
    # 右下
    LOWER_RIGHT = _OneDirection(1, 1)
    # 右
    RIGHT = _OneDirection(0, 1)
    # 右上
    UPPER_RIGHT = _OneDirection(-1, 1)

    def reverse(self, direction_name: str):
        """
        返回相反的方向
        """
        if self.UPPER.name == direction_name:
            return self.LOWER

        elif self.UPPER_LEFT.name == direction_name:
            return self.LOWER.value

        elif self.LEFT.name == direction_name:
            return self.RIGHT

        elif self.LOWER_LEFT.name == direction_name:
            return self.UPPER_RIGHT

        elif self.LOWER.name == direction_name:
            return self.UPPER

        elif self.LOWER_RIGHT.name == direction_name:
            return self.LOWER

        elif self.RIGHT.name == direction_name:
            return self.LEFT

        elif self.UPPER_RIGHT.name == direction_name:
            return self.LOWER_LEFT

        else:
            return None


def get_point(point: Point, i, distance):
    """
    获取坐标
    :param point: 初始坐标
    :param i: 偏移方向
    :param distance: 距离
    """
    return Point(point.X + direction[i].dx * distance, point.Y + direction[i].dy * distance)
