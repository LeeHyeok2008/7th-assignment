import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.fc(x)


class DQNAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = DQN(state_dim, action_dim).to(self.device)

        self.optimizer = optim.Adam(self.model.parameters(), lr=3e-4)
        self.memory = deque(maxlen=20000)
        self.batch_size = 64
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.999
        self.loss = 0

    def act(self, state, train=True):
        if train and random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        # 움직이지 않음 방지
        if not train and (random.random() < self.epsilon_min):
                return random.randint(0, self.action_dim - 1)
        state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            action = self.model(state_t).argmax().item()
            return action

    def train_step(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        s, a, r, ns, d = zip(*batch)
        s, a, r, ns, d = map(lambda x: torch.FloatTensor(np.array(x)).to(self.device), [s, a, r, ns, d])

        curr_q = self.model(s).gather(1, a.long().unsqueeze(1))
        next_q = self.model(ns).max(1)[0].unsqueeze(1)
        target_q = r.unsqueeze(1) + (self.gamma * next_q * (1 - d.unsqueeze(1)))

        loss = nn.MSELoss()(curr_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1)
        self.optimizer.step()
        self.loss = loss.item()

    def save(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_name = "model.pth"
        full_path = os.path.join(base_path, file_name)
        torch.save(self.model.state_dict(), full_path)

    def load(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_name = "model.pth"
            full_path = os.path.join(base_path, file_name)
            self.model.load_state_dict(torch.load(full_path, map_location=self.device))
            print("loaded model")
        except:
            print("model not loaded")
            pass
