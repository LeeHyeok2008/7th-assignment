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


    def draw(self, canvas):
        car_w, car_h = 80, 40
        car_layer = Image.new("RGBA", (car_w, car_h), (*BLACK, 0))
        draw = ImageDraw.Draw(car_layer)

        # 바퀴
        wheel_color = (*BLACK, 0)
        draw.rectangle([10, 0, 25, 8], fill=wheel_color)  # 앞왼
        draw.rectangle([10, 32, 25, 40], fill=wheel_color)  # 앞오
        draw.rectangle([55, 0, 70, 8], fill=wheel_color)  # 뒤왼
        draw.rectangle([55, 32, 70, 40], fill=wheel_color)  # 뒤오

        # 몸체
        draw.rounded_rectangle([5, 5, 75, 35], radius=5, fill=(*BLUE, 255))

        # 유리창 & 헤드라이트
        draw.rectangle([45, 8, 60, 32], fill=(100, 200, 255, 255))  # 유리
        draw.rectangle([72, 7, 77, 15], fill=(255, 255, 200, 255))  # 헤드라이트1
        draw.rectangle([72, 25, 77, 33], fill=(255, 255, 200, 255))  # 헤드라이트2

        # 자동차 회전
        angle_deg = math.degrees(self.angle)
        rotated_car = car_layer.rotate(-angle_deg, expand=True, resample=Image.BICUBIC)

        # 메인 캔버스에 합성
        car_offset = (int(self.x - rotated_car.width / 2), int(self.y - rotated_car.height / 2))
        canvas.paste(rotated_car, car_offset, rotated_car)


    def check_wall_collision(self):
        margin = 20
        if (self.x < margin or self.x > WIDTH - margin or
                self.y < margin or self.y > HEIGHT - margin):
            return True
        return False