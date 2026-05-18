import numpy as np
from PIL import Image
from config import WHITE
from interfaces.scene import Scene


class ManualPlay(Scene):
    def __init__(self):
        super().__init__()
        self.drive = 0
        self.turn = 0

    def update(self):
        if not self.paused:
            self.env.update((self.drive, self.turn))

        return self.env.draw()

    def control(self, action):
        if action == 'ArrowUp':
            self.drive = 1
        if action == 'ArrowDown':
            self.drive = -1
        if action == 'ArrowLeft':
            self.turn = -1
        if action == 'ArrowRight':
            self.turn = 1
        if action == 'STOP':
            self.drive = 0
            self.turn = 0