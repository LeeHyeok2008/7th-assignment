import numpy as np
from abc import ABC, abstractmethod
from environments.game_environment import GameEnvironment

class Scene(ABC):
    def __init__(self):
        self.paused = False
        self.env = GameEnvironment()

    @abstractmethod
    def update(self) -> dict:
        pass

    def toggle_pause(self):
        self.paused = not self.paused
        return "일시정지 중" if self.paused else "게임 진행 중"

    def reset(self):
        self.env = GameEnvironment()

