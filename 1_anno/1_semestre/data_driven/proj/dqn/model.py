import random
import numpy as np
from collections import deque

from torch.nn import Module
from torch.nn import Conv2d
from torch.nn import Linear
from torch.nn import MaxPool2d
from torch.nn import ReLU
from torch.nn import Softmax
from torch import flatten
import torch


class DNN(Module):
    def __init__(self, frame_stack_num, action_space) -> None:
        super().__init__()
        # CNN output dim: (I - F +2 *P) / S] +1

        # NN architecture is the same as LeNet
        self.conv1 = Conv2d(in_channels=frame_stack_num, # Those are not RGB, but the history of the state
                            out_channels=16,
                            kernel_size=7,
                            stride=4)
        # [N, 4, 84, 84] -> [N, 16, 20, 20]

        self.conv2 = Conv2d(in_channels=16,
                            out_channels=32,
                            kernel_size=4,
                            stride=2)
        # [N, 16, 20, 20] -> [N, 32, 9, 9]

        self.in_features = 32 * 9 * 9        
        self.fc1 = Linear(in_features=self.in_features,
                          out_features=256)
        self.fc2 = Linear(in_features=256,
                          out_features=len(action_space)
                          )
        self.output_activation = ReLU()
    
    def forward(self, x):
        x = self.conv1(x)

        x = self.conv2(x)

        dim = 0 if len(x.shape) < 4 else 1
        x = flatten(x, dim)
        x = self.fc1(x)
        x = self.fc2(x)
        #output = self.output_activation(x)

        return x


class DQNCarRacngAgent:
    def __init__(self, epsilon=1):
        # Data structures parameters
        self.frame_stack_num = 3
        # action: (steering, acceleration, breaking)
        self.action_space = [
            (-1, None, None), # left
            ( 0, None, None), # straight
            ( 1, None, None)  # right
        ]
        self.memory = deque(maxlen=5000)

        # Qlearning parameters
        self.q_learning_rate = 0.01
        self.gamma = 0.95
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9999
        self.learning_rate = 0.00025

        # DQN settings
        self.policy_model = DNN(self.frame_stack_num, self.action_space)
        self.target_model = DNN(self.frame_stack_num, self.action_space)

        self.loss_function = torch.nn.CrossEntropyLoss()
        self.optimizer = torch.optim.RMSprop(self.policy_model.parameters(), lr=self.learning_rate)
        # torch.optim.Adam(self.policy_model.parameters(), lr=self.learning_rate, eps=1e-7)

    def set_training(self):
        self.policy_model.train()
        self.target_model.train()
    
    def update_target_model(self):
        self.target_model.load_state_dict(self.policy_model.state_dict())
    
    def convert_action(self, action):
        return (action[0], None, None)

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, self.action_space.index(self.convert_action(action)), reward, next_state, done))
    
    def act(self, state):
        if np.random.rand() > self.epsilon:
            act_values = self.policy_model(torch.from_numpy(state))
            action_index = torch.argmax(act_values)
        else:
            action_index = random.randrange(len(self.action_space))
        return self.action_space[action_index]

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        train_state = []
        train_target = []
        for state, action_index, reward, next_state, done in minibatch:
            target = np.zeros(len(self.action_space))
            # self.policy_model(torch.from_numpy(state))
            # Q(s,a) <- (1 - alpha) Q(s, a) + alpha * (r + gamma * max(Q(s_1, a)) )
            if done:
                target[action_index] = (1 - self.q_learning_rate) * target[action_index] + self.q_learning_rate * (reward)
            else:
                t = self.target_model(torch.from_numpy(next_state))
                target[action_index] += (1 - self.q_learning_rate) * target[action_index] + self.q_learning_rate * (reward + self.gamma * torch.amax(t))
            train_state.append(state)
            train_target.append(target)

        self.train(train_state, train_target)
    
    def train(self, train_state, train_target):
        self.optimizer.zero_grad()
        outputs = self.policy_model(torch.tensor(np.array(train_state)))
        loss = self.loss_function(outputs, torch.tensor(train_target))

        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def train_on_dataset(self, train_state, train_target):
        return self.train(train_state, train_target)
        avg_loss = 0
        # for i in range(len(train_state)):
        #     x = train_state[i]
        #     y = train_target[i]
        outputs = self.policy_model(torch.tensor(np.array(train_state)))
        loss = self.loss_function(outputs, torch.tensor(train_target))

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        avg_loss += loss.item()
        
        return avg_loss

    def save_weights(self, file_path):
        torch.save(self.policy_model.state_dict(), file_path)
        self.update_target_model()
    
    def load_weights(self, file_path):
        self.policy_model.load_state_dict(torch.load(file_path))
