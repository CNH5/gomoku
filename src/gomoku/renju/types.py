from src.gomoku.renju import Renju, live_2_score, sleep_2_score, live_3_score, sleep_3_score, chong_4_score, \
    live_4_score, renju_5_score

# 无禁手活二
renju_live_2 = (
    Renju('[|]oxxooo', points_index=[2, 3], build_index=[4, 5], block_index=[1, 4, 5, 6], score=live_2_score),
    Renju('oooxxo[|]', points_index=[3, 4], build_index=[1, 2], block_index=[0, 1, 2, 5], score=live_2_score),
    Renju('oooxxooo', points_index=[3, 4], build_index=[1, 2, 5, 6], block_index=[2, 5], score=live_2_score),
    # 跳活二
    Renju('[|]oxoxoo', points_index=[2, 4], build_index=[3, 5], block_index=[1, 3, 5, 6], score=live_2_score),
    Renju('ooxoxo[|]', points_index=[2, 4], build_index=[1, 3], block_index=[0, 1, 3, 5], score=live_2_score),
    Renju('ooxoxoo', points_index=[2, 4], build_index=[1, 3, 5], block_index=[1, 3, 5], score=live_2_score),
    # 大跳活二
    Renju('oxooxo', points_index=[1, 4], build_index=[2, 3], block_index=[0, 2, 3, 5], score=live_2_score),
)
# 眠二
renju_sleep_2 = (
    Renju('[|]xxooo', points_index=[1, 2], build_index=[3, 4, 5], score=sleep_2_score),
    Renju('[|]xoxoo', points_index=[1, 3], build_index=[2, 4, 5], score=sleep_2_score),
    Renju('[|]xooxo', points_index=[1, 4], build_index=[2, 3, 5], score=sleep_2_score),
    Renju('oooxx[|]', points_index=[3, 4], build_index=[0, 1, 2], score=sleep_2_score),
    Renju('ooxox[|]', points_index=[2, 4], build_index=[0, 1, 3], score=sleep_2_score),
    Renju('oxoox[|]', points_index=[1, 4], build_index=[0, 2, 3], score=sleep_2_score),

    Renju('[|]oxoxo[|]', points_index=[2, 4], build_index=[1, 3, 5], score=sleep_2_score),
    Renju('[|]oxxoo[|]', points_index=[2, 3], build_index=[1, 4, 5], score=sleep_2_score),
    Renju('[|]ooxxo[|]', points_index=[3, 4], build_index=[1, 2, 5], score=sleep_2_score),

)
# 眠三
renju_sleep_3 = (
    Renju('ooxxx[|]', points_index=[2, 3, 4], build_index=[0, 1], score=sleep_3_score),
    Renju('oxoxx[|]', points_index=[1, 3, 4], build_index=[0, 2], score=sleep_3_score),
    Renju('oxxox[|]', points_index=[1, 2, 4], build_index=[0, 3], score=sleep_3_score),

    Renju('xxoox', points_index=[0, 1, 4], build_index=[2, 3], score=sleep_3_score),
    Renju('xoxox', points_index=[1, 2, 4], build_index=[1, 3], score=sleep_3_score),
    Renju('xooxx', points_index=[0, 3, 4], build_index=[1, 2], score=sleep_3_score),

    Renju('[|]xoxxo', points_index=[1, 3, 4], build_index=[2, 5], score=sleep_3_score),
    Renju('[|]xxoxo', points_index=[1, 2, 4], build_index=[3, 5], score=sleep_3_score),
    Renju('[|]xxxoo', points_index=[1, 2, 3], build_index=[4, 5], score=sleep_3_score),
    Renju('[|]oxxxo[|]', points_index=[2, 3, 4], build_index=[1, 5], score=sleep_3_score),
)
# 无禁手的活三
renju_live_3 = (
    Renju('oxoxxo', points_index=[1, 3, 4], build_index=[2], block_index=[0, 2, 5], score=live_3_score),
    Renju('oxxoxo', points_index=[1, 2, 4], build_index=[3], block_index=[0, 3, 5], score=live_3_score),
    Renju('ooxxxo[|]', points_index=[2, 3, 4], build_index=[1], block_index=[0, 1, 5], score=live_3_score),
    Renju('[|]oxxxoo', points_index=[2, 3, 4], build_index=[5], block_index=[1, 5, 6], score=live_3_score),
    Renju('ooxxxoo', points_index=[2, 3, 4], build_index=[1, 5], score=live_3_score),
)
# 冲四和活四
renju4 = (
    # 冲四
    Renju('xoxxx', points_index=[0, 2, 3, 4], build_index=[1], score=chong_4_score),
    Renju('xxoxx', points_index=[0, 1, 2, 4], build_index=[2], score=chong_4_score),
    Renju('xxxox', points_index=[0, 1, 2, 4], build_index=[3], score=chong_4_score),
    Renju('oxxxx[|]', points_index=[1, 2, 3, 4], build_index=[0], score=chong_4_score),
    Renju('[|]xxxxo', points_index=[1, 2, 3, 4], build_index=[5], score=chong_4_score),
    # 活四
    Renju('oxxxxo', points_index=[1, 2, 3, 4], build_index=[0, 5], score=live_4_score)
)
# 禁手活二,build变成活三
f_renju_live2 = (
    Renju('[|]oxxooo[^x]', points_index=[2, 3], build_index=[4, 5], score=live_2_score),
    Renju('[^x]oooxxo[|]', points_index=[4, 5], build_index=[2, 3], score=live_2_score),

    Renju('[^x]oooxxoo[|]', points_index=[4, 5], build_index=[2, 3, 6], score=live_2_score),
    Renju('[|]ooxxooo[^x]', points_index=[3, 4], build_index=[2, 5, 6], score=live_2_score),

    Renju('[^x]oooxxooo[^x]', points_index=[4, 5], build_index=[2, 3, 6, 7], score=live_2_score),
    # 跳活二
    Renju('[|]oxoxoo[^x]', points_index=[2, 4], build_index=[3, 5], score=live_2_score),
    Renju('[^x]ooxoxo[|]', points_index=[3, 5], build_index=[2, 4], score=live_2_score),
    Renju('[^x]ooxoxoo[^x]', points_index=[3, 5], build_index=[2, 4, 6], score=live_2_score),
    # 大跳活二
    Renju('[^x]oxooxo[^x]', points_index=[2, 5], build_index=[3, 4], score=live_2_score),
)
# 禁手眠二
f_renju_sleep2 = (
    # 手动判断活二没必要...
    # Renju('xxxoxxooo[^x]', points_index=[4, 5], build_index=[6, 7, 8], score=sleep_2_score),
    # Renju('[^x]oooxxoxxx', points_index=[4, 5], build_index=[1, 2, 3], score=sleep_2_score),
    Renju('[^x]xooox[^x]', points_index=[1, 5], build_index=[2, 3, 4], score=sleep_2_score),
    Renju('[|]xxooo[^x]', points_index=[1, 2], build_index=[3, 4, 5], score=sleep_2_score),
    Renju('[|]xoxoo[^x]', points_index=[1, 3], build_index=[2, 4, 5], score=sleep_2_score),
    Renju('[|]xooxo[^x]', points_index=[1, 4], build_index=[2, 3, 5], score=sleep_2_score),

    Renju('[|]oxoxo[|]', points_index=[2, 4], build_index=[1, 3, 5], score=sleep_2_score),
    Renju('[|]oxxoo[|]', points_index=[2, 3], build_index=[1, 4, 5], score=sleep_2_score),
    Renju('[|]ooxxo[|]', points_index=[3, 4], build_index=[1, 2, 5], score=sleep_2_score),

    Renju('[^x]oooxx[|]', points_index=[4, 5], build_index=[1, 2, 3], score=sleep_2_score),
    Renju('[^x]ooxox[|]', points_index=[3, 5], build_index=[1, 2, 4], score=sleep_2_score),
    Renju('[^x]oxoox[|]', points_index=[2, 5], build_index=[1, 3, 4], score=sleep_2_score),
)
# 禁手活三
f_renju_live3 = (
    # 右边堵住的活三
    Renju('[^x]ooxxxo([|]|(ox))', points_index=[3, 4, 5], build_index=[2], block_index=[1, 2, 6], score=live_3_score),
    # 跳活三
    Renju('[^x]oxoxxo[^x]', points_index=[2, 4, 5], build_index=[3], block_index=[1, 3, 6], score=live_3_score),
    Renju('[^x]oxxoxo[^x]', points_index=[2, 3, 5], build_index=[4], block_index=[1, 4, 6], score=live_3_score),
    # 左边堵住的活三
    Renju('[|]oxxxoo[^x]', points_index=[2, 3, 4], build_index=[5], block_index=[1, 5, 6], score=live_3_score),
    Renju('xooxxxoo[^x]', points_index=[3, 4, 5], build_index=[6], block_index=[2, 6, 7], score=live_3_score),
    # 两头活三
    Renju('[^x]ooxxxoo[^x]', points_index=[3, 4, 5], build_index=[2, 6], score=live_3_score),
)
# 禁手眠三
f_renju_sleep_3 = (
    # 这几个和冲四重复了...
    # Renju('[x]oxxxoo[^x]', points_index=[2, 3, 4], build_index=[5, 6], score=sleep_3_score),
    # Renju('[^x]ooxxxo[x]', points_index=[3, 4, 5], build_index=[1, 2], score=sleep_3_score),
    Renju('[|]oxxxo[|]', points_index=[2, 3, 4], build_index=[1, 5], score=sleep_3_score),

    Renju('[^x]ooxxx[|]', points_index=[3, 4, 5], build_index=[1, 2], score=sleep_3_score),
    Renju('[^x]oxoxx[|]', points_index=[1, 3, 4], build_index=[1, 3], score=sleep_3_score),
    Renju('[^x]oxxox[|]', points_index=[1, 2, 4], build_index=[1, 4], score=sleep_3_score),

    Renju('[^x]xxoox[^x]', points_index=[1, 2, 5], build_index=[3, 4], score=sleep_3_score),
    Renju('[^x]xoxox[^x]', points_index=[1, 3, 5], build_index=[2, 4], score=sleep_3_score),
    Renju('[^x]xooxx[^x]', points_index=[1, 4, 5], build_index=[2, 3], score=sleep_3_score),

    Renju('[|]xoxxo[^x]', points_index=[1, 3, 4], build_index=[2, 5], score=sleep_3_score),
    Renju('[|]xxoxo[^x]', points_index=[1, 2, 4], build_index=[3, 5], score=sleep_3_score),
    Renju('[|]xxxoo[^x]', points_index=[1, 2, 3], build_index=[4, 5], score=sleep_3_score),
)
# 禁手下的冲四和活四
f_renju4 = (
    # 冲四
    Renju('[^x]oxxxx([|]|(ox))', points_index=[2, 3, 4, 5], build_index=[1], score=chong_4_score),
    Renju('[^x]xoxxx[^x]', points_index=[1, 3, 4, 5], build_index=[2], score=chong_4_score),
    Renju('[^x]xxoxx[^x]', points_index=[1, 2, 4, 5], build_index=[3], score=chong_4_score),
    Renju('[^x]xxxox[^x]', points_index=[1, 2, 3, 5], build_index=[4], score=chong_4_score),
    Renju('[|]xxxxo[^x]', points_index=[1, 2, 3, 4], build_index=[5], score=chong_4_score),
    # 手动预判禁手点...
    Renju('xoxxxxo[^x]', points_index=[2, 3, 4, 5], build_index=[6], score=chong_4_score),
    # 活四
    Renju('[^x]oxxxxo[^x]', points_index=[2, 3, 4, 5], build_index=[1, 6], score=live_4_score),
)
# 五连
renju5 = Renju('[^x]x{5}[^x]', points_index=range(1, 6), build_index=[], score=renju_5_score)
# 长连
renju5_ = Renju('[^x]x{5,}[^x]', points_index=[], build_index=[], score=renju_5_score)
