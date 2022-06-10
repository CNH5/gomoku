import pygame

from src import config as CONFIG


class MyButton:
    def __init__(self, rect: pygame.Rect, text, text_size, background_color=None,
                 hover_background_color=None, border_color=None,
                 hover_border_color=None, text_color=CONFIG.BLACK_COLOR,
                 border_width=1, is_active=True):
        self.body_rect = rect
        self.border_width = border_width
        self.is_active = is_active
        self.text_color = text_color  # 按钮文字颜色
        self.border_color = border_color if border_color is not None else None  # 初始边框的颜色
        # 鼠标移动到按钮上时，边框的颜色
        self.hover_border_color = hover_border_color if hover_border_color is not None else None
        if background_color is not None:
            self.background = pygame.Surface((rect.width, rect.height), flags=pygame.HWSURFACE)
            self.background.fill(background_color)
        else:
            self.background = None
        if hover_background_color is not None:
            self.hover_background = pygame.Surface((rect.width, rect.height), flags=pygame.HWSURFACE)
            self.hover_background.fill(hover_background_color)
        else:
            self.hover_background = None
        if text == "":
            self.text = None
        else:
            self.text = pygame.font.Font(CONFIG.FONT_MSYH, text_size) \
                .render(text, True, self.text_color)

    def set_background_color(self, background_color, hover_background_color=None,
                             border_color=None, hover_border_color=None, border_width=None):
        """
        设置背景颜色
        """
        self.background = pygame.Surface(
            (self.body_rect.width, self.body_rect.height),
            flags=pygame.HWSURFACE
        )
        self.background.fill(background_color)
        if hover_border_color is not None:
            self.hover_border_color = hover_border_color
        if border_width is not None:
            self.border_width = border_width
        if border_color is not None:
            self.border_color = border_color
        if hover_background_color is not None:
            self.hover_background = pygame.Surface(
                (self.body_rect.width, self.body_rect.height),
                flags=pygame.HWSURFACE
            )
            self.hover_background.fill(hover_background_color)

    def set_background(self, background, hover_background=None, border_width=None):
        """
        设置背景surface
        """
        self.background = background
        if hover_background is not None:
            self.hover_background = hover_background
        if border_width is not None:
            self.border_width = border_width

    def set_text(self, text: str, text_size, text_color=None):
        """
        修改按钮文字
        """
        if text_color is not None:
            self.text_color = text_color
        self.text = pygame.font.Font(CONFIG.FONT_MSYH, text_size) \
            .render(text, True, self.text_color)

    def in_area(self, mouse_x, mouse_y):
        return self.body_rect.collidepoint(mouse_x, mouse_y) and self.is_active

    def __get_border(self):
        """
        获取边框四个角的坐标
        """
        return [[self.body_rect.x, self.body_rect.y],
                [self.body_rect.x + self.body_rect.width - self.border_width, self.body_rect.y],
                [self.body_rect.x + self.body_rect.width - self.border_width,
                 self.body_rect.y + self.body_rect.height - self.border_width],
                [self.body_rect.x, self.body_rect.y + self.body_rect.height - self.border_width]]

    def draw(self, surface):
        """
        在surface上绘制按钮
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.in_area(mouse_x, mouse_y) and self.hover_background is not None:
            surface.blit(self.hover_background, self.body_rect)
            if self.hover_border_color is not None and self.border_width > 0:
                pygame.draw.lines(surface, self.hover_border_color, True, self.__get_border(), self.border_width)

        elif self.background is not None:
            surface.blit(self.background, self.body_rect)
            if self.border_color is not None and self.border_width > 0:
                pygame.draw.lines(surface, self.border_color, True, self.__get_border(), self.border_width)

        if self.text is not None:
            rect = self.text.get_rect()
            rect.center = self.body_rect.center
            surface.blit(self.text, rect)
