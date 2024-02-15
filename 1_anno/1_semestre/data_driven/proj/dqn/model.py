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
        super(DNN, self).__init__()

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
        self.relu2 = ReLU()
        self.maxpool2 = MaxPool2d(kernel_size=2)

        self.fc1 = Linear(in_features=360,
                          out_features=216)
        self.relu3 = ReLU()

        self.fc2 = Linear(in_features=216,
                          out_features=len(action_space)
                          )
        self.softmax = Softmax()
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)

        x = self.conv2(x)
        x = self.relu2(x)
        x = self.maxpool2(x)

        dim = 0 if len(x.shape) < 4 else 1
        x = flatten(x, dim)
        x = self.fc1(x)
        x = self.relu3(x)

        x = self.fc2(x)
        output = self.softmax(x)

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
        self.memory = deque(maxlen=5000)

        # Qlearning parameters
        self.gamma = 0.95
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9999
        self.learning_rate = 0.01

        # DQN settings
        self.policy_model = DNN(self.frame_stack_num, self.action_space)
        self.target_model = DNN(self.frame_stack_num, self.action_space)

        self.loss_function = torch.nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.policy_model.parameters(), lr=self.learning_rate)

    def set_training(self):
        self.policy_model.train()
        self.target_model.train()
    
    def upate_target_model(self):
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
            target = self.policy_model(torch.from_numpy(state))
                #np.expand_dims(state, axis=0))
            if done:
                target[action_index] = reward
            else:
                t = self.target_model(torch.from_numpy(next_state))
                target[action_index] = reward + self.gamma * torch.argmax(t)
            train_state.append(state)
            train_target.append(target.detach().numpy())

        # Train the model
        self.optimizer.zero_grad()
        outputs = self.policy_model(torch.tensor(np.array(train_state)))
        loss = self.loss_function(outputs, torch.tensor(train_target))

        loss.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save_weights(self, file_path):
        torch.save(self.policy_model.state_dict(), file_path)
        self.update_target_model()
    
    def load_weights(self, file_path):
        self.policy_model.load_state_dict(torch.load(file_path))
