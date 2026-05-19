import math
from config import *
from PIL import Image, ImageDraw

class Player:
    def __init__(self, x=WIDTH/2, y=HEIGHT/2, angle=0.0, speed=100.0, angular_speed=1.92):
        self.x = float(x)
        self.y = float(y)
        self.angle = angle

        self.vx = 0.0
        self.vy = 0.0
        self.ang_v = 0.0

        self.speed = speed
        self.angular_speed = angular_speed

    def update(self, action):
        """
        Player 객체의 상태 업데이트
        action[0]: 전진/정지/후진 (-1, 0, 1)
        action[1]: 좌회전/직진/우회전 (-1, 0, 1)
        """
        dt = 1.0 / FPS

        vel_factor = -0.5 if action[0] == -1 else float(action[0])
        self.vx = vel_factor * self.speed * math.cos(self.angle)
        self.vy = vel_factor * self.speed * math.sin(self.angle)
        self.ang_v = float(action[1]) * self.angular_speed

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.angle += self.ang_v * dt

    def check_wall_collision(self):
        margin = 20
        if (self.x < margin or self.x > WIDTH - margin or
                self.y < margin or self.y > HEIGHT - margin):
            return True
        return False