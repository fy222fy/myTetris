from pyFile.env import env
from pyFile.config import config
from pyFile.button import Button
from pyFile.music import music
import logging as log
import time
import pygame
from pygame.locals import *
from pyFile.color import *
import random
import pymunk
import pymunk.pygame_util
import math

class Block:#一个具体的方块儿
    def __init__(self,shape,img):
        self.shape = shape
        self.img = img
    def __del__(self):
        print("我死了")

class BlocksController:
    def __init__(self):
        self.env = env
        self.cf = config
        self._blocks = [] # 所有在场的方块儿组
        self.move_block= None  # 这表示正在掉落的方块
        self.remove_blocks = []
        self.block_n = 0
        self.next_shape = ''  # 表示下一个方块是什么形状的
        self.next_img = None # 表示下一个方块是什么颜色的图像
        self.cur_img = None
        self.cur_img = None # 表示当前方块是什么颜色的图像
        self.bug_time = None
        self.music = music
        self.block_images = []
        for item in self.cf.block_pics:
            img = pygame.image.load(item).convert_alpha()
            img = pygame.transform.scale(img,(int(self.cf.BLOCK_SIZE_IMAGE), int(self.cf.BLOCK_SIZE_IMAGE)))
            self.block_images.append(img)
        self.block_shapes = ['.', '.', '.', '.', '.', '.', '+', 'I', 'I', 'I', 'I']
        h = self.env.space.add_collision_handler(self.cf.BLOCK_COLLTYPE, self.cf.BLOCK_COLLTYPE)
        h.begin = self.collision
    def is_moved(self): # 是否有块儿正在下落
        return True if self.move_block != None else False

    def is_stop_down(self): #是否已经停止
        # if self.move_block_group == None or time.time() - self.bug_time < 1:
        #     return False
        # for block in self.move_block_group._blocks: # 如果每一个都小于4则停止
        #     if abs(block.body.velocity[1]) > 4:
        #         return False
        # return True
        return True if self.move_block and abs(self.move_block.shape.body.velocity[1]) < 4  and time.time() - self.bug_time > 1 else False

    def gen_next_blocker(self):
        self.next_shape = self.block_shapes[random.randint(0, len(self.block_shapes) - 1)]
        self.next_img = self.block_images[random.randint(0,len(self.block_images) - 1)]
    def create_new_blocker(self): # 创建一个新的俄罗斯方块儿组
        my_shape = self.next_shape  # 准备好的另一个形状
        my_img = self.next_img
        size = self.cf.BLOCK_SIZE
        #max_y = self.env.screen.get_size()[1] - size / 2
        y = size / 2
        if my_shape == '.':  # 如果形状是单个方块
            self.block_n = 1
            xy = (self.cf.GAME_WEIGHT / 2, y)
            big_block = self._new_block(xy,my_img)
            self.move_block = big_block
            self._blocks.append(big_block)
        elif my_shape == '+':  # 如果形状是连接形方块
            self.block_n = 5  # 该方块由5个子方块组成
            b1 = self._new_block((self.cf.GAME_WEIGHT / 2, y),my_img)
            b2 = self._new_block((self.cf.GAME_WEIGHT / 2 - size * 2, y - 2 * size),my_img)
            b_ = self._new_block((self.cf.GAME_WEIGHT / 2, y - 2 * size),my_img)
            b3 = b_  # 全都连在b_上
            b4 = self._new_block((self.cf.GAME_WEIGHT / 2 + size * 2, y - 2 * size),my_img)
            b5 = self._new_block((self.cf.GAME_WEIGHT / 2, y - 4 * size),my_img)
            self._set_PinJoint(b1.shape.body, b3.shape.body, 'ud')
            self._set_PinJoint(b2.shape.body, b3.shape.body, 'lr')
            self._set_PinJoint(b4.shape.body, b3.shape.body, 'rl')
            self._set_PinJoint(b5.shape.body, b3.shape.body, 'du')
            self.move_block = b_
            self._blocks.extend([b1,b2,b3,b4,b5])
        elif my_shape == '2':
            pass
        else:  # 如果是三连环
            self.block_n = 3
            b1 = self._new_block((self.cf.GAME_WEIGHT / 2 - size * 2, y),my_img)
            b_ = self._new_block((self.cf.GAME_WEIGHT / 2, y),my_img)
            b3 = self._new_block((self.cf.GAME_WEIGHT / 2 + size * 2, y),my_img)
            b2 = b_
            self._set_PinJoint(b1.shape.body, b2.shape.body, 'lr')
            self._set_PinJoint(b2.shape.body, b3.shape.body, 'lr')
            self.move_block = b_
            self._blocks.extend([b1,b2,b3])
        self.bug_time = time.time()

    def start_move_block(self,way):
        dv = 100 * self.block_n
        if way == 'left':
            b = self.move_block.shape.body
            vx, vy = b._get_velocity()
            b._set_velocity(pymunk.Vec2d(-dv, vy))  # 向左移动
        elif way == 'right':
            b = self.move_block.shape.body
            vx, vy = b._get_velocity()
            b._set_velocity(pymunk.Vec2d(dv, vy))
        elif way == 'clockwise':
            b = self.move_block.shape.body
            b._set_angular_velocity(2.0 * self.block_n ** 1.7)
        elif way == 'counterclockwise':
            b = self.move_block.shape.body
            b._set_angular_velocity(-2.0 * self.block_n ** 1.7)
        else:
            log.error("unkonw way to move the block, got %s" %way)

    def stop_move_block(self,way):
        if way == 'left' or way == "right":
            b = self.move_block.shape.body
            vx, vy = b._get_velocity()
            b._set_velocity(pymunk.Vec2d(0.0, vy))
        elif way == 'clockwise' or way == "counterclockwise":
            b = self.move_block.shape.body
            b._set_angular_velocity(0.0)
        else:
            log.error("unkonw way to move the block, got %s" % way)

    # 检测一行是否满了
    # 从下往上，设置一条横线，
    # 横线上每隔定长检测，只要都不为空就满了，条件简单点吧
    def check_full(self):
        add_mark = 0
        size = self.cf.GAME_WEIGHT / self.cf.BLOCKS_NUMS_ALINE / 2  # 大小
        self.remove_blocks = []
        for check_y in range(int(size), self.cf.WINDOW_HEIGHT, int(size * 2)):
            test_move_2 = []
            for check_x in range(int(size), self.cf.WINDOW_WEIGHT, int(size * 2)):
                for block in self._blocks:
                    b = block.shape
                    if (-4 < b.body.velocity[1] < 7 and
                            abs(b.body.position[0] - check_x) < 1.42 * size and
                            abs(b.body.position[1] - check_y) < 1.42 * size):
                        # print(check_x, check_y,b.body.position)
                        if self._point_in_body((check_x, check_y), b.body):
                            test_move_2.append(block)
            if len(test_move_2) >= self.cf.BLOCKS_NUMS_ALINE - 2:
                add_mark += 1
                self.remove_blocks.extend(test_move_2)
        return add_mark
    def remove_full_blocks(self):
        self.remove_block(self.remove_blocks)
    # 检测点是否在body内
    def _point_in_body(self, p, b):
        size = self.cf.GAME_WEIGHT / self.cf.BLOCKS_NUMS_ALINE / 2  # 大小
        o = b.angle
        while o > math.pi / 2.0:
            o -= math.pi / 2.0
        while o < 0:
            o += math.pi / 2.0
        # 坐标系原点移到方形中点
        p_x, p_y = p[0] - b.position[0], p[1] - b.position[1]
        p_r = math.sqrt(p_x ** 2 + p_y ** 2)
        p_o = math.atan2(p_y, p_x) - o
        p_x, p_y = p_r * math.sin(p_o), p_r * math.cos(p_o)
        if -size < p_x < size and -size < p_y < size:
            return True
        else:
            return False
    def _new_block(self, xy,img): # 创建一个新的方块儿
        size = self.cf.GAME_WEIGHT / self.cf.BLOCKS_NUMS_ALINE / 2  # 大小
        points = [(-size, -size), (-size, size), (size, size), (size, -size)]
        mass = 1.0
        moment = pymunk.moment_for_poly(mass, points, (0, 0))
        body = pymunk.Body(mass, moment)
        #xy = (xy[0],-xy[1])
        body.position = xy
        shape = pymunk.Poly(body, points)
        shape.friction = 1
        shape.color = RED
        shape.collision_type = self.cf.BLOCK_COLLTYPE
        self.env.space.add(body, shape)
        block = Block(shape,img)
        return block

    def _set_PinJoint(self, b1, b2, n):
        size = self.cf.GAME_WEIGHT / self.cf.BLOCKS_NUMS_ALINE / 2  # 大小
        if n == 'lr':
            pin = pymunk.PinJoint(b1, b2, (size, size / 3), (-size, size / 3))
            self.env.space.add(
                pymunk.PinJoint(b1, b2, (size, size / 3), (-size, size / 3)))
            self.env.space.add(
                pymunk.PinJoint(b1, b2, (size, -size / 3), (-size, -size / 3)))
        elif n == 'du':
            self.env.space.add(
                pymunk.PinJoint(b1, b2, (size / 3, size), (size / 3, -size)))
            self.env.space.add(
                pymunk.PinJoint(b1, b2, (-size / 3, size), (-size / 3, -size)))
        elif n == 'rl':
            self._set_PinJoint(b2, b1, 'lr')
        elif n == 'ud':
            self._set_PinJoint(b2, b1, 'du')
        else:
            print('未知的方向：', n)

    def remove_all_blocks(self):
        for i in self.env.space.constraints:
            self.env.space.remove(i)
        for block in self._blocks:
            self.env.space.remove(block.shape,block.shape.body)
        self._blocks.clear()
    def remove_block(self, remove_list):
        for block in remove_list:
            ball = block.shape
            all_pinjoints = self.env.space.constraints
            for i in all_pinjoints:
                if i._a == ball.body or i._b == ball.body:
                    self.env.space.remove(i)
            try:
                self.env.space.remove(ball, ball.body)
                self._blocks.remove(block)
            except:
                print()

    def collision(self,arbiter,space,data):#检测是否发生碰撞
        shapes = arbiter.shapes
        vx, vy = shapes[0].body._get_velocity()
        vx2, vy2 = shapes[1].body._get_velocity()
        #print("当前速度分别为%s %s %s %s",vx,vy,vx2,vy2)
        if abs(vx-vx2) > 150 or abs(vy - vy2) > 200:
            self.music.impact_sound.play()
        return True