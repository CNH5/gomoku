import json

from src import config as CONFIG

box_size: float  # 选中框大小
button_width: float  # 按钮宽度
button_height: float  # 按钮高度
button_text_size: int  # 按钮文字大小
input_box_width: float  # 输入框宽度
input_box_height: float  # 输入框高度
x_input_box: float  # 所有的选项的左边距
y_repentance_times: float  # 修改悔棋次数的区域的y
plus_minus_bt_size: float  # 加减按钮的大小
y_game_config_title: float
x_text_left: float
y_infinity_repentance: float
y_show_coordinate: float
x_checkbox: float
y_show_piece_id: float
y_show_config_title: float
title_text_size: int

y_row_num: float
y_col_num: float
x_plus: float
x_minus: float
y_show_border: float
y_show_forbidden_point: float
y_reset_bt: float

x_reset_bt: float
x_back_bt: float

box_text_size: int  # checkbox文字的大小
input_text_size: int  # 输入框的文字大小
row_points: int  # 每行有多少格
col_points: int  # 每列有多少格
infinity_repentance: bool  # 是否无限悔棋
repentance_times: int  # 悔棋次数

show_subscript: bool
show_piece_id: bool
draw_border: bool
show_forbidden_point: bool


def init_location():
    global box_size, button_width, button_height, button_text_size, plus_minus_bt_size, input_text_size, \
        infinity_repentance, input_box_height, input_box_width, x_checkbox, x_minus, x_plus, x_input_box, x_text_left, \
        x_back_bt, x_reset_bt, box_text_size, title_text_size, y_reset_bt, y_infinity_repentance, y_repentance_times, \
        y_show_config_title, y_game_config_title, y_show_forbidden_point, y_col_num, y_row_num, y_show_piece_id, \
        y_show_coordinate, y_show_border

    width, height = CONFIG.screen_width, CONFIG.screen_height
    box_size = min(width * 0.04, height * 0.04)
    button_height = box_size * 1.5
    button_width = button_height * 25 / 9
    plus_minus_bt_size = box_size

    input_box_height = box_size * 1.1
    input_box_width = input_box_height * 5 / 3
    x_checkbox = width * 0.75

    x_plus = x_checkbox
    x_minus = x_plus - box_size * 1.2
    x_input_box = x_minus - box_size * 0.2 - input_box_width
    x_text_left = width * 0.2

    x_back_bt = (width - button_width) / 2 + button_width * 0.8
    x_reset_bt = (width - button_width) / 2 - button_width * 1.3

    box_text_size = int(box_size * 0.8)
    button_text_size = int(box_text_size * 0.7)
    input_text_size = int(box_text_size * 0.8)
    title_text_size = int(box_text_size * 0.9)

    row_height = input_box_height * 1.3

    y_game_config_title = height * 0.1
    y_row_num = y_game_config_title + row_height
    y_col_num = y_row_num + row_height
    y_infinity_repentance = y_col_num + row_height
    y_repentance_times = y_infinity_repentance + row_height

    y_show_config_title = y_repentance_times + row_height + 10
    y_show_coordinate = y_show_config_title + row_height
    y_show_piece_id = y_show_coordinate + row_height
    y_show_forbidden_point = y_show_piece_id + row_height
    y_show_border = y_show_forbidden_point + row_height
    y_reset_bt = y_show_border + row_height * 2.5


def __init__():
    global row_points, col_points, show_subscript, show_subscript, show_piece_id, \
        show_forbidden_point, draw_border, infinity_repentance, repentance_times
    row_points = CONFIG.row_points
    col_points = CONFIG.col_points
    show_subscript = CONFIG.show_subscript
    show_forbidden_point = CONFIG.show_forbidden_point
    show_piece_id = CONFIG.show_piece_id
    draw_border = CONFIG.draw_border
    infinity_repentance = CONFIG.infinity_repentance
    repentance_times = CONFIG.repentance_times
    init_location()


__init__()


def set_row_points(num: int):
    global row_points
    row_points = num


def set_col_points(num: int):
    global col_points
    col_points = num


def set_repentance_times(num: int):
    global repentance_times
    repentance_times = num


def save():
    CONFIG.row_points = row_points
    CONFIG.col_points = col_points
    CONFIG.show_subscript = show_subscript
    CONFIG.show_forbidden_point = show_forbidden_point
    CONFIG.show_piece_id = show_piece_id
    CONFIG.draw_border = draw_border
    CONFIG.infinity_repentance = infinity_repentance
    CONFIG.repentance_times = repentance_times


def change_size(width, height):
    CONFIG.change_size(width, height)
    init_location()


def reset():
    """
    重置设置界面的值
    """
    global repentance_times, row_points, col_points, show_subscript, show_piece_id, \
        show_forbidden_point, draw_border, infinity_repentance

    with open(CONFIG.DEFAULT_CONFIG_PATH) as f:
        default = json.load(f)
        repentance_times = default["repentance_times"]
        row_points = default["row_points"]
        col_points = default["col_points"]
        show_subscript = default["show_subscript"]
        show_piece_id = default["show_piece_id"]
        draw_border = default["draw_border"]
        show_forbidden_point = default["show_forbidden_point"]
        infinity_repentance = default["infinity_repentance"]
