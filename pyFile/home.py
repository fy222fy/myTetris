from pyFile.env import env
from pyFile.button import Button
from pyFile.config import config
import logging as log
import pygame
from pygame.locals import *
log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
class Home:
    def __init__(self):
        self.env = env
        self.cf = config
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
                self.state = "menu"
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
        self.env.set_background(self.cf.menu_pic)
        # 画按钮
        button_img = pygame.image.load(self.cf.start_button_pic)
        x, y = (self.cf.WINDOW_WEIGHT - button_img.get_width()) // 2, 300
        #self.env.draw_text("俄罗斯方块儿", (window_w // 2, y // 3), size=50, center='center')
        # 开始游戏按钮
        self.button_list.append(Button('start', self.cf.start_button_pic, (x, y)))
        # 退出按钮
        y += button_img.get_height() + 20
        self.button_list.append(Button('exit', self.cf.exit_button_pic, (x, y)))
        self.env.draw_button(self.button_list)
        x2 = self.cf.NAME_WEIGHT
        y2 = self.cf.NAME_HEIGHT
        self.env.draw_text('姓名:xxx  学号：xxx ', (x2, y2), size=20, center='center')
        y2 += 30
        self.env.draw_text('姓名:xxx  学号：xxx ', (x2, y2), size=20, center='center')
        y2 += 30
        self.env.draw_text('姓名:xxx  学号：xxx ', (x2, y2), size=20, center='center')
        self.state = 'wait'