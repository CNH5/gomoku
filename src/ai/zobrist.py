import random

import numpy as np

from src.gomoku import Point


class Zobrist:
    _black: np.ndarray
    _white: np.ndarray

    def __init__(self, n=15, m=15):
        # 初始化 Zobrist 哈希值
        self.code = self._rand()
        self.reset(n, m)

    def reset(self, n, m):
        # 初始化两个 n × m 的空数组
        self._black = np.empty([n, m], dtype=int)
        self._white = np.empty([n, m], dtype=int)

        # 数组与棋盘相对应
        # 给每一个位置附上一个随机数, 代表不同的状态
        for i in range(n):
            for j in range(m):
                self._black[i, j] = self._rand()
                self._white[i, j] = self._rand()

    @staticmethod
    def _rand():
        return random.randint(0, np.int64(1 << 31))

    def go(self, point: Point, is_black):
        # 判断本次操作是 AI 还是人, 并返回相应位置的随机数
        arr = self._black if is_black else self._white
        # 当前键值异或位置随机数
        self.code = self.code ^ arr[point.X, point.Y]


zobrist = Zobrist()
