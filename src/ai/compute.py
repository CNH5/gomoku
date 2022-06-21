import math
import random
from collections import namedtuple
from functools import lru_cache

from src.ai import ai_chessman
from src.ai.cache import Cache
from src.ai.zobrist import zobrist
from src.gomoku import game, Point  # 不导入这个Point不方便debug
from src.gomoku.checkerboard import Checkerboard
from src.gomoku.renju import forbidden_point_score, renju_5_score

Node = namedtuple("Node", ["score", "depth", "point"])

DEPTH = 8  # 6层太弱，8层太慢，还是搞8层算了...
compute_times = 0


def get_camp_renju(checkerboard, self_is_black):
    """
    获取敌我双方的连珠
    """
    if self_is_black:
        return checkerboard.renju_black(), checkerboard.renju_white()
    else:
        return checkerboard.renju_white(), checkerboard.renju_black()


def gen(checkerboard: Checkerboard, self_is_black: bool):
    """
    启发式搜索...
    """
    consider_points = checkerboard.edge_points()  # 棋盘上的边界点
    if checkerboard.forbidden_moves and self_is_black:
        # 黑方需要不考虑禁手点
        consider_points = consider_points - set(checkerboard.forbidden_points())

    self, enemy = get_camp_renju(checkerboard, self_is_black)

    atk_p, def_p = [], []
    for p in consider_points:
        atk_score, def_score = 0, 0
        for k in list(self.keys())[:3]:  # 眠二、活二、眠三
            atk_score += sum(
                r.renju.score() for r in self[k] if r.renju.get_build_points(r.point, r.i).__contains__(p)
            )
            def_score += sum(
                r.renju.score() for r in enemy[k] if r.renju.get_block_points(r.point, r.i).__contains__(p)
            )
        score = atk_score - def_score
        if score > 0:
            atk_p.append((p, score))
        else:
            def_p.append((p, score))
    return [p_s[0] for p_s in sorted(atk_p, key=lambda x: -x[1])], [p_s[0] for p_s in sorted(def_p, key=lambda x: x[1])]


@lru_cache(maxsize=4096)  # 这个缓存起来还是很有必要的
def get_consider_points(checkerboard: Checkerboard, depth: int, self_is_black: bool, only_three=False, only_four=False):
    """
    获取进攻点和防守点，没有就转启发式搜索
    :returns atk_p, def_p
    """
    self, enemy = get_camp_renju(checkerboard, self_is_black)
    # 应对冲四和活四
    if len(self["renju4"]) > 0:  # 自己有四，就连五
        loc = self["renju4"][random.randint(0, len(self["renju4"]) - 1)]
        ps = loc.renju.get_build_points(loc.point, loc.i)
        return [ps[random.randint(0, len(ps) - 1)]], []

    elif len(enemy["renju4"]) > 0:  # 自己没四，敌方有四，只能阻挡一个
        loc = enemy["renju4"][random.randint(0, len(enemy["renju4"]) - 1)]
        ps = loc.renju.get_build_points(loc.point, loc.i)
        return [], [ps[random.randint(0, len(ps) - 1)]]

    # 在每一层开始的时候计算VCF，但是速度太慢了，扫描一层的时间翻了十多倍...
    # if not (only_three ^ only_four):
    #     print("开始计算VCF")
    #     if (p := vcf(checkerboard, self_is_black)) is not None:
    #         # 计算己方vcf
    #         print("VCF成功!")
    #         return [p], []
    #     print("VCF失败!")

    if len(self["live3"]) > 0:
        # 自己有活三，对方没有四，绝对要优先活四
        loc = self["live3"][random.randint(0, len(self["live3"]) - 1)]
        atk_p = loc.renju.get_build_points(loc.point, loc.i)
        return [atk_p[random.randint(0, len(atk_p) - 1)]], []  # 随机选一个就可以了

    elif len(self["sleep3"]) > 0 and len(self["live2"]) > 0 and not (only_three ^ only_four):
        # 找四三点
        p_c4, p_l3, p_43, p_33 = set(), set(), set(), set()
        for loc in self["sleep3"]:
            p_ = set(loc.renju.get_build_points(loc.point, loc.i))
            if len(p_44 := p_ & p_c4) > 0:  # 存在四四点，必胜了
                return list(p_44)[:1], []
            p_c4 = p_c4 | p_  # 合并冲四点

        for loc in self["live2"]:
            p_ = set(loc.renju.get_build_points(loc.point, loc.i))
            p_43 = p_43 | (p_c4 & p_)  # 四三点
            p_33 = p_33 | (p_l3 & p_)  # 三三点
            p_l3 = p_l3 | p_

        if len(p_43) > 0 and (p := vcf(checkerboard, self_is_black)) is not None:
            # 用VCF去判断能否四三杀
            return [p], []

        if len(p_33) > 0 and vcf(checkerboard, not self_is_black) is None \
                and (p := vct(checkerboard, self_is_black)) is not None:
            # 用VCT去判断能否三三杀,在这之前需要判断敌方能否VCF
            return [p], []

    if len(enemy["live3"]) > 0:  # 敌方有活三,我方无四和活三，需要考虑VCF和阻挡活三
        atk_p, def_p = set(), set()  # 冲四点
        for loc in self["sleep3"]:
            atk_p = atk_p | set(loc.renju.get_build_points(loc.point, loc.i))

        if not only_three and only_four:  # VCF时
            return list(atk_p), []

        for loc in enemy["live3"]:  # 敌方活三的防点
            def_p = def_p | set(loc.renju.get_block_points(loc.point, loc.i))
        return list(atk_p), list(def_p)

    elif len(enemy["sleep3"]) > 0 and len(enemy["live2"]) > 0:
        p_c4, p_l3, bp_43, bp_33 = set(), set(), set(), set()
        for loc in enemy["sleep3"]:
            p_ = set(loc.renju.get_build_points(loc.point, loc.i))
            if len(p_44 := p_ & p_c4) > 0:  # 四四点,必定要防
                return [], list(p_44)[:1]
            p_c4 = p_c4 | p_  # 合并冲四点

        for loc in enemy["live2"]:
            p_ = set(loc.renju.get_build_points(loc.point, loc.i))
            if len(p_c4 & p_) > 0:  # 敌方四三点
                bp_43 = bp_43 | set(loc.renju.get_block_points(loc.point, loc.i))
            if len(p_l3 & p_) > 0:  # 敌方三三点
                bp_33 = bp_33 | set(loc.renju.get_block_points(loc.point, loc.i))
            p_l3 = p_l3 | p_

        atk_p = set()
        for loc in self["sleep3"]:
            atk_p = atk_p | set(loc.renju.get_build_points(loc.point, loc.i))

        if len(bp_43) > 0:
            return list(atk_p), list(bp_43)

        if len(bp_33) > 0:
            for loc in self["live2"]:
                atk_p = atk_p | set(loc.renju.get_build_points(loc.point, loc.i))
            return list(atk_p), list(bp_33)

    if only_four ^ only_three:
        # 没有必定要防的点,且在计算vct或vcf
        if depth % 2 == 0:  # 敌方取得先手,没必要往下了
            return [], []

        atk_p = set()
        for loc in self["sleep3"]:
            atk_p = atk_p | set(loc.renju.get_build_points(loc.point, loc.i))
        if only_four:  # VCF只需要考虑冲四
            return list(atk_p), []

        else:  # VCT的时候需要考虑活二
            for loc in self["live2"]:
                atk_p = atk_p | set(loc.renju.get_build_points(loc.point, loc.i))
            return list(atk_p), []

    return gen(checkerboard, self_is_black)


def evaluation(checkerboard: Checkerboard):
    """
    评估函数,统计第0层的分数
    """
    self_is_black = game.is_black_now(checkerboard)
    black = checkerboard.renju_black()
    white = checkerboard.renju_white()

    black_score, white_score = 0, 0
    for key in list(black.keys())[:4]:
        black_score += sum([loc.renju.score() for loc in black[key]])
        for loc in white[key]:
            white_score += loc.renju.score()
            if checkerboard.forbidden_moves:
                white_score += \
                    forbidden_point_score * \
                    len([
                        p for p in loc.renju.get_block_points(loc.point, loc.i)
                        if checkerboard.forbidden_points().__contains__(p)
                    ])

    return black_score - white_score if not self_is_black else white_score - black_score


def negamax(checkerboard, max_depth, self_is_black: bool, alpha=-99999999, beta=99999999,
            cache: Cache = None, depth=1, only_three=False, only_four=False):
    """
    极大极小搜索 + Alpha Beta剪枝
    :return
        score: 当前计算的最优alpha
        depth: 最优节点的计算深度
        point: 最优点
    """
    if cache is None:
        cache = Cache()
    global compute_times
    compute_times += 1
    if (node := cache.get(zobrist.code)) is not None and \
            (node.depth >= max_depth or math.fabs(node.score) == renju_5_score):
        # 之前计算过同样情况下深度更大的情况，计算得到必败或必胜则有效，没有必要重复计算
        return node

    atk_p, def_p = get_consider_points(checkerboard, depth, self_is_black, only_three=only_three, only_four=only_four)

    if len(atk_p) == 1 and len(def_p) == 0:
        # 完全不需要防守, 且只有一个进攻点
        return Node(renju_5_score, depth, atk_p[0])

    if len(atk_p) == 0 and len(def_p) > 0 and self_is_black and checkerboard.forbidden_moves \
            and len(set(def_p) - checkerboard.forbidden_points()) == 0:
        # 黑方被迫防守的点全是禁手点，则判断此时黑方必败
        return Node(-renju_5_score, depth, def_p[0])

    if depth == 1 and len(atk_p) == 0 and len(def_p) == 1:
        # 在考虑的时候敌方已经有冲四，不必继续往下
        return Node(0, depth, def_p[0])

    if depth == max_depth or len(atk_p) + len(def_p) == 0:
        # 达到最大计算深度或者不必继续往下
        return Node(evaluation(checkerboard), depth, None)

    point, d1, is_vcx = None, depth, only_three ^ only_four
    for p in set(atk_p + def_p):
        if self_is_black and checkerboard.forbidden_points().__contains__(p):
            # 黑方落子到禁手点，直接负最高分
            score = -renju_5_score  # 必败节点被剪枝，导致失误?
            d = depth
        else:
            # 落子，算分，移除棋子
            checkerboard.place(p, game.get_piece(self_is_black), update_edge=not is_vcx)  # vcx时没必要更新边界点
            node = negamax(
                checkerboard, max_depth, not self_is_black, alpha=-beta, beta=-alpha, cache=cache,
                depth=depth + 1, only_three=only_three, only_four=only_four
            )
            score, d = -node.score, node.depth
            checkerboard.remove_piece(p, update_edge=not is_vcx)
        if score > alpha:
            if score >= beta:  # Alpha Beta剪枝
                cache.save(zobrist.code, Node(alpha, max_depth, p))
                return Node(beta, d, None)
            point, d1 = p, d
            alpha = score
        elif score == alpha and alpha < 0 and d > d1:  # 分数相同且己方处于劣势，选取深度大的
            point, d1 = p, d

        print(f"depth={depth}, score={score}, {p}")
        if alpha == renju_5_score or not ai_chessman.thinking:
            # 出现必胜分支或超时，没必要计算其它分支了
            break
    cache.save(zobrist.code, Node(alpha, max_depth, point))
    return Node(alpha, d1, point)


def iter_depth(checkerboard: Checkerboard, self_is_black: bool, start=2,
               max_depth=DEPTH, cache: Cache = None, only_three=False, only_four=False):
    """
    迭代加深
    """
    if cache is None:
        cache = Cache()

    node = None
    for depth in range(start, max_depth, 2):
        node = negamax(
            checkerboard, max_depth=depth, self_is_black=self_is_black,
            cache=cache, only_three=only_three, only_four=only_four
        )
        print(node)
        if node.score == renju_5_score:
            # 必胜了
            break
    if only_three ^ only_four and not (node.score == renju_5_score):
        # 计算完VCF或VCT，没有找到结果
        return None
    return node.point


def vct(checkerboard, self_is_black: bool, max_depth=20, cache=None):
    if cache is None:
        cache = Cache()

    self, enemy = get_camp_renju(checkerboard, self_is_black)
    n = len(self["live2"])
    if n == 0 or len(enemy["live3"]) > 0 or len(enemy["renju4"]) > 0:
        # 没有活二，或当前没有先手，不可能VCT
        return None
    # VCT的最大深度不好确定，两个活二就能到12层...
    return iter_depth(checkerboard, self_is_black, max_depth=max_depth, cache=cache, only_three=True)


def vcf(checkerboard, self_is_black: bool, max_depth=12, cache=None):
    if cache is None:  # 在函数上面的Cache是同一个...
        cache = Cache()

    self, enemy = get_camp_renju(checkerboard, self_is_black)
    n = len(self["sleep3"])
    if n == 0 or len(enemy["renju4"]) > 0:
        # 没有眠三，不可能VCF
        return None
    # VCF的最小深度是4，深度一般不会超过眠三的数量太多
    max_depth = min((n if n % 2 == 0 else n + 1) + 6, max_depth)
    return iter_depth(checkerboard, self_is_black, max_depth=max_depth, cache=cache, only_four=True)
