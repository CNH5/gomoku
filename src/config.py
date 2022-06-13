import json

_SAVE_PATH = "../res/data/config.json"  # 设置保存的路径
LAST_GAME_PATH = "../res/data/last_game.json"  # 上一次游戏的保存路径
DEFAULT_CONFIG_PATH = "../res/data/default_config.json"  # 默认设置的路径

BLACK_PIECE = "../res/image/piece_black.png"
WHITE_PIECE = "../res/image/piece_white.png"
CROSS_RESOURCE = "../res/image/cross_2.png"
HOVER_RESOURCE = "../res/image/hover.png"
ICON = "../res/image/KOR.png"
BOX_UNCHECKED_RESOURCE = "../res/image/box_unchecked_1.png"
BOX_CHECKED_RESOURCE = "../res/image/box_checked_1.png"
DISABLE_BOX_UNCHECKED_1_RESOURCE = "../res/image/box_unchecked_2.png"
DISABLE_BOX_CHECKED_1_RESOURCE = "../res/image/box_checked_2.png"
DISABLE_BOX_UNCHECKED_2_RESOURCE = "../res/image/box_unchecked_3.png"
DISABLE_BOX_CHECKED_2_RESOURCE = "../res/image/box_checked_3.png"
BOX_PLUS_RESOURCE = "../res/image/square_plus.png"
BOX_PLUS_DISABLE_RESOURCE = "../res/image/square_plus_disable.png"
BOX_MINUS_RESOURCE = "../res/image/square_minus.png"
BOX_MINUS_DISABLE_RESOURCE = "../res/image/square_minus_disable.png"
X_RESOURCE = "../res/image/x.png"
FONT_MSYH = "../res/fonts/msyh.ttc"

MIN_ROW_POINTS = 5  # 最小行数
MIN_COL_POINTS = 5  # 最小列数
MIN_REPENTANCE_TIMES = 1  # 最小悔棋次数
MAX_ROW_POINTS = 30  # 最大行数
MAX_COL_POINTS = 30  # 最大列数
MAX_REPENTANCE_TIMES = 10  # 最大悔棋次数
FPS = 30  # 帧率

# CHECKERBOARD_COLOR = (0xE3, 0x92, 0x65)  # 棋盘颜色
CHECKERBOARD_COLOR = (249, 211, 95)  # 棋盘颜色
CHECKERBOARD_BACKGROUND_COLOR = (0xF9, 0xEC, 0xAF)  # 棋盘背景颜色
DISABLE_COLOR = (0x90, 0x93, 0x99)  # 禁用时的颜色
ORANGE_COLOR1 = (0xF9, 0xCD, 0x44)
TITLE_TEXT_COLOR = (0x40, 0x9E, 0xFF)
BLACK_COLOR = (0, 0, 0)
GREY_COLOR1 = (60, 62, 66)
GREY_COLOR2 = (0x70, 0x70, 0x70)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)
WHITE_COLOR2 = (242, 246, 252)
WHITE_COLOR3 = (228, 231, 237)

repentance_times: int
row_points: int
col_points: int
forbidden_moves: bool
show_subscript: bool
ai_is_black: bool
infinity_repentance: bool
screen_width: float
screen_height: float
ai_enabled: bool
show_piece_id: bool
draw_border: bool
show_forbidden_point: bool
debug = False  # ...  -_-

time_out = 100  # AI思考超时时间


def __init__():
    global repentance_times, row_points, col_points, forbidden_moves, show_subscript, show_piece_id, ai_is_black, \
        show_forbidden_point, infinity_repentance, screen_width, screen_height, ai_enabled, draw_border

    with open(_SAVE_PATH, "r") as f:
        saved_config = json.load(f)
        repentance_times = saved_config["repentance_times"]  # 悔棋次数
        row_points = saved_config["row_points"]  # 棋盘每行点数
        col_points = saved_config["col_points"]  # 棋盘每列点数
        forbidden_moves = saved_config["forbidden_moves"]  # 是否启用禁手
        show_subscript = saved_config["show_subscript"]  # 显示行列编号
        ai_is_black = saved_config["ai_is_black"]  # AI是否先手
        infinity_repentance = saved_config["infinity_repentance"]  # 是否无限悔棋
        screen_width = saved_config["screen_width"]  # 屏幕宽度
        screen_height = saved_config["screen_height"]  # 屏幕长度
        ai_enabled = saved_config["ai_enabled"]  # 是否启用AI
        show_piece_id = saved_config["show_piece_id"]
        draw_border = saved_config["draw_border"]
        show_forbidden_point = saved_config["show_forbidden_point"]


def change_size(width, height):
    """
    修改窗口大小
    """
    global screen_width, screen_height
    screen_width, screen_height = width, height


def save():
    """
    保存到文件
    """
    with open(_SAVE_PATH, "w") as f:
        json.dump({
            "repentance_times": repentance_times,  # 悔棋次数
            "screen_width": screen_width,  # 屏幕宽度
            "screen_height": screen_height,  # 屏幕高度
            "row_points": row_points,  # 棋盘每行点数
            "col_points": col_points,  # 棋盘每列点数
            "forbidden_moves": forbidden_moves,  # 是否启用禁手
            "show_subscript": show_subscript,  # 显示行列编号
            "ai_is_black": ai_is_black,
            "ai_enabled": ai_enabled,  # 是否启用AI
            "show_piece_id": show_piece_id,  # 是否显示棋子编号
            "draw_border": draw_border,
            "show_forbidden_point": show_forbidden_point,
            "infinity_repentance": infinity_repentance,  # 是否无限悔棋
        }, f)


__init__()
