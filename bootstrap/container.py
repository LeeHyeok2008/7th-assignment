import torch

from models.DQN import DQNAgent
from scenes.manual_play import ManualPlay
from scenes.ai_play import AIPlay
from scenes.reinforcement import  Reinforcement
from ui.clear_controller import ClearController
from ui.app_builder import AppBuilder

class Container:
    @staticmethod
    def build_app():
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        agent = DQNAgent(7, 9)
        agent.load()

        manual_play = ManualPlay()
        ai_play = AIPlay(agent)
        reinforcement = Reinforcement(agent)

        clear_controller = ClearController()

        builder = AppBuilder(
            manual_play=manual_play,
            ai_play=ai_play,
            reinforcement=reinforcement,
            clear_controller=clear_controller,
        )
        return builder.build()


