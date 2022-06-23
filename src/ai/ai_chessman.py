import random
import threading
import time
import src.ai.compute as ai_compute
from multiprocessing import Process, Pipe
from src import config as CONFIG

from src.ai.compute import iter_depth, vcf, vct
from src.gomoku import direction, game
from src.gomoku.game import Point

thinking = False
pipe = Pipe()  # 创建管道


def corresponding_chessman():
    """
    获取AI对应的棋手
    """
    return game.BLACK_CHESSMAN if CONFIG.ai_is_black else game.WHITE_CHESSMAN


def check_timeout(t0: float, te):
    """
    检查是否超时
    """
    global thinking
    while True:
        if time.time() - t0 >= te or not thinking:
            thinking = False
            break
        time.sleep(1)


def check_break(p1):
    """
    检查是否终止计算
    """
    p1.recv()
    global thinking
    thinking = False
    print("计算终止!")


def compute(p1):
    checkerboard = p1.recv()  # 接收棋盘
    global thinking
    thinking = True

    check_time_thread = threading.Thread(target=check_timeout, args=(time.time(), CONFIG.time_out))
    check_time_thread.start()  # 检查超时
    check_break_thread = threading.Thread(target=check_break, args=(p1,))
    check_break_thread.start()  # 检查退出信号

    self_is_black = game.is_black_now(checkerboard)
    if (p := vcf(checkerboard, self_is_black)) is not None:
        pass  # 己方VCF
    elif vcf(checkerboard, not self_is_black) is None:  # 敌方VCF
        print("敌方无VCF，计算VCT中...")
        if (p := vct(checkerboard, self_is_black)) is not None:  # 敌方VCF不存在时我方尝试VCT
            print("我方存在VCT！")
        else:
            print("我方不存在VCT！")

    if p is None:
        # 迭代加深搜索
        p = iter_depth(checkerboard, self_is_black)
    print(f'compute_times: {ai_compute.compute_times}')
    p1.send(p)
    thinking = False


def start_thinking(after_get):
    """
    等待计算结果
    """
    global thinking
    thinking = True
    pipe[0].send(game.checkerboard)  # 不拷贝也可以...

    # 创建一个新进程来计算，避免游戏界面卡顿
    t1 = time.time()
    compute_thread = Process(target=compute, args=(pipe[1],))
    compute_thread.start()

    point = pipe[0].recv()
    stop_thinking()  # 终止计算
    print(f"time: {time.time() - t1}, best point: {point}")
    if point is not None and game.start:
        game.place(point, game.now_chessman())  # 无所谓了，反正鼠标不能放置棋子，棋盘不会变动，现在的棋手也不会有变动

    if after_get is not None:
        after_get(point)


def stop_thinking():
    """
    AI停止计算
    """
    global thinking
    if thinking:
        pipe[0].send("终止运行。。")
    thinking = False


def start_point() -> Point:
    """
    获取开局点
    """
    point = None
    x, y = game.row // 2, game.col // 2  # 中心点
    if CONFIG.ai_is_black and game.BLACK_CHESSMAN.len_records() == 0:
        point = Point(x, y)  # 默认黑方先手放在中间

    elif CONFIG.ai_is_black and game.BLACK_CHESSMAN.len_records() == 1:
        dx, dy = direction[random.randint(0, 7)]  # 黑方第二手在周围随机布局
        while point := Point(x + dx * random.randint(1, 2), y + dy * random.randint(1, 2)):
            if game.can_place(point):
                break
            dx, dy = direction[random.randint(0, 7)]

    elif not CONFIG.ai_is_black and game.WHITE_CHESSMAN.len_records() == 0:
        # 白方第一手在黑方周围
        black_last = game.BLACK_CHESSMAN.last_point()
        if black_last.X == x:
            if black_last.Y == y:
                dx, dy = direction[random.randint(0, 7)]
                point = Point(x + dx, y + dy)

            elif black_last.Y < y:
                point = Point(x, black_last.Y + 1)

            else:
                point = Point(x, black_last.Y - 1)

        elif black_last.X < x:
            if black_last.Y == y:
                point = Point(black_last.X + 1, y)

            elif black_last.Y < y:
                while point := Point(black_last.X + random.randint(0, 1), black_last.Y + random.randint(0, 1)):
                    if game.can_place(point):
                        break
            else:
                while point := Point(black_last.X + random.randint(0, 1), black_last.Y - random.randint(0, 1)):
                    if game.can_place(point):
                        break
        else:
            if black_last.Y == y:
                point = Point(black_last.X - 1, y)

            elif black_last.Y < y:
                while point := Point(black_last.X - random.randint(0, 1), black_last.Y + random.randint(0, 1)):
                    if game.can_place(point):
                        break
            else:
                while point := Point(black_last.X - random.randint(0, 1), black_last.Y - random.randint(0, 1)):
                    if game.can_place(point):
                        break
    return point


def get_point(call_back):
    """
    获取接下来要放置的位置
    """
    # ai计算要丢到另一个线程，否则游戏会无响应
    if game.winner is None:
        # thread和主线程的值是相同的，需要创建一个新的线程，来等待计算进程的结果
        if game.checkerboard.piece_count() < 3:
            p = start_point()
            game.place(p, corresponding_chessman())
            if call_back is not None:
                call_back(p)
        else:
            wait_thread = threading.Thread(target=start_thinking, args=(call_back,))
            wait_thread.start()
