from pyFile.env import env
from pyFile.button import Button
import logging as log
import pygame
from pygame.locals import *
log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
class Home:
    def __init__(self):
        self.env = env
        self.state = 'menu'
        self.button_list  = [] # 所有的按钮
    def run(self):
        while self.env.state == 'home':
            self.handle_event() # 处理当前事件
            if self.state == "wait":
                pass
            elif self.state == "menu":
                self.show_menu() # 展示菜单和提示信息
            elif self.state == 'start':
                self.env.state = 'game'
            elif self.state == 'exit':
                self.env.state = 'exit'
            else:
                log.error("unknow game state, expect 'home' or 'game' or ..., got %s" % self.state)
            self.env.update()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.env.state = 'exit'
            # 按Esc则退出游戏
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.env.state = 'exit'
            if event.type == MOUSEBUTTONDOWN:
                for i in self.button_list:
                    if i.is_click(event.pos):
                        self.state = i.name
                        break

    def show_menu(self):
        self.env.set_background("../img/background.png")
        # 画按钮
        window_w, window_h = self.env.screen.get_size()
        button_img = pygame.image.load('./img/button_start.jpg')
        x, y = (window_w - button_img.get_width()) // 2, 200
        self.env.draw_text("俄罗斯方块儿", (window_w // 2, y // 3), size=50, center='center')
        self.env.draw_text('姓名:', (window_w // 2, y // 3 + 60), size=20, center='center')
        self.env.draw_text('学号:', (window_w // 2, y // 3 + 90), size=20, center='center')
        # 开始游戏按钮
        self.button_list.append(Button('start', 'button_start.jpg', (x, y)))
        # 返回按钮
        y += button_img.get_height() + 20
        self.button_list.append(Button('back', 'button_back.jpg', (x, y)))
        # 退出按钮
        y += button_img.get_height() + 20
        self.button_list.append(Button('exit', 'button_exit.jpg', (x, y)))
        self.env.draw_button(self.button_list)
        self.state = 'wait'