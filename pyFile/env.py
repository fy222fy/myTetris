'''
环境类，指示一些基本的游戏参数（可能会动态改变）
'''
import pygame
from pyFile.config import config
from pyFile.color import *
import pymunk
import pymunk.pygame_util

class Env:
    def __init__(self):
        self.cf = config
        pygame.init()
        self.screen = None
        self.state = 'home' # 表示当前状态
        # 定义整个重力空间
        self.space = pymunk.Space()
        self.space.gravity = self.cf.GRAVITY
        # 物理和画面切换相关
        self.dt = 1.0 / self.cf.FPS
        self.physics_steps_per_frame = 1  # 每屏画面物理步数
        self.clock = pygame.time.Clock()
        self.set_window()

    def set_window(self):
        self.screen = pygame.display.set_mode((self.cf.WINDOW_WEIGHT, self.cf.WINDOW_HEIGHT), pygame.DOUBLEBUF, 32)
        self.surface = self.screen.convert_alpha()
        pygame.display.set_caption("俄罗斯方块儿")

    def update(self):
        pygame.display.flip()
        time_passed = self.clock.tick(self.cf.FPS)

    def set_background(self,path):
        self.screen.fill(WHITE) # 暂定白背景填充
        background = pygame.image.load(path)
        self.screen.blit(background,(0,0))
    def set_background_white(self):
        self.screen.fill(WHITE) # 暂定白背景填充

    def draw_button(self,buttons):
        for b in buttons:
            if b.is_show:
                self.screen.blit(b.image, b.rect)

    def draw_text(self,text,xy,color=BLACK,size=18,center=None,font_name='fangsong'):
        font = pygame.font.SysFont(font_name, size)
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if center == 'center':
            text_rect.move_ip(xy[0] - text_rect.w // 2, xy[1])
        else:
            text_rect.move_ip(xy[0], xy[1])
        # print('画文字：',text,text_rect)
        self.screen.blit(text_obj, text_rect)

    def step(self):
        self.space.step(self.dt)

env = Env()
