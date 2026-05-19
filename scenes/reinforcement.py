from interfaces.scene import Scene
from config import NUMBER_TO_ACTION

class Reinforcement(Scene):

    def __init__(self, agent):
        super().__init__()
        self.agent = agent

        self.is_learning = False
        self.episode = 0

        self.speed = 10
        self.total_reward = 0

    def update(self):

        if not self.paused:
            for _ in range(self.speed):
                cur_state = self.env.get_state()
                action = self.agent.act(cur_state, train=True)
                self.env.update(NUMBER_TO_ACTION[action])

                next_state = self.env.get_state()
                reward = self.calculate_reward(cur_state, next_state)
                done = self.env.is_finished

                self.agent.memory.append((cur_state, action, reward, next_state, done))
                self.agent.train_step()

                self.total_reward += reward
                if done:
                    self.episode += 1
                    self.total_reward = 0
                    self.agent.epsilon = max(self.agent.epsilon_min, self.agent.epsilon * self.agent.epsilon_decay)
                    self.reset()
                    break

        return self.env.draw()

    def calculate_reward(self, cur_state, next_state):
        # 시간 효율성 패널티
        reward = -0.5

        # 거리에 따른 보상 (절대 거리 + 거리 변화)
        prev_dist = cur_state[0]
        curr_dist = next_state[0]
        reward += (prev_dist - curr_dist) * 0.3
        reward += (0.2 - curr_dist) * 0.3

        # 방향에 따른 보상 (방향이 주차창을 향할 때 보상)
        reward += (1 - abs(next_state[1])) * 0.3

        # 주차 정확성에 따른 보상
        if self.env.parking_time >= 0.01:
            reward += self.env.parking_accuracy * 1.5
            reward += (1 - abs(next_state[2])) * 1.0

        if self.env.is_finished:
            if self.env.finish_type == "SUCCESS":
                reward += 300
            elif self.env.finish_type == "TIME_OVER":
                reward -= 100
            elif self.env.finish_type == "COLLISION":
                reward -= 100

        return reward