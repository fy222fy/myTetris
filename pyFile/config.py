'''
配置文件，配置全局固定的参数
'''
class Config:
    def __init__(self):
        self.WINDOW_WEIGHT = 540
        self.WINDOW_HEIGHT = 670
        self.FPS = 60
        self.GAME_WEIGHT = 300
        self.GAME_HEIGHT = self.WINDOW_HEIGHT
        self.BLOCKS_NUMS_ALINE = 11
        self.GRAVITY = (0.0, -60) # 这是你空间的重力
        self.NB_Y = 200
        self.BLOCK_SIZE = self.GAME_WEIGHT / self.BLOCKS_NUMS_ALINE / 2  # 大小
        self.BLOCK_SIZE_IMAGE = self.BLOCK_SIZE + 16
        self.BLOCK_COLLTYPE = 102
        self.backgroundpic = ""
        self.backgroundmiusic = "./music/background.mp3"
        self.impact_sound = "./music/impact.wav"
        self.block_pics = []
        self.block_pics.append("./img/blue_block.png")
        self.block_pics.append("./img/green_block.png")
        self.block_pics.append("./img/orange_block.png")
        self.block_pics.append("./img/purple_block.png")
        self.block_pics.append("./img/red_block.png")
        self.block_pics.append("./img/yellow_block.png")
config = Config()