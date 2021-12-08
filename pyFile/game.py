'''
游戏的根控制器，用于处理欢迎界面，以及启动俄罗斯方块
'''
import pygame, os, time
from pyFile.home import Home
from pyFile.tetris import Tetris
from pyFile.env import env
import logging as log
from pyFile.color import *
class Game:
    def __init__(self):
        self.env = env
        self.home = Home()
        self.tetris = Tetris()

    def run(self): # 开始游戏
        while self.env.state != 'exit':
            if self.env.state == 'home':
                self.home.run()
            elif self.env.state == 'game':
                self.tetris.run()
            else:
                log.error("unknow game state, expect 'home' or 'game' or ..., got %s" %self.env.state)
