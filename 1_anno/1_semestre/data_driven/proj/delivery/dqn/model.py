import random
import numpy as np
from collections import deque

from torch.nn import Module
from torch.nn import Conv2d
from torch.nn import Linear
from torch.nn import MaxPool2d
from torch.nn import ReLU
from torch.nn import LogSoftmax
from torch import flatten


class DNN:
    def __init__(self, frame_stack_num) -> None:
        # NN architecture is the same as LeNet
        self.conv1 = Conv2d(in_channels=frame_stack_num, # Those are not RGB, but the history of the state
                            out_channels=6,
                            kernel_size=7,
                            stride=3)
        self.relu1 = ReLU()
        self.maxpool1 = MaxPool2d(kernel_size=2)

        self.conv2 = Conv2d(in_channels=6,
                            out_channels=12,
                            kernel_size=4)
        self.relu2 = ReLu()
        self.maxpool2 = MaxPool2d(kernel_size=2)

        self.fc1 = Linear(in_features=216,
                          out_features=216)
        self.relu3 = ReLu()

        self.fc2 = Linear(in_features=216,
                          out_features=len(self.action_space)
                          )
        self.logSoftmax = LogSoftmax(dim=1)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)

        x = self.conv2(x)
        x = self.relu2(x)
        x = self.maxpool2(x)

        x = flatten(x, 1)
        x = self.fc1(x)
        x = self.relu3(x)

        x = self.fc2(x)
        output = self.logSoftmax(x)

        return output


class DQNCarRacngAgent:
    def __init__(self):
        # Data structures parameters
        self.frame_stack_num = 3
        # action: (steering, acceleration, breaking)
        self.action_space = [
            (-1, None, None), # left
            ( 0, None, None), # straight
            ( 1, None, None)  # right
        ]

        # Qlearning parameters
        self.gamma = 0.95
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_decay = 1
        self.learning_rate = 0.01

        # DQN settings
        self.model = DNN(self.frame_stack_num)
        self.target_model = DNN(self.frame_stack_num)


