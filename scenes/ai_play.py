from config import NUMBER_TO_ACTION
from interfaces.scene import Scene

class AIPlay(Scene):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    def update(self):
        if not self.paused:
            state = self.env.get_state()
            action = self.agent.act(state, train=False)
            self.env.update(NUMBER_TO_ACTION[action])

        return self.env.get_render_data()
