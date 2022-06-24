import pygame

from src.ai import ai_chessman
from src.gomoku import Point
from src.surface.button import MyButton
from src.gomoku import game
from src import config as CONFIG
from src.main import hover_img, cross_img, x_img, box_checked_img, box_unchecked_img, \
    disable_box_checked_1_img, disable_box_unchecked_1_img
from src.surface.screen import MyScreen

from src.surface.game_screen import config as gs_conf
import src.surface.config_screen.screen as cs

# 天元和星的位置
stars = ((3, 3), (3, 11), (7, 7), (11, 3), (11, 11))


def get_mouse_point(mouse_x, mouse_y) -> Point:
    # 获取屏幕上x, y对应的棋盘坐标
    x = int((mouse_x - gs_conf.row_border + gs_conf.size / 2) // gs_conf.size)
    y = int((mouse_y - gs_conf.col_border + gs_conf.size / 2) // gs_conf.size)
    return Point(x, y)


def get_center_coordinate(point) -> (float, float):
    # 获取棋盘坐标的中心对应的屏幕坐标
    return gs_conf.row_border + gs_conf.size * point.X, gs_conf.col_border + gs_conf.size * point.Y


def mouse_chessman():
    if CONFIG.ai_enabled:
        return game.WHITE_CHESSMAN if CONFIG.ai_is_black else game.BLACK_CHESSMAN
    else:
        return game.now_chessman()


class GameScreen(MyScreen):
    # 游戏界面
    _restart_bt: MyButton  # 重开按钮
    _repentance_bt: MyButton  # 悔棋按钮
    _config_bt: MyButton  # 设置按钮
    _enable_forbidden_cb: MyButton  # 启用禁手checkbox
    _enable_ai_cb: MyButton  # 启用AI checkbox
    _ai_first_cb: MyButton  # AI先手checkbox
    _ai_think_bt: MyButton  # AI计算按钮,测试用的
    _hover_point: Point = None  # 鼠标所在的棋盘坐标

    def __init__(self, screen):
        super().__init__(screen, "五子棋")
        self.mark = cross_img  # 需要绘制的标志

        gs_conf.init_location(game.row, game.col)
        self.__re_init_buttons()

        if game.winner is not None:
            if game.forbidden_win:
                self.mark = x_img
            self._other_points = game.win_points  # 需要绘制十字的坐标
        else:
            self._other_points = [game.last_chessman().last_point()]

        if game.start:
            # 游戏已经开始了，行数和列数可能不太一样，要重新设置
            gs_conf.init_location(game.row, game.col)

        if not game.is_player_now():
            ai_chessman.get_point(call_back=self.set_other_point)

    def __reset_game(self):
        gs_conf.init_location(CONFIG.row_points, CONFIG.col_points)
        self.__re_init_buttons()
        game.reset()

    def __restart(self):
        """
        重新开始
        """
        ai_place = not (game.start and ai_chessman.thinking)
        if ai_chessman.thinking:
            ai_chessman.stop_thinking()
        self.__reset_game()
        self._other_points = []
        self.mark = cross_img
        if CONFIG.ai_enabled and CONFIG.ai_is_black and ai_place:
            # AI落子
            ai_chessman.get_point(call_back=self.set_other_point)

    def set_other_point(self, placed_point: Point):
        if game.start:
            if len(game.win_points) == 0:
                self._other_points = [placed_point]
            else:
                self._other_points = game.win_points

    def __draw_checkerboard(self):
        """
        绘制棋盘
        """
        if not game.start and (game.row != CONFIG.row_points or game.col != CONFIG.col_points):
            self.__reset_game()

        self.screen.fill(CONFIG.CHECKERBOARD_BACKGROUND_COLOR)
        background = pygame.Surface(
            (gs_conf.checkerboard_edge_width, gs_conf.checkerboard_edge_height),
            flags=pygame.HWSURFACE)
        background.fill(CONFIG.CHECKERBOARD_COLOR)
        rect = gs_conf.checkerboard_background_rect
        self.screen.blit(background, rect)

        pygame.draw.lines(self.screen, CONFIG.WHITE_COLOR, False,
                          [[rect[0], rect[1] + gs_conf.checkerboard_edge_height],
                           [rect[0], rect[1]],
                           [rect[0] + gs_conf.checkerboard_edge_width, rect[1]]],
                          gs_conf.line_width)
        pygame.draw.lines(self.screen, CONFIG.GREY_COLOR2, False,
                          [[rect[0], rect[1] + gs_conf.checkerboard_edge_height],
                           [rect[0] + gs_conf.checkerboard_edge_width, rect[1] +
                            gs_conf.checkerboard_edge_height],
                           [rect[0] + gs_conf.checkerboard_edge_width, rect[1]]],
                          gs_conf.line_width)
        # 边框
        if CONFIG.draw_border:
            pygame.draw.lines(self.screen, CONFIG.BLACK_COLOR, True,
                              [[gs_conf.row_border - gs_conf.Inside_Width,
                                gs_conf.col_border - gs_conf.Inside_Width],
                               [gs_conf.row_border - gs_conf.Inside_Width,
                                gs_conf.col_border + gs_conf.Inside_Width + gs_conf.checkerboard_height],
                               [gs_conf.row_border + gs_conf.Inside_Width + gs_conf.checkerboard_width,
                                gs_conf.col_border + gs_conf.Inside_Width + gs_conf.checkerboard_height],
                               [gs_conf.row_border + gs_conf.Inside_Width + gs_conf.checkerboard_width,
                                gs_conf.col_border - gs_conf.Inside_Width]],
                              gs_conf.Border_Width)
        # 画列
        for i in range(game.row):
            x = gs_conf.row_border + gs_conf.size * i
            pygame.draw.line(self.screen, CONFIG.BLACK_COLOR, [x, gs_conf.col_border],
                             [x, gs_conf.col_border + gs_conf.checkerboard_height], gs_conf.line_width)
        # 画行
        for i in range(game.col):
            y = gs_conf.col_border + gs_conf.size * i
            pygame.draw.line(self.screen, CONFIG.BLACK_COLOR, [gs_conf.row_border, y],
                             [gs_conf.row_border + gs_conf.checkerboard_width, y], gs_conf.line_width)

    def __draw_frame(self, surface, point, dx: float = 0, dy: float = 0):
        """
        在坐标点上绘制单个元素
        """
        x, y = get_center_coordinate(point)
        rect = surface.get_rect()
        rect.center = (x + dx, y + dy)
        self.screen.blit(surface, rect)

    def __draw_pieces(self):
        """
        绘制棋子
        """
        font = pygame.font.Font(CONFIG.FONT_MSYH, gs_conf.id_text_size)

        def draw_piece(chessman, is_black, text_color) -> None:
            """
            绘制棋子
            :param chessman: 棋手
            :param is_black: 是否是黑色方
            :param text_color: 棋子ｉｄ的颜色
            """
            # 转换大小
            piece_res = pygame.transform.smoothscale(chessman.piece_res(), (gs_conf.piece_size, gs_conf.piece_size))
            records = chessman.records()
            for i in range(len(records)):
                point = records[i]
                self.__draw_frame(piece_res, point)
                if CONFIG.show_piece_id:
                    piece_id = str(i * 2 + 1) if is_black else str((i + 1) * 2)
                    if game.is_black_now() ^ is_black:
                        if self._other_points.__contains__(point):  # 特殊标记的点
                            text = font.render(piece_id, True, CONFIG.RED_COLOR)
                        else:
                            text = font.render(piece_id, True, text_color)
                    else:
                        text = font.render(piece_id, True, text_color)
                    self.__draw_frame(text, point)

        draw_piece(game.BLACK_CHESSMAN, True, CONFIG.WHITE_COLOR)
        draw_piece(game.WHITE_CHESSMAN, False, CONFIG.BLACK_COLOR)

    def __draw_mark(self):
        """
        绘制上一个落点和鼠标准心的标志
        """
        if not CONFIG.show_piece_id:
            # 绘制十字准心或者禁手的x
            if game.winner is None:
                mark = pygame.transform.smoothscale(cross_img, (gs_conf.cross_size, gs_conf.cross_size))
            else:
                # 出现禁手或者有获胜者了
                mark = pygame.transform.smoothscale(self.mark, (gs_conf.x_size, gs_conf.x_size))

            for point in self._other_points:
                self.__draw_frame(mark, point)

        if CONFIG.show_forbidden_point and game.forbidden_moves and (game.winner is None) and game.is_black_now():
            mark = pygame.transform.smoothscale(x_img, (gs_conf.x_size, gs_conf.x_size))
            for p in game.checkerboard.forbidden_points():
                self.__draw_frame(mark, p)

        if self._hover_point is not None and game.can_place(self._hover_point):
            hover = pygame.transform.smoothscale(hover_img, (gs_conf.piece_size, gs_conf.piece_size))
            self.__draw_frame(hover, self._hover_point)

    def __draw_standard_elements(self):
        """
        就是天元、星和坐标轴
        """
        if game.col == game.row == 15:
            for x, y in stars:
                # 画天元和星
                pygame.draw.circle(self.screen, CONFIG.BLACK_COLOR,
                                   [gs_conf.row_border + gs_conf.size * x,
                                    gs_conf.col_border + gs_conf.size * y], 3)
            if CONFIG.show_subscript:
                # 绘制行列标
                f_msyh = pygame.font.Font(CONFIG.FONT_MSYH, gs_conf.subscript_size)

                for i in range(15):
                    text = f_msyh.render(str(i + 1), True, CONFIG.BLACK_COLOR)
                    self.__draw_frame(text, Point(-1, 14 - i), dx=gs_conf.size * 0.1)
                    text = f_msyh.render(chr(ord("A") + i), True, CONFIG.BLACK_COLOR)
                    self.__draw_frame(text, Point(i, 15), dy=-gs_conf.size * 0.2)

    def __draw_info(self):
        """
        绘制文本
        """
        now_chessman = game.now_chessman()
        font = pygame.font.Font(CONFIG.FONT_MSYH, gs_conf.info_size)
        if game.winner is None:  # 没有胜者
            if game.is_draw():
                text = font.render("和棋!", True, CONFIG.BLACK_COLOR)
            elif not game.is_player_now() and game.start and ai_chessman.thinking:
                text = font.render("AI思考中..", True, CONFIG.BLACK_COLOR)
            else:
                text = font.render(f"当前棋手: {now_chessman.name}", True, CONFIG.BLACK_COLOR)
        else:
            text = font.render(f"{game.winner.name} 获胜!", True, CONFIG.RED_COLOR)

        self.__draw_frame(text, Point(game.row + 2, 1), dx=gs_conf.size * 0.3)

        if game.is_player_now() and not game.infinity_repentance and now_chessman.len_records():
            # 能不显示的时候就不显示，东西太多显得杂乱
            text = font.render(f"剩余悔棋次数: {now_chessman.repentance_times}", True, CONFIG.BLACK_COLOR)
            self.__draw_frame(text, Point(game.row + 2, 2), dx=gs_conf.size * 0.4, dy=gs_conf.size * 0.3)

        font = pygame.font.Font(CONFIG.FONT_MSYH, gs_conf.box_text_size)
        # checkbox的文本
        self.screen.blit(
            font.render(gs_conf.enable_forbidden_cb_text, True, CONFIG.BLACK_COLOR),
            (gs_conf.x_button + gs_conf.box_size + gs_conf.box_text_border, gs_conf.y_forbidden_bt - 4))
        self.screen.blit(
            font.render(gs_conf.enable_ai_cb_text, True, CONFIG.BLACK_COLOR),
            (gs_conf.x_button + gs_conf.box_size + gs_conf.box_text_border, gs_conf.y_enable_ai_bt - 4))
        self.screen.blit(
            font.render(gs_conf.ai_first_cb_text, True, CONFIG.BLACK_COLOR),
            (gs_conf.x_button + gs_conf.box_size + gs_conf.box_text_border, gs_conf.y_ai_first_bt - 4))

    def draw_background(self):
        super().draw_background()
        self.__draw_checkerboard()
        self.__draw_info()
        self.__init_buttons()
        self.__draw_buttons()
        self.__draw_standard_elements()
        self.__draw_pieces()
        self.__draw_mark()
        return self

    def key_down(self, key):
        return self

    def __place_piece(self, point):
        """
        放置棋子
        """
        game.place(point, mouse_chessman())
        if game.forbidden_win:  # 因为禁手获胜，改变标记为x
            self.mark = x_img
        self.set_other_point(point)

        if CONFIG.ai_enabled and game.winner is None:
            # 没有胜者之后轮到AI落子
            ai_chessman.get_point(call_back=self.set_other_point)

    def mouse_click(self, x, y, button):
        if button == 1:
            # 鼠标左键
            point = get_mouse_point(x, y)
            if game.can_place(point) and game.is_player_now():
                # 点击棋盘
                self.__place_piece(point)
            elif self.restart_bt.in_area(x, y):
                # 开始游戏按钮
                self.__restart()
            elif self._repentance_bt.in_area(x, y):
                # 悔棋按钮
                self.set_other_point(game.repentance(game.now_chessman()))
            elif self._config_bt.in_area(x, y):
                # 设置按钮
                return cs.ConfigScreen(self.screen)
            elif self._enable_forbidden_cb.in_area(x, y):
                # 是否启用禁手checkbox
                game.forbidden_moves = CONFIG.forbidden_moves = not CONFIG.forbidden_moves
            elif self._enable_ai_cb.in_area(x, y):
                # 人机对战checkbox
                CONFIG.ai_enabled = not CONFIG.ai_enabled
            elif self._ai_first_cb.in_area(x, y):
                # ai先手checkbox
                CONFIG.ai_is_black = not CONFIG.ai_is_black
            if self._ai_think_bt.in_area(x, y) and CONFIG.debug:
                # 测试用的...迟早要把这玩意删掉
                ai_chessman.get_point(call_back=self.set_other_point)
                # print("VCF: " + str(vcf(game.checkerboard, game.is_black_now(game.checkerboard))))
                # print("VCT: " + str(vct(game.checkerboard, game.is_black_now(game.checkerboard))))
        return self

    def mouse_motion(self, x, y):
        self._hover_point = get_mouse_point(x, y)
        return self

    def __init_buttons(self):
        """
        初始化按钮的属性
        """
        box_checked = pygame.transform.smoothscale(box_checked_img, (gs_conf.box_size, gs_conf.box_size))
        box_unchecked = pygame.transform.smoothscale(box_unchecked_img, (gs_conf.box_size, gs_conf.box_size))
        disable_box_checked = pygame.transform.smoothscale(
            disable_box_checked_1_img,
            (gs_conf.box_size, gs_conf.box_size)
        )
        disable_box_unchecked = pygame.transform.smoothscale(
            disable_box_unchecked_1_img,
            (gs_conf.box_size, gs_conf.box_size)
        )
        self.restart_bt.draw(self.screen)
        if mouse_chessman().can_repentance() and game.is_player_now() and not game.is_draw():
            self._repentance_bt.set_text("悔棋", text_size=gs_conf.button_text_size, text_color=CONFIG.BLACK_COLOR)
            self._repentance_bt.set_background_color(background_color=CONFIG.CHECKERBOARD_COLOR,
                                                     hover_background_color=CONFIG.ORANGE_COLOR1)
            self._repentance_bt.is_active = True
        else:
            self._repentance_bt.set_text("悔棋", text_size=gs_conf.button_text_size, text_color=CONFIG.DISABLE_COLOR)
            self._repentance_bt.set_background_color(background_color=CONFIG.CHECKERBOARD_BACKGROUND_COLOR,
                                                     hover_background_color=CONFIG.CHECKERBOARD_BACKGROUND_COLOR)
            self._repentance_bt.is_active = False

        self._enable_forbidden_cb.set_background(box_checked if CONFIG.forbidden_moves else box_unchecked)
        if game.start:
            # 游戏开始，设置部分按钮不能点击，修改部分文字
            self.restart_bt.set_text("重来", text_size=gs_conf.button_text_size)
            self._enable_forbidden_cb.is_active = False
            self._ai_first_cb.is_active = False
            self._enable_ai_cb.is_active = False
        else:
            self.restart_bt.set_text("开始", text_size=gs_conf.button_text_size)
            self._enable_forbidden_cb.is_active = True
            self._ai_first_cb.is_active = True
            self._enable_ai_cb.is_active = True

        if CONFIG.ai_enabled:
            self._enable_ai_cb.set_background(box_checked)
            self._ai_first_cb.set_background(box_checked if CONFIG.ai_is_black else box_unchecked)
        else:
            self._enable_ai_cb.set_background(box_unchecked)
            self._ai_first_cb.is_active = False
            self._ai_first_cb.set_background(disable_box_checked if CONFIG.ai_is_black else disable_box_unchecked)

    def __draw_buttons(self):
        """
        绘制按钮
        """
        self._repentance_bt.draw(self.screen)
        self._config_bt.draw(self.screen)
        self._enable_forbidden_cb.draw(self.screen)
        self._enable_ai_cb.draw(self.screen)
        self._ai_first_cb.draw(self.screen)

        if CONFIG.debug:
            self._ai_think_bt.draw(self.screen)

    def __re_init_buttons(self):
        """
        重置按钮
        """
        self._enable_forbidden_cb = MyButton(
            rect=pygame.Rect(gs_conf.x_button, gs_conf.y_forbidden_bt, gs_conf.box_size, gs_conf.box_size),
            text="",
            text_size=0,
            border_width=0)
        self._enable_ai_cb = MyButton(
            rect=pygame.Rect(gs_conf.x_button, gs_conf.y_enable_ai_bt, gs_conf.box_size, gs_conf.box_size),
            text="",
            text_size=0,
            border_width=0)
        self._ai_first_cb = MyButton(
            rect=pygame.Rect(gs_conf.x_button, gs_conf.y_ai_first_bt, gs_conf.box_size, gs_conf.box_size),
            text="",
            text_size=0,
            border_width=0)
        self.restart_bt = MyButton(
            rect=pygame.Rect(gs_conf.x_button, gs_conf.y_restart_bt, gs_conf.button_width, gs_conf.button_height),
            text="开始",
            text_size=gs_conf.button_text_size,
            background_color=CONFIG.CHECKERBOARD_COLOR,
            hover_background_color=CONFIG.ORANGE_COLOR1,
            border_color=CONFIG.GREY_COLOR2,
            hover_border_color=CONFIG.GREY_COLOR2)
        self._repentance_bt = MyButton(
            rect=pygame.Rect(gs_conf.x_button, gs_conf.y_repentance_bt, gs_conf.button_width, gs_conf.button_height),
            text="悔棋",
            text_size=gs_conf.button_text_size,
            border_color=CONFIG.GREY_COLOR2,
            hover_border_color=CONFIG.GREY_COLOR2, border_width=1)
        self._config_bt = MyButton(
            rect=pygame.Rect(gs_conf.x_button, gs_conf.y_config_bt, gs_conf.button_width, gs_conf.button_height),
            text="设置",
            text_size=gs_conf.button_text_size,
            background_color=CONFIG.CHECKERBOARD_COLOR,
            hover_background_color=CONFIG.ORANGE_COLOR1,
            border_color=CONFIG.GREY_COLOR2,
            hover_border_color=CONFIG.GREY_COLOR2)
        self._ai_think_bt = MyButton(
            rect=pygame.Rect(gs_conf.x_button, gs_conf.y_restart_bt - 200, gs_conf.button_width, gs_conf.button_height),
            text="思考",
            text_size=gs_conf.button_text_size,
            background_color=CONFIG.CHECKERBOARD_COLOR,
            hover_background_color=CONFIG.ORANGE_COLOR1,
            border_color=CONFIG.GREY_COLOR2,
            hover_border_color=CONFIG.GREY_COLOR2)

    def change_size(self):
        width, height = self.screen.get_size()
        CONFIG.change_size(width, height)
        gs_conf.init_location(game.row, game.col)
        self.__re_init_buttons()
        return self

    def exit(self) -> None:
        game.save()
