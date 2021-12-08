import pygame
from pyFile.config import config
class Music:
    def __init__(self):
        self.cf = config
        pygame.mixer.init()
        self.background = pygame.mixer.music.load(self.cf.backgroundmiusic)

        pygame.mixer.music.play(-1)

        self.impact_sound = pygame.mixer.Sound(self.cf.impact_sound)
        self.impact_sound.set_volume(1)

music = Music()