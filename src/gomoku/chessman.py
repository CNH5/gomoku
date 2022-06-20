from copy import deepcopy

from pygame import surface
from src import config as CONFIG
from src.gomoku import Point, game
from main import black_piece_img, white_piece_img


class Chessman:
    # 棋手类
    def __init__(self, name: str, piece: int, repentance_times: int, piece_res: surface, records=None):
        if records is None:
            records: [Point] = []
        self.name = name  # 棋手名称
        self._piece = piece  # 棋子的值
        self.repentance_times = repentance_times  # 剩余悔棋次数
        self._records = records  # 落子记录
        self._piece_res = piece_res

    def piece(self):
        """
        获取棋子的值
        """
        return self._piece

    def piece_res(self) -> surface:
        """
        获取棋子的图片资源
        """
        return self._piece_res

    def reset(self, repentance_times, records=None):
        """
        重置悔棋次数和落子记录
        """
        if records is None:
            self._records = []
        else:
            self._records = records
        self.repentance_times = repentance_times

    def len_records(self) -> int:
        """
        获取落子记录
        """
        return len(self._records)

    def records(self):
        """
        获取落子记录的拷贝
        """
        return deepcopy(self._records)

    def last_point(self) -> Point:
        """
        获取最后一个落点
        """
        return self._records[-1] if len(self.records()) > 0 else None

    def use_repentance(self) -> None:
        """
        消耗一次悔棋机会
        """
        if game.infinity_repentance:
            self.repentance_times -= 1

    def can_repentance(self) -> bool:
        """
        棋手是否还可以悔棋
        """
        return (self.repentance_times > 0 or game.infinity_repentance) and len(self._records) > 0

    def pop_record(self) -> Point:
        """
        移除最后一条落子记录
        """
        return self._records.pop(-1)

    def add_record(self, point: Point) -> None:
        """
        添加落子记录
        :param point:
        """
        self._records.append(point)

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hash__() == other.__hash__()
        else:
            return False


BLACK_CHESSMAN = Chessman(name="黑棋", piece=1, repentance_times=CONFIG.repentance_times, piece_res=black_piece_img)
WHITE_CHESSMAN = Chessman(name="白棋", piece=-1, repentance_times=CONFIG.repentance_times, piece_res=white_piece_img)
