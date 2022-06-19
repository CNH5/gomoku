import re
from src.gomoku import get_point


class Renju:
    """
    连珠类
    """

    def __init__(self, shape_reg, points_index: [int], build_index: [int], block_index=None, score: int = 0):
        """
        :param shape_reg: 连珠形状的正则表达式
        :param points_index: 连珠拥有的棋子位置
        :param build_index: 成形的位置
        :param score 连珠的分数
        """
        self._reg = re.compile(shape_reg)  # 提前编译好
        self._points_index = points_index
        self._build_index = build_index
        if block_index is None:
            self._block_index = self._build_index
        else:
            self._block_index = block_index
        self._score = score

    def finditer(self, shape: str):
        return self._reg.finditer(shape)

    def score(self):
        """
        获取连珠的分值
        """
        return self._score

    def get_shape_points(self, start, i: int):
        """
        获取连珠的形状所在的坐标
        :param start: 起始点
        :param i: 方向
        """
        return [get_point(start, i, d) for d in self._points_index]

    def get_build_points(self, start, i: int):
        """
        获取连珠成型点所在的坐标
        :param start: 起始点
        :param i: 方向
        """
        return [get_point(start, i, d) for d in self._build_index]

    def get_block_points(self, start, i):
        """
        获取阻挡点的坐标
        """
        return [get_point(start, i, d) for d in self._block_index]

    def __str__(self):
        return f"pattern: {self._reg.pattern}, build_index: {self._build_index}, score: {self._score}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hash__() == other.__hash__()
        else:
            return False


# 分数
sleep_2_score = 400
live_2_score = 1500
sleep_3_score = 2000
live_3_score = 8000
chong_4_score = 20_000
live_4_score = 200_000
renju_5_score = 1000_000
forbidden_point_score = 1000
