import io
import math
import random
import numpy as np
from config import *
from PIL import Image
from environments.player import Player
from environments.target import Target

class GameEnvironment:
    def __init__(self):
        self.player = Player()
        self.target = Target()

        self.reset_target()

        self.is_finished = False
        self.finish_type = "None"
        self.elapsed_time = 0.0
        self.time_limit = 15.0

        self.parking_accuracy = 0.0
        self.parking_limit = 0.7
        self.parking_time = 0.0
        self.parking_finish_time = 3.0

    def reset_target(self):
        margin = 100
        self.target = Target(
            x=random.uniform(margin, WIDTH - margin),
            y=random.uniform(margin, HEIGHT - margin),
            angle=random.uniform(-math.pi, math.pi)
        )

        self.player = Player(
            x=random.uniform(margin, WIDTH - margin),
            y=random.uniform(margin, HEIGHT - margin),
            angle=random.uniform(-math.pi, math.pi),
        )

    def get_accuracy(self):
        dist_weight = 0.8
        angle_weight = 0.2

        dist = math.sqrt((self.target.x - self.player.x) ** 2 + (self.target.y - self.player.y) ** 2)
        dist_score = max(0.0, 1.0 - dist / 50.0)
        angle_diff = abs((self.target.angle - self.player.angle + math.pi) % (2 * math.pi) - math.pi)
        angle_score = max(0.0, 1.0 - angle_diff / math.pi)

        return dist_score * dist_weight + angle_score * angle_weight

    def get_state(self):
        dx = self.target.x - self.player.x
        dy = self.target.y - self.player.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        rel_angle = (math.atan2(dy, dx) - self.player.angle + math.pi) % (2 * math.pi) - math.pi
        angle_diff = (self.target.angle - self.player.angle + math.pi) % (2 * math.pi) - math.pi
        return np.array([dist / max(WIDTH, HEIGHT), rel_angle / math.pi, angle_diff / math.pi,
                         math.sqrt(self.player.vx**2 + self.player.vy**2) / self.player.speed, self.player.ang_v / self.player.angular_speed,
                         self.player.x / max(WIDTH, HEIGHT), self.player.y / max(WIDTH, HEIGHT)])

    def update(self, action):
        if self.is_finished:
            return

        dt = 1.0 / FPS

        # 시간 업데이트
        self.elapsed_time += dt
        if self.elapsed_time >= self.time_limit:
            self.elapsed_time = self.time_limit
            self.is_finished = True
            self.finish_type = "TIME_OVER"

        # 주차 정확성 계산
        self.parking_accuracy = self.get_accuracy()
        if self.parking_accuracy >= self.parking_limit:
            self.parking_time += dt
            if self.parking_time >= self.parking_finish_time:
                self.parking_time = self.parking_finish_time
                self.is_finished = True
                self.finish_type = "SUCCESS"
        else:
            self.parking_time = 0.0

        if self.player.check_wall_collision():
            self.is_finished = True
            self.finish_type = "COLLISION"

        self.player.update(action)

    def draw(self):
        canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        self.player.draw(canvas)
        self.target.draw(canvas)

        background = Image.new("RGB", canvas.size, (255, 255, 255))
        background.paste(canvas, mask=canvas.split()[3])

        return np.array(background, dtype=np.uint8)

