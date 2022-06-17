import pygame

from src import config as CONFIG
from src.main import box_checked_img, box_unchecked_img, box_plus_img, \
    box_plus_disable_img, box_minus_img, box_minus_disable_img
from src.surface.screen import MyScreen
from src.surface.button import MyButton
from src.surface.input import MyIntInputBox
from src.surface.config_screen import config as cs_conf
import src.surface.game_screen.screen as gs


class ConfigScreen(MyScreen):
    """
    显示：
        是否显示棋盘坐标；
        是否显示棋盘外框;
        是否显示棋子的序号；
    游戏：
        修改棋盘的行、列数；
        设置是否无限悔棋；
            设置最大悔棋次数；
    """
    _show_coordinate_cb: MyButton  # 显示坐标checkbox
    _show_piece_id_cb: MyButton  # 显示棋子序号
    _show_border_cb: MyButton  # 显示棋盘周围的边框
    _show_forbidden_point_cb: MyButton  # 显示禁手点
    _infinity_repentance_cb: MyButton  # 是否无限悔棋
    _back_bt: MyButton  # 返回按钮
    _reset_bt: MyButton  # 重置按钮
    _repentance_times_plus_bt: MyButton  # 悔棋次数+1按钮
    _repentance_times_minus_bt: MyButton  # 悔棋次数-1按钮
    _row_points_plus_bt: MyButton  # 行数量+1按钮
    _row_points_minus_bt: MyButton  # 行数量-1按钮
    _col_points_plus_bt: MyButton  # 列数量+1按钮
    _col_points_minus_bt: MyButton  # 列数量-1按钮
    _repentance_times_input_box: MyIntInputBox  # 悔棋次数input_box
    _row_points_input_box: MyIntInputBox  # 行数量input_box
    _col_points_input_box: MyIntInputBox  # 列数量input_box

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, "五子棋 - 设置")
        cs_conf.__init__()
        self.__re_init_buttons()
        self.__re_init_input()

    def __re_init_input(self):
        """
        重置输入框的参数
        """
        self._row_points_input_box = MyIntInputBox(
            rect=pygame.Rect(
                cs_conf.x_input_box, cs_conf.y_row_num,
                cs_conf.input_box_width, cs_conf.input_box_height
            ),
            max_=CONFIG.MAX_ROW_POINTS, min_=CONFIG.MIN_ROW_POINTS,
            default_num=cs_conf.col_points,
            text_size=cs_conf.input_text_size,
            color_active=CONFIG.TITLE_TEXT_COLOR,
            color_inactive=CONFIG.ORANGE_COLOR1)

        self._col_points_input_box = MyIntInputBox(
            rect=pygame.Rect(
                cs_conf.x_input_box, cs_conf.y_col_num,
                cs_conf.input_box_width, cs_conf.input_box_height
            ),
            max_=CONFIG.MAX_COL_POINTS,
            min_=CONFIG.MIN_COL_POINTS,
            default_num=cs_conf.row_points,
            text_size=cs_conf.input_text_size,
            color_active=CONFIG.TITLE_TEXT_COLOR,
            color_inactive=CONFIG.ORANGE_COLOR1)

        self._repentance_times_input_box = MyIntInputBox(
            rect=pygame.Rect(
                cs_conf.x_input_box, cs_conf.y_repentance_times,
                cs_conf.input_box_width, cs_conf.input_box_height
            ),
            min_=CONFIG.MIN_REPENTANCE_TIMES,
            max_=CONFIG.MAX_REPENTANCE_TIMES,
            default_num=cs_conf.repentance_times,
            text_size=cs_conf.input_text_size,
            color_active=CONFIG.TITLE_TEXT_COLOR,
            color_inactive=CONFIG.ORANGE_COLOR1)

    def __init_input(self):
        """
        设置输入框的参数
        """
        self._repentance_times_input_box.is_active = not cs_conf.infinity_repentance
        if self._repentance_times_input_box.is_active:
            self._repentance_times_input_box.set_color(
                color_active=CONFIG.TITLE_TEXT_COLOR,
                color_inactive=CONFIG.ORANGE_COLOR1)
        else:
            self._repentance_times_input_box.set_color(
                color_active=None,
                color_inactive=CONFIG.DISABLE_COLOR)

    def __re_init_buttons(self):
        """
        重置按钮的参数
        """
        self._infinity_repentance_cb = MyButton(  # 是否无限悔棋
            rect=pygame.Rect(
                cs_conf.x_checkbox, cs_conf.y_infinity_repentance + 1,
                cs_conf.box_size, cs_conf.box_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self.show_coordinate_cb = MyButton(  # 显示棋盘坐标
            rect=pygame.Rect(
                cs_conf.x_checkbox, cs_conf.y_show_coordinate + 1,
                cs_conf.box_size, cs_conf.box_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._show_piece_id_cb = MyButton(  # 显示棋子序号
            rect=pygame.Rect(
                cs_conf.x_checkbox, cs_conf.y_show_piece_id + 1,
                cs_conf.box_size, cs_conf.box_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._show_border_cb = MyButton(  # 显示棋盘边框
            rect=pygame.Rect(
                cs_conf.x_checkbox, cs_conf.y_show_border + 1,
                cs_conf.box_size, cs_conf.box_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._show_forbidden_point_cb = MyButton(
            rect=pygame.Rect(
                cs_conf.x_checkbox, cs_conf.y_show_forbidden_point + 1,
                cs_conf.box_size, cs_conf.box_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._back_bt = MyButton(  # 返回按钮
            rect=pygame.Rect(
                cs_conf.x_back_bt, cs_conf.y_reset_bt,
                cs_conf.button_width, cs_conf.button_height
            ),
            text="返回",
            text_size=cs_conf.button_text_size,
            background_color=CONFIG.CHECKERBOARD_COLOR,
            hover_background_color=CONFIG.ORANGE_COLOR1,
            border_color=CONFIG.GREY_COLOR2,
            hover_border_color=CONFIG.GREY_COLOR2)
        self._reset_bt = MyButton(  # 重置按钮
            rect=pygame.Rect(
                cs_conf.x_reset_bt, cs_conf.y_reset_bt,
                cs_conf.button_width, cs_conf.button_height
            ),
            text="重置",
            text_size=cs_conf.button_text_size,
            background_color=CONFIG.CHECKERBOARD_COLOR,
            hover_background_color=CONFIG.ORANGE_COLOR1,
            border_color=CONFIG.GREY_COLOR2,
            hover_border_color=CONFIG.GREY_COLOR2)
        self._row_points_minus_bt = MyButton(  # 行数量-1按钮
            rect=pygame.Rect(
                cs_conf.x_minus, cs_conf.y_row_num + 1,
                cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._row_points_plus_bt = MyButton(  # 行数量+1按钮
            rect=pygame.Rect(
                cs_conf.x_plus, cs_conf.y_row_num + 1,
                cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._col_points_minus_bt = MyButton(  # 列数量-1按钮
            rect=pygame.Rect(
                cs_conf.x_minus, cs_conf.y_col_num + 1,
                cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._col_points_plus_bt = MyButton(  # 列数量+1按钮
            rect=pygame.Rect(
                cs_conf.x_plus, cs_conf.y_col_num + 1,
                cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._repentance_times_minus_bt = MyButton(  # 悔棋次数-1按钮
            rect=pygame.Rect(
                cs_conf.x_minus, cs_conf.y_repentance_times + 1,
                cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size
            ),
            text="",
            text_size=0,
            border_width=0)
        self._repentance_times_plus_bt = MyButton(  # 悔棋次数+1按钮
            rect=pygame.Rect(
                cs_conf.x_plus, cs_conf.y_repentance_times + 1,
                cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size
            ),
            text="",
            text_size=0,
            border_width=0)

    def __draw_input(self):
        """
        绘制按钮
        """
        self._row_points_input_box.draw(self.screen)
        self._col_points_input_box.draw(self.screen)
        self._repentance_times_input_box.draw(self.screen)

    def __init_buttons(self):
        """
        初始化按钮的参数
        """
        box_checked = pygame.transform.smoothscale(
            box_checked_img,
            (cs_conf.box_size, cs_conf.box_size))
        box_unchecked = pygame.transform.smoothscale(
            box_unchecked_img,
            (cs_conf.box_size, cs_conf.box_size))
        box_plus = pygame.transform.smoothscale(
            box_plus_img,
            (cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size))
        box_plus_disable = pygame.transform.smoothscale(
            box_plus_disable_img,
            (cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size))
        box_minus = pygame.transform.smoothscale(
            box_minus_img,
            (cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size))
        box_minus_disable = pygame.transform.smoothscale(
            box_minus_disable_img,
            (cs_conf.plus_minus_bt_size, cs_conf.plus_minus_bt_size))

        self.show_coordinate_cb.set_background(box_checked if cs_conf.show_subscript else box_unchecked)
        self._show_piece_id_cb.set_background(box_checked if cs_conf.show_piece_id else box_unchecked)
        self._show_border_cb.set_background(box_checked if cs_conf.draw_border else box_unchecked)
        self._show_forbidden_point_cb.set_background(box_checked if cs_conf.show_forbidden_point else box_unchecked)
        self._infinity_repentance_cb.set_background(box_checked if cs_conf.infinity_repentance else box_unchecked)

        if self._row_points_input_box.get_value() <= self._row_points_input_box.min_:
            self._row_points_minus_bt.set_background(box_minus_disable)
            self._row_points_minus_bt.is_active = False
            self._row_points_plus_bt.set_background(box_plus)
            self._row_points_plus_bt.is_active = True
        elif self._row_points_input_box.get_value() >= self._row_points_input_box.max_:
            self._row_points_plus_bt.set_background(box_plus_disable)
            self._row_points_plus_bt.is_active = False
            self._row_points_minus_bt.set_background(box_minus)
            self._row_points_minus_bt.is_active = True
        else:
            self._row_points_plus_bt.set_background(box_plus)
            self._row_points_plus_bt.is_active = True
            self._row_points_minus_bt.set_background(box_minus)
            self._row_points_minus_bt.is_active = True

        if self._col_points_input_box.get_value() <= self._col_points_input_box.min_:
            self._col_points_minus_bt.set_background(box_minus_disable)
            self._col_points_minus_bt.is_active = False
            self._col_points_plus_bt.set_background(box_plus)
            self._col_points_plus_bt.is_active = True
        elif self._col_points_input_box.get_value() >= self._col_points_input_box.max_:
            self._col_points_plus_bt.set_background(box_plus_disable)
            self._col_points_plus_bt.is_active = False
            self._col_points_minus_bt.set_background(box_minus)
            self._col_points_minus_bt.is_active = True
        else:
            self._col_points_plus_bt.set_background(box_plus)
            self._col_points_plus_bt.is_active = True
            self._col_points_minus_bt.set_background(box_minus)
            self._col_points_minus_bt.is_active = True

        if cs_conf.infinity_repentance:
            # 启用无限悔棋时，修改悔棋次数不应该有任何用处
            self._repentance_times_plus_bt.set_background(box_plus_disable)
            self._repentance_times_plus_bt.is_active = False
            self._repentance_times_minus_bt.set_background(box_minus_disable)
            self._repentance_times_minus_bt.is_active = False
        else:
            # 没有启用无限悔棋时，才可以修改悔棋次数
            if self._repentance_times_input_box.get_value() <= self._repentance_times_input_box.min_:
                self._repentance_times_minus_bt.set_background(box_minus_disable)
                self._repentance_times_minus_bt.is_active = False
            else:
                self._repentance_times_minus_bt.set_background(box_minus)
                self._repentance_times_minus_bt.is_active = True
            self._repentance_times_plus_bt.set_background(box_plus)
            self._repentance_times_plus_bt.is_active = True

    def __draw_buttons(self):
        self.show_coordinate_cb.draw(self.screen)
        self._show_piece_id_cb.draw(self.screen)
        self._back_bt.draw(self.screen)
        self._show_border_cb.draw(self.screen)
        self._row_points_plus_bt.draw(self.screen)
        self._row_points_minus_bt.draw(self.screen)
        self._col_points_plus_bt.draw(self.screen)
        self._col_points_minus_bt.draw(self.screen)
        self._infinity_repentance_cb.draw(self.screen)
        self._repentance_times_minus_bt.draw(self.screen)
        self._repentance_times_plus_bt.draw(self.screen)
        self._show_forbidden_point_cb.draw(self.screen)
        self._reset_bt.draw(self.screen)

    def __draw_info(self):
        """
        绘制按钮的说明文字
        """
        f_text = pygame.font.Font(CONFIG.FONT_MSYH, cs_conf.box_text_size)
        f_title = pygame.font.Font(CONFIG.FONT_MSYH, cs_conf.title_text_size)
        self.screen.blit(
            f_text.render("无限悔棋", True, CONFIG.BLACK_COLOR),
            (cs_conf.x_text_left, cs_conf.y_infinity_repentance)
        )
        self.screen.blit(
            f_text.render("显示坐标", True, CONFIG.BLACK_COLOR),
            (cs_conf.x_text_left, cs_conf.y_show_coordinate)
        )
        self.screen.blit(
            f_text.render("显示序号", True, CONFIG.BLACK_COLOR),
            (cs_conf.x_text_left, cs_conf.y_show_piece_id)
        )
        self.screen.blit(
            f_text.render("显示边框", True, CONFIG.BLACK_COLOR),
            (cs_conf.x_text_left, cs_conf.y_show_border)
        )
        self.screen.blit(
            f_text.render("行", True, CONFIG.BLACK_COLOR),
            (cs_conf.x_text_left, cs_conf.y_row_num)
        )
        self.screen.blit(
            f_text.render("列", True, CONFIG.BLACK_COLOR),
            (cs_conf.x_text_left, cs_conf.y_col_num)
        )
        self.screen.blit(
            f_text.render("悔棋次数", True, CONFIG.BLACK_COLOR),
            (cs_conf.x_text_left, cs_conf.y_repentance_times)
        )
        self.screen.blit(
            f_text.render("显示禁手点", True, CONFIG.BLACK_COLOR),
            (cs_conf.x_text_left, cs_conf.y_show_forbidden_point)
        )
        self.screen.blit(
            f_title.render("游戏", True, CONFIG.TITLE_TEXT_COLOR),
            (cs_conf.x_text_left, cs_conf.y_game_config_title)
        )
        self.screen.blit(
            f_title.render("显示", True, CONFIG.TITLE_TEXT_COLOR),
            (cs_conf.x_text_left, cs_conf.y_show_config_title)
        )

    def draw_background(self):
        super().draw_background()
        self.screen.fill(CONFIG.CHECKERBOARD_BACKGROUND_COLOR)
        # 绘制文本
        self.__draw_info()
        # 设置按钮参数并绘制
        self.__init_buttons()
        self.__draw_buttons()
        # 设置输入框参数并绘制
        self.__init_input()
        self.__draw_input()
        return self

    def key_down(self, key):
        self._row_points_input_box.handle_key_down(key, func=cs_conf.set_row_points)
        self._col_points_input_box.handle_key_down(key, func=cs_conf.set_col_points)
        self._repentance_times_input_box.handle_key_down(key, func=cs_conf.set_repentance_times)
        return self

    def mouse_click(self, x, y, button):
        if button == 1:
            # 鼠标左键
            if self._show_piece_id_cb.in_area(x, y):
                # 点击显示棋子坐标checkbox
                cs_conf.show_piece_id = not cs_conf.show_piece_id

            elif self.show_coordinate_cb.in_area(x, y):
                # 点击显示坐标checkbox
                cs_conf.show_subscript = not cs_conf.show_subscript

            elif self._show_border_cb.in_area(x, y):
                # 点击显示棋盘边框checkbox
                cs_conf.draw_border = not cs_conf.draw_border

            elif self._show_forbidden_point_cb.in_area(x, y):
                cs_conf.show_forbidden_point = not cs_conf.show_forbidden_point

            elif self._infinity_repentance_cb.in_area(x, y):
                # 点击无限悔棋checkbox
                cs_conf.infinity_repentance = not cs_conf.infinity_repentance

            elif self._back_bt.in_area(x, y):
                # 点击返回按钮
                cs_conf.save()
                return gs.GameScreen(self.screen)

            elif self._row_points_plus_bt.in_area(x, y):
                # 点击行数+1按钮
                cs_conf.col_points += 1
                self._row_points_input_box.set_value(cs_conf.col_points)

            elif self._row_points_minus_bt.in_area(x, y):
                # 点击行数-1按钮
                cs_conf.col_points -= 1
                self._row_points_input_box.set_value(cs_conf.col_points)

            elif self._col_points_plus_bt.in_area(x, y):
                # 点击列数+1按钮
                cs_conf.row_points += 1
                self._col_points_input_box.set_value(cs_conf.row_points)

            elif self._col_points_minus_bt.in_area(x, y):
                # 点击列数-1按钮
                cs_conf.row_points -= 1
                self._col_points_input_box.set_value(cs_conf.row_points)

            elif self._repentance_times_plus_bt.in_area(x, y):
                # 点击悔棋次数+1按钮
                cs_conf.repentance_times += 1
                self._repentance_times_input_box.set_value(cs_conf.repentance_times)

            elif self._repentance_times_minus_bt.in_area(x, y):
                # 点击悔棋次数-1按钮
                cs_conf.repentance_times -= 1
                self._repentance_times_input_box.set_value(cs_conf.repentance_times)

            elif self._reset_bt.in_area(x, y):
                # 点击重置按钮
                self.reset_config()

            # 判断行输入框
            if self._row_points_input_box.in_area(x, y):
                self._row_points_input_box.is_on_focus = True

            elif self._row_points_input_box.is_on_focus:
                self._row_points_input_box.clear_focus(func=cs_conf.set_row_points)

            # 判断列输入框
            if self._col_points_input_box.in_area(x, y):
                self._col_points_input_box.is_on_focus = True

            elif self._col_points_input_box.is_on_focus:
                self._col_points_input_box.clear_focus(func=cs_conf.set_col_points)

            # 判断悔棋次数输入框
            if self._repentance_times_input_box.in_area(x, y):
                self._repentance_times_input_box.is_on_focus = True

            elif self._col_points_input_box.is_on_focus:
                self._repentance_times_input_box.clear_focus(func=cs_conf.set_repentance_times)
        return self

    def reset_config(self):
        """
        重置设置的值
        """
        cs_conf.reset()
        self.__re_init_input()

    def mouse_motion(self, x, y):
        return self

    def change_size(self):
        width, height = self.screen.get_size()
        cs_conf.change_size(width, height)
        self.__re_init_buttons()
        self.__re_init_input()
        return self

    def exit(self) -> None:
        cs_conf.save()
        super().exit()
