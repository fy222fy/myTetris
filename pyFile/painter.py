'''画画用的
'''
from pyFile.env import env
from pyFile.button import Button
import logging as log
import time
import pygame
from pygame.locals import *
from pyFile.color import *
from pyFile.blocks import Blocks
import random
import math
import pymunk
import pymunk.pygame_util
from pyFile.config import config
log.basicConfig(level=log.DEBUG,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
class Painter:
    def __init__(self):
        self.env = env
        self.cf = config
        self.button_list = []

    def draw_mark(self,mark):
        size_2 = self.cf.GAME_WEIGHT // self.cf.BLOCKS_NUMS_ALINE  # 大小
        pygame.draw.rect(self.env.screen,WHITE,
                         (self.cf.GAME_WEIGHT + 1, 0, self.cf.WINDOW_WEIGHT - self.cf.GAME_WEIGHT, self.cf.NB_Y - 1))
        self.rect = pygame.draw.rect(self.env.screen, WHITE, (
        self.cf.GAME_WEIGHT, self.cf.NB_Y + 50, self.cf.WINDOW_WEIGHT - self.cf.GAME_WEIGHT, 20))
        center_x = (self.cf.GAME_WEIGHT + self.cf.WINDOW_WEIGHT) // 2

        self.env.draw_text("下一个方块:", (self.cf.GAME_WEIGHT + 10, 10), size=18)
        self.env.draw_text("得分：" + str(mark), (center_x, self.cf.NB_Y + 50), size=18, center='center')

    # TODO:主要是画一层img的图
    def draw_next_shape(self,next_shape,next_img):
        dx = 100
        size_2 = self.cf.GAME_WEIGHT // self.cf.BLOCKS_NUMS_ALINE  # 大小
        if next_shape == '.':
            pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
        elif next_shape == '+':
            pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100 - size_2, size_2, size_2))
            pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx - size_2, 100, size_2, size_2))
            pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
            pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx + size_2, 100, size_2, size_2))
            pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100 + size_2, size_2, size_2))
        elif next_shape == 'I':
            pygame.draw.rect(self.env.screen,BLACK,(self.cf.GAME_WEIGHT + dx - size_2, 100, size_2, size_2))
            pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
            pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx + size_2, 100, size_2, size_2))
    # 画按钮
    def draw_game_button(self):
        b_w = 150
        center_x = (self.cf.GAME_WEIGHT + self.cf.WINDOW_WEIGHT) // 2
        x, y = center_x - b_w // 2, self.cf.NB_Y + 150
        self.button_list.append(Button('star', 'button_again.jpg', (x, y), [b_w, -1]))
        y += b_w // 3 + 40
        self.button_list.append(Button('back', 'button_back.jpg', (x, y), [b_w, -1]))
        y += b_w // 3 + 40
        self.button_list.append(Button('exit', 'button_exit.jpg', (x, y), [b_w, -1]))
        self.env.draw_button(self.button_list)
        self.state = 'new'
    # 画墙
    def add_static_wall(self):
        static_body = self.env.space.static_body
        static_lines = [pymunk.Segment(static_body, (0.0, 0.0), (self.cf.GAME_WEIGHT, 0.0), 0.0),
                        pymunk.Segment(static_body, (0.0, 0.0), (0.0, self.cf.WINDOW_HEIGHT), 0.0),
                        pymunk.Segment(static_body, (self.cf.GAME_WEIGHT, self.cf.WINDOW_HEIGHT),
                                       (self.cf.GAME_WEIGHT, 0), 0.0)]
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.9
        self.env.space.add(static_lines)

    def draw_split_line(self):
        center_x = (self.cf.GAME_WEIGHT + self.cf.WINDOW_WEIGHT) // 2
        pygame.draw.line(self.env.screen, BLACK, (self.cf.GAME_WEIGHT, 0), (self.cf.GAME_WEIGHT, self.cf.WINDOW_HEIGHT), 1)
        pygame.draw.line(self.env.screen, BLACK, (self.cf.GAME_WEIGHT, self.cf.NB_Y), (self.cf.WINDOW_WEIGHT, self.cf.NB_Y),1)

    def draw_beautiful_blocks(self,blocks,cur_img):
        for block in blocks:
            p = self.to_pygame(block.body.position)
            angle = math.degrees(block.body.angle) # 弧度转换为角度
            temp_block = pygame.transform.rotate(cur_img,angle)
            x, y = p
            self.env.screen.blit(temp_block, (x, y))

    def to_pygame(self, p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x - 13), int(-p.y + 657)