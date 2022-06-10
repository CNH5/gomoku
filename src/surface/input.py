import pygame

from src import config as CONFIG


class MyIntInputBox:
    def __init__(self, rect: pygame.Rect, default_num: int, text_size: int, max_: int = None, min_: int = None,
                 is_active=True, color_inactive=None, color_active=None, border_width=1, text_color=CONFIG.BLACK_COLOR):
        self.body_rect = rect
        self.text_size = text_size
        self._value = default_num
        self.is_on_focus = False
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.border_width = border_width
        self.is_active = is_active
        self.max_ = max_
        self.min_ = min_
        self.text_color = text_color

    def set_color(self, color_active, color_inactive):
        self.color_active = color_active
        self.color_inactive = color_inactive

    def set_text_color(self, text_color):
        self.text_color = text_color

    def handle_key_down(self, key, func=None):
        if self.is_on_focus:
            if pygame.K_0 <= key <= pygame.K_9:
                self._value += self._value * 10 + key - pygame.K_0 - 1
            elif key == pygame.K_BACKSPACE:
                self._value = int(self._value / 10)
            if func is not None and self.min_ < self._value < self.max_:
                func(self._value)

    def get_value(self):
        return self._value

    def set_value(self, value: int):
        self._value = value

    def in_area(self, mouse_x, mouse_y):
        return self.body_rect.collidepoint(mouse_x, mouse_y) and self.is_active

    def clear_focus(self, func=None):
        self.is_on_focus = False
        if self.min_ is not None and self._value < self.min_:
            self._value = self.min_
        elif self.max_ is not None and self._value > self.max_:
            self._value = self.max_
        if func is not None:
            func(self._value)

    def __get_border(self):
        return [[self.body_rect.x, self.body_rect.y],
                [self.body_rect.x + self.body_rect.width - self.border_width, self.body_rect.y],
                [self.body_rect.x + self.body_rect.width - self.border_width,
                 self.body_rect.y + self.body_rect.height - self.border_width],
                [self.body_rect.x, self.body_rect.y + self.body_rect.height - self.border_width]]

    def draw(self, surface):
        if self.is_on_focus and self.color_active is not None:
            pygame.draw.lines(surface, self.color_active, True, self.__get_border(), self.border_width)
        elif not self.is_on_focus and self.color_inactive is not None:
            pygame.draw.lines(surface, self.color_inactive, True, self.__get_border(), self.border_width)

        text = pygame.font.Font(CONFIG.FONT_MSYH, self.text_size) \
            .render(str(self._value), True, self.text_color)
        rect = text.get_rect()
        rect.center = self.body_rect.center
        surface.blit(text, rect)
