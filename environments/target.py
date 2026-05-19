import math
from config import *
from PIL import Image, ImageDraw, ImageFont

class Target:
    def __init__(self, x=WIDTH/2, y=HEIGHT/2, angle=0.0):
        self.x = float(x)
        self.y = float(y)
        self.angle = angle

    def draw(self, canvas):
        target_w, target_h = 80, 50

        # 1. 주차선 레이어 생성
        target_layer = Image.new("RGBA", (target_w, target_h), (*BLACK, 0))
        t_draw = ImageDraw.Draw(target_layer)
        t_draw.rectangle([0, 0, target_w - 1, target_h - 1], outline=(*GREEN, 255), width=2)

        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        # 2. 'P' 글자용 별도 투명 레이어 생성
        text_layer = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_layer)
        text_draw.text((target_w / 2, target_h / 2), "P", fill=(*GREEN, 255), font=font, anchor="mm")

        # 3. 'P' 글자만 원하는 각도로 회전 (예: 90도)
        p_rotation_angle = -90  # 원하는 각도로 수정하세요
        rotated_text = text_layer.rotate(p_rotation_angle, expand=False)

        # 4. 주차선 레이어 위에 회전된 'P' 레이어 합성
        target_layer.alpha_composite(rotated_text)

        # 5. 전체 타겟(주차선+'P')을 자신의 각도(self.angle)만큼 회전 및 캔버스 합성
        rotated_target = target_layer.rotate(-math.degrees(self.angle), expand=True)
        t_offset = (int(self.x - rotated_target.width / 2), int(self.y - rotated_target.height / 2))
        canvas.paste(rotated_target, t_offset, rotated_target)


