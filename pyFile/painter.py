'''画画用的
'''
from pyFile.env import env
from pyFile.button import Button
from pyFile.music import music
import logging as log
import time
import pygame
from pygame.locals import *
from pyFile.color import *
from pyFile.blocks import BlocksController
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
        self.music = music
        self.button_list = []
        h = self.env.space.add_collision_handler(self.cf.BLOCK_COLLTYPE, self.cf.WALLSIDE_COLLTYPE)
        h.begin = self.collision_side
        h = self.env.space.add_collision_handler(self.cf.BLOCK_COLLTYPE, self.cf.WALLFLOOR_COLLTYPE)
        h.begin = self.collision_floor

    def draw_mark(self,mark,level):
        size_2 = self.cf.GAME_WEIGHT // self.cf.BLOCKS_NUMS_ALINE  # 大小
        pygame.draw.rect(self.env.screen,WHITE,
                         (self.cf.GAME_WEIGHT + 1, 0, self.cf.WINDOW_WEIGHT - self.cf.GAME_WEIGHT, self.cf.NB_Y - 1))
        self.rect = pygame.draw.rect(self.env.screen, WHITE, (
        self.cf.GAME_WEIGHT, self.cf.NB_Y + 50, self.cf.WINDOW_WEIGHT - self.cf.GAME_WEIGHT, 20))
        center_x = (self.cf.GAME_WEIGHT + self.cf.WINDOW_WEIGHT) // 2

        self.env.draw_text("下一个方块:", (self.cf.GAME_WEIGHT + 10, 30), size=18)
        self.env.draw_text("得分：" + str(mark), (center_x, self.cf.NB_Y + 30), size=18,center='center')
        self.env.draw_text("关卡：第" + str(level) + "关", (center_x, self.cf.NB_Y2 + 15), size=18,center='center')
        self.env.draw_text("←：控制方块儿向左边运动" , (center_x, self.cf.NB_Y2 + 45), size=16, center='center')
        self.env.draw_text("→：控制方块儿向右边运动", (center_x, self.cf.NB_Y2 + 70), size=16, center='center')
        self.env.draw_text("↑：控制方块儿逆时针旋转", (center_x, self.cf.NB_Y2 + 95), size=16, center='center')
        self.env.draw_text("↓：控制方块儿顺时针旋转", (center_x, self.cf.NB_Y2 + 120), size=16, center='center')
        self.env.draw_text("一行凑够9块即满足俄罗斯条件", (center_x, self.cf.NB_Y2 + 155), size=16, center='center')
        self.env.draw_text("躲避障碍物，试着获得5分吧！", (center_x, self.cf.NB_Y2 + 180), size=16,
                           center='center')
    def draw_next_shape(self,next_shape,next_img):
        dx = 100
        size_2 = self.cf.GAME_WEIGHT // self.cf.BLOCKS_NUMS_ALINE  # 大小
        if next_shape == '.':
            #pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
        elif next_shape == '+':
            #pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100 - size_2, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx, 100 - size_2, size_2, size_2))
            #pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx - size_2, 100, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx - size_2, 100, size_2, size_2))
            #pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
            #pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx + size_2, 100, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx + size_2, 100, size_2, size_2))
            #pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100 + size_2, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx, 100 + size_2, size_2, size_2))
        elif next_shape == 'I':
            #pygame.draw.rect(self.env.screen,BLACK,(self.cf.GAME_WEIGHT + dx - size_2, 100, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx - size_2, 100, size_2, size_2))
            #pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx, 100, size_2, size_2))
            #pygame.draw.rect(self.env.screen, BLACK,(self.cf.GAME_WEIGHT + dx + size_2, 100, size_2, size_2))
            self.env.screen.blit(next_img, (self.cf.GAME_WEIGHT + dx + size_2, 100, size_2, size_2))
    # 画按钮
    def draw_game_button(self):
        b_w = 150
        center_x = (self.cf.GAME_WEIGHT + self.cf.WINDOW_WEIGHT) // 2
        x, y = center_x - b_w // 2, self.cf.NB_Y + 80
        button_list = []
        button_list.append(Button('restart', self.cf.restart_button_pic, (x, y), [b_w, -1]))
        y += b_w // 3 + 20
        # self.button_list.append(Button('back', self.cf.back_button_pic, (x, y), [b_w, -1]))
        # y += b_w // 3 + 40
        button_list.append(Button('back', self.cf.back_button_pic, (x, y), [b_w, -1]))
        self.env.draw_button(button_list)
        self.state = 'new'
    # 画墙
    def add_static_wall(self):
        static_body = self.env.space.static_body
        floor = pymunk.Segment(static_body, (0.0, self.cf.WINDOW_HEIGHT), (self.cf.GAME_WEIGHT, self.cf.WINDOW_HEIGHT), 0.0)
        floor.collision_type = self.cf.WALLFLOOR_COLLTYPE
        side_left = pymunk.Segment(static_body, (0.0, 0.0), (0.0, self.cf.WINDOW_HEIGHT), 0.0)
        side_left.collision_type = self.cf.WALLSIDE_COLLTYPE
        side_right = pymunk.Segment(static_body, (self.cf.GAME_WEIGHT, 0),(self.cf.GAME_WEIGHT, self.cf.WINDOW_HEIGHT), 0.0)
        side_right.collision_type = self.cf.WALLSIDE_COLLTYPE
        for line in [floor,side_left,side_right]:
            line.elasticity = 0.95
            line.friction = 0.9
            self.env.space.add(line)

    def draw_split_line(self):
        center_x = (self.cf.GAME_WEIGHT + self.cf.WINDOW_WEIGHT) // 2
        pygame.draw.line(self.env.screen, BLACK, (self.cf.GAME_WEIGHT, 0), (self.cf.GAME_WEIGHT, self.cf.WINDOW_HEIGHT), 1)
        pygame.draw.line(self.env.screen, BLACK, (self.cf.GAME_WEIGHT, self.cf.NB_Y), (self.cf.WINDOW_WEIGHT, self.cf.NB_Y),1)
        pygame.draw.line(self.env.screen, BLACK, (self.cf.GAME_WEIGHT, self.cf.NB_Y2),
                         (self.cf.WINDOW_WEIGHT, self.cf.NB_Y2), 1)

    def draw_beautiful_blocks(self,blocks):
        for block in blocks:
            p = self.to_pygame(block.shape.body.position)
            angle = math.degrees(block.shape.body.angle) # 弧度转换为角度
            temp_block = pygame.transform.rotate(block.img,-angle)
            x, y = p
            self.env.screen.blit(temp_block, (x, y))

    def to_pygame(self, p):
        """Convert pymunk to pygame coordinates"""
        return int(p.x-self.cf.BLOCK_SIZE  ), int(p.y-self.cf.BLOCK_SIZE )

    def collision_side(self, arbiter, space, data):  # 检测是否发生碰撞
        shapes = arbiter.shapes
        vx, vy = shapes[0].body._get_velocity()
        vx2, vy2 = shapes[1].body._get_velocity()
        if abs(vx - vx2) > 50:
            self.music.impact_wall_sound.play()
        return True

    def collision_floor(self, arbiter, space, data):  # 检测是否发生碰撞
        shapes = arbiter.shapes
        vx, vy = shapes[0].body._get_velocity()
        vx2, vy2 = shapes[1].body._get_velocity()
        if abs(vy - vy2) > 50:
            self.music.impact_wall_sound.play()
        return True