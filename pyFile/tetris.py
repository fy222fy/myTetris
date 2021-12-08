from pyFile.env import env
from pyFile.button import Button
import logging as log
import time
import pygame
from pygame.locals import *
from pyFile.color import *
from pyFile.blocks import BlocksController
from pyFile.painter import Painter
from pyFile.music import music
import random
import pymunk
import pymunk.pygame_util
from pyFile.config import config
log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
class Tetris:
    def __init__(self):
        self.cf = config
        self.env = env
        self.painter = Painter()
        self.state = 'start' # 游戏开始啦
        self.mark = 0 # 这是你的得分
        self.level = 1 # 这是你当前的关卡数
        self.button_list = [] # 仍旧需要一些按钮
        self.music = music
        # 定义画板
        self._draw_options = pymunk.pygame_util.DrawOptions(self.env.screen)
        # 先画好游戏的边界，是刚体墙壁
        self.painter.add_static_wall()
        # 定义方块儿
        self.blc = BlocksController()

    def run(self): # 游戏开始
        self.state = "start"
        while self.env.state == "game" and self.state != "back":
            self.env.step()
            self.handle_events() # 处理当前所有发生的事件
            self.is_game_over() # 判断游戏是否结束
            # 如果当前正在下落中，并且横向速度已经小于4，并且超过了固定的bug时间
            if self.state == 'down' and self.blc.is_stop_down():
                self.state = 'new'
                self.check_is_full()
            elif self.state == 'start':
                self.start()
            elif self.state == "new":
                self.blc.create_new_blocker() # 创建新的块儿
                self.blc.gen_next_blocker()
                self.state = 'down'
            elif self.state == 'down':
                pass
            elif self.state == 'clear':
                self.clear()
            elif self.state == "over":
                self.next_level()
            elif self.state == "restart":
                self.clear_all() #清除所有块，重新开始
                self.state = "start"
            elif self.state == "wait":
                pass
            elif self.state == "back":
                self.clear_all()
                break
            else:
                log.error("unknow game state, expect 'start' or 'down' or ..., got %s" % self.env.state)

            pygame.draw.rect(self.env.screen,
                             WHITE,
                             (0, 0, self.cf.GAME_WEIGHT, self.env.screen.get_size()[1]))
            #self.env.space.debug_draw(self._draw_options)
            self.draw_others() # 画出侧边栏目
            self.painter.draw_beautiful_blocks(self.blc._blocks)  # 让块子更加美丽
            self.env.update()
        if self.state == 'back':
            self.env.state = 'home'
    def next_level(self):
        pass
    def start(self):
        self.blc.gen_next_blocker()
        self.env.set_background_white()
        # 画分割线
        self.painter.draw_split_line()
        # 写文字
        self.painter.draw_mark(self.mark,self.level)
        self.painter.draw_next_shape(self.blc.next_shape,self.blc.next_img)
        self.painter.draw_game_button()
        self.state = 'new'

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:# 按Esc则退出游戏
                self.env.state = 'exit'
            if event.type == KEYDOWN: # 如果是按下了某个按键
                if event.key == K_ESCAPE: # 如果是按下了esc
                    self.env.state = 'exit'
                if event.key in [K_LEFT, K_a] and self.blc.is_moved():# 如果是左键或a建
                    self.blc.start_move_block('left')
                if event.key in [K_RIGHT, K_d] and self.blc.is_moved():
                    self.blc.start_move_block('right')
                if event.key in [K_DOWN, K_s] and self.blc.is_moved(): # 如果是下键或者是s键
                    self.blc.start_move_block('clockwise')
                    # 旋转
                if event.key in [K_SPACE, K_UP, K_w] and self.blc.is_moved():
                    self.blc.start_move_block('counterclockwise')
                    # 旋转
            elif event.type == KEYUP: # 如果是抬起按键
                if event.key in [K_LEFT, K_a] and self.blc.is_moved():
                    self.blc.stop_move_block("left")

                if event.key in [K_RIGHT, K_d] and self.blc.is_moved():
                    self.blc.stop_move_block("right")
                if event.key in [K_SPACE, K_UP, K_w] and self.blc.is_moved():
                    self.blc.stop_move_block("clockwise")
                if event.key in [K_DOWN, K_s] and self.blc.is_moved():
                    self.blc.stop_move_block("counterclockwise")

            if event.type == MOUSEBUTTONDOWN: #如果是鼠标按键，则看看按得是哪里
                for i in self.painter.button_list:
                    if i.is_click(event.pos):
                        self.state = i.name
                        break
    def is_game_over(self):
        if self.mark > 5:
            self.state = "over"

    def check_is_full(self):
        add_mark = self.blc.check_full()
        if add_mark > 0:
            self.mark += add_mark
            self.state = "clear"

    def clear(self):
        self.blc.remove_full_blocks()
        self.state = "new"
    def clear_all(self):
        self.blc.remove_all_blocks()
        self.mark = 0
    def draw_others(self):
        self.env.set_background_white()
        self.painter.draw_mark(self.mark,self.level)
        self.painter.draw_split_line()
        self.painter.draw_next_shape(self.blc.next_shape,self.blc.next_img)
        self.painter.draw_game_button()
