from src import config as CONFIG

Border_Width = 3  # 边框宽度
line_width = 1  # 线宽度
Inside_Width = 4  # 边框跟实际的棋盘之间的间隔
size: float
row_border: float
col_border: float
subscript_size: int
info_size: int
button_text_size: int
box_text_size: int
id_text_size: int
piece_size: float  # 选中框和棋子的大小
cross_size: float  # 十字标记大小
x_size: float  # 禁手标志大小
box_size: float  # 选中框大小
config_box_size: float
button_height: float
button_width: float
button_spacing: float  # 几个按钮的纵向间距
box_spacing: float  # checkbox的纵向高度
checkerboard_width: float
checkerboard_height: float
checkerboard_edge_width: float
checkerboard_edge_height: float
x_button: float
y_config_bt: float
y_repentance_bt: float
y_restart_bt: float
y_ai_first_bt: float
y_enable_ai_bt: float
y_forbidden_bt: float
box_text_border: float
checkerboard_background_rect: tuple

enable_forbidden_cb_text = "启用禁手"
enable_ai_cb_text = "人机对战"
ai_first_cb_text = "机器先下"


def init_location(row_points, col_points):
    global size, row_border, col_border, subscript_size, info_size, button_text_size, box_text_size, id_text_size, \
        piece_size, cross_size, x_size, box_size, button_height, button_width, box_spacing, checkerboard_width, \
        checkerboard_height, checkerboard_edge_width, checkerboard_edge_height, x_button, y_config_bt, button_spacing, \
        y_repentance_bt, y_restart_bt, y_ai_first_bt, y_enable_ai_bt, y_forbidden_bt, box_text_border, \
        checkerboard_background_rect

    width, height = CONFIG.screen_width, CONFIG.screen_height
    if row_points == col_points == 15 and CONFIG.show_subscript:
        # 标准棋盘，并且启用行、列下标
        size = min(width / (row_points + 8), height / (col_points + 2))
        row_border = (width - (row_points + 6) * size) / 2 + size
        col_border = (height - (col_points + 1) * size) / 2 + size * 0.6
    else:
        size = min(width / (row_points + 7), height / (col_points + 1))
        row_border = (width - (row_points + 5) * size) / 2.2
        col_border = (height - col_points * size) / 2 + size * 0.4
    subscript_size = int(size * 0.5)  # 行列标记文字大小
    info_size = int(size * 0.6)
    button_text_size = int(info_size * 0.7)  # 按钮文字大小
    box_text_size = int(size * 0.5)  # checkbox文字的大小
    id_text_size = int(size * 0.45)
    piece_size = size * 0.85  # 选中框和棋子的大小
    cross_size = piece_size * 0.5  # 十字标记大小
    x_size = piece_size * 0.4  # 禁手标志大小
    box_size = size * 0.53  # 选中框大小
    button_height = size * 0.95
    button_width = button_height * 25 / 9

    box_spacing = size * 0.25  # checkbox的纵向高度
    checkerboard_width = size * (row_points - 1)
    checkerboard_height = size * (col_points - 1)
    checkerboard_edge_width = row_points * size
    checkerboard_edge_height = col_points * size
    x_button = row_border + size * (row_points + 2.5) - button_width / 2
    y_config_bt = (checkerboard_height - button_height + Inside_Width + col_border + Border_Width)

    button_spacing = button_height * 0.12  # 几个按钮的纵向间距
    y_repentance_bt = y_config_bt - button_height - button_spacing
    y_restart_bt = y_repentance_bt - button_height - button_spacing

    y_ai_first_bt = y_restart_bt - box_size - size
    y_enable_ai_bt = y_ai_first_bt - box_size - box_spacing
    y_forbidden_bt = y_enable_ai_bt - box_size - box_spacing
    box_text_border = box_size * 0.15

    checkerboard_background_rect = (row_border - size / 2, col_border - size / 2)
