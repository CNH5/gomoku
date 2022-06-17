import pygame
import abc
from pygame import Surface


class MyScreen(metaclass=abc.ABCMeta):
    def __init__(self, screen: Surface, caption):
        self.caption = caption
        self.screen = screen

    @abc.abstractmethod
    def draw_background(self):
        """
        绘制当前画面
        """
        pygame.display.set_caption(self.caption)
        return self

    @abc.abstractmethod
    def key_down(self, key):
        """
        处理按键点击事件
        :param key: 键盘按键
        """
        return self

    @abc.abstractmethod
    def mouse_click(self, x, y, button):
        """
        处理鼠标点击事件
        :param x: 鼠标当前的x
        :param y: 鼠标当前的y
        :param button: 鼠标按键
        """
        return self

    @abc.abstractmethod
    def mouse_motion(self, x, y):
        """
        处理鼠标移动事件
        """
        return self

    @abc.abstractmethod
    def change_size(self):
        """
        处理大小改变事件
        """
        return self

    @abc.abstractmethod
    def exit(self) -> None:
        """
        点击右上角的关闭按钮之后,调用这个函数
        """
        pass
