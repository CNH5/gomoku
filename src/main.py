import multiprocessing
import sys

import pygame

import src.surface.game_screen.screen as gs

from src import config as CONFIG
from src.surface.screen import MyScreen

pygame.init()

# 加载资源
hover_img = pygame.image.load(CONFIG.HOVER_RESOURCE)
x_img = pygame.image.load(CONFIG.X_RESOURCE)
black_piece_img = pygame.image.load(CONFIG.BLACK_PIECE)
white_piece_img = pygame.image.load(CONFIG.WHITE_PIECE)
cross_img = pygame.image.load(CONFIG.CROSS_RESOURCE)
box_checked_img = pygame.image.load(CONFIG.BOX_CHECKED_RESOURCE)
box_unchecked_img = pygame.image.load(CONFIG.BOX_UNCHECKED_RESOURCE)
disable_box_checked_1_img = pygame.image.load(CONFIG.DISABLE_BOX_CHECKED_1_RESOURCE)
disable_box_unchecked_1_img = pygame.image.load(CONFIG.DISABLE_BOX_UNCHECKED_1_RESOURCE)
disable_box_checked_2_img = pygame.image.load(CONFIG.DISABLE_BOX_CHECKED_2_RESOURCE)
disable_box_unchecked_2_img = pygame.image.load(CONFIG.DISABLE_BOX_UNCHECKED_2_RESOURCE)
icon = pygame.image.load(CONFIG.ICON)
box_plus_img = pygame.image.load(CONFIG.BOX_PLUS_RESOURCE)
box_plus_disable_img = pygame.image.load(CONFIG.BOX_PLUS_DISABLE_RESOURCE)
box_minus_img = pygame.image.load(CONFIG.BOX_MINUS_RESOURCE)
box_minus_disable_img = pygame.image.load(CONFIG.BOX_MINUS_DISABLE_RESOURCE)


def handle_events(main_screen: MyScreen, event) -> MyScreen:
    """
    处理事件
    """
    if event.type == pygame.QUIT:
        # 右上角的关闭按钮
        pygame.quit()
        CONFIG.save()
        main_screen.exit()
        sys.exit()
    elif event.type == pygame.VIDEORESIZE:
        # 窗口大小改变
        return main_screen.change_size()

    elif event.type == pygame.MOUSEMOTION:
        # 鼠标移动事件
        x, y = event.pos
        return main_screen.mouse_motion(x, y)

    elif event.type == pygame.KEYDOWN:
        # 键盘按键
        return main_screen.key_down(event.key)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        # 鼠标点击事件
        x, y = event.pos
        return main_screen.mouse_click(x, y, event.button)
    else:
        return main_screen


def main():
    multiprocessing.freeze_support()

    clock = pygame.time.Clock()
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((CONFIG.screen_width, CONFIG.screen_height), flags=pygame.RESIZABLE)
    main_screen = gs.GameScreen(screen)

    while True:
        clock.tick(CONFIG.FPS)  # 设置帧数
        main_screen.draw_background()
        # event = pygame.event.wait()  # 等待事件发生
        for event in pygame.event.get():
            main_screen = handle_events(main_screen, event)
        # 更新屏幕显示
        pygame.display.update()


if __name__ == '__main__':
    main()
