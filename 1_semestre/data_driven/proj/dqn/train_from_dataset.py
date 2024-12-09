import gym
from collections import deque
from tqdm import tqdm
from common import process_state_image, generate_state_frame_stack_from_queue
import os
import numpy as np
import matplotlib.pyplot as plt
import pickle 
import torch
from sklearn.model_selection import train_test_split
import random
import matplotlib.pyplot as plt

import model

UPDATE_TARGET_MODEL_FREQUENCY = 5

agent = model.DQNCarRacngAgent(epsilon=1)
agent.set_training()
# agent.load_weights("weights.h5")
agent.optimizer.zero_grad()

file_names = []
for i in range(4,9):
    file_names.append(f"dataset/dataset_batch{i}.pkl")
# file_names.append('dataset/dataset_batch047.pkl')
#file_names.append(f"dataset/dataset_batch0.pkl")
gamma = 0.95
q_learning_rate = 0.01

e=0
for file_name in tqdm(file_names):
    with open(file_name, 'rb') as file: 
        dataset = pickle.load(file) 

    train_state = []
    train_target = []

    values, counts = np.unique(np.array([e for e in np.array(dataset)[:,1]])[:,0], return_counts=True)
    min_count = min(counts)
    p0 = int(10 * min_count / counts[0])
    p1 = int(10 * min_count / counts[1])
    p2 = int(10 * min_count / counts[2])

    # for i in range(len(dataset)):
    #     steer = steer = dataset[i][1][0]
    #     if steer == -1:
    #         action = [1, 0, 0]
    #     elif steer == 0:
    #         action = [0, 1, 0]
    #     else:
    #         action = [0, 0, 1]
    #     if action[0] == 1:
    #         if random.randint(0,9) > p0:
    #             continue        
    #     if action[1] == 1:
    #         if random.randint(0,9) > p1:
    #             continue
    #     if action[2] == 1:
    #         if random.randint(0,9) > p2:
    #             continue  
    #     train_target.append(np.array(action).astype(np.float32))
    #     train_state.append([process_state_image(im) for im in dataset[i][0]])

    agent.optimizer = torch.optim.Adam(agent.policy_model.parameters(), 
                                    lr=agent.learning_rate, eps=1e-7)

    for el in tqdm(dataset, "loading dataset"):
        # state, action, reward, next_state
        reward = el[2]
        steer = el[1][0]
        done = el[4]
        if steer == -1:
            if random.randint(0,9) > p0:
                continue        
        if steer == 0:
            if random.randint(0,9) > p1:
                continue
        if steer == 1:
            if random.randint(0,9) > p2:
                continue  

        state = torch.tensor([process_state_image(im) for im in el[0]])
        next_state = torch.tensor([process_state_image(im) for im in el[3]])
        target = agent.policy_model(state)
        action_index = steer + 1
        if done:
            target[action_index] = reward
        else:
            t = agent.target_model(next_state) # expec
            target[action_index] = reward + gamma * torch.amax(t)
            pass
        # (target[action_index] - reward - gamma * torch.amax(t))**2
        # (Learning_net(state)[action] - reward - gamma * target(state).max())**2

        # (1 - q_learning_rate) * target[action_index] + q_learning_rate * (reward + gamma * torch.amax(t))
        # reward + gamma * torch.amax(t)
        # el[2] + gamma * torch.amax(t)

        # TODO:
        # (1 - self.q_learning_rate) * target[action_index] + self.q_learning_rate * (reward + self.gamma * torch.amax(t))
        # (1 - self.q_learning_rate) * target[action_index] + self.q_learning_rate * (reward)

        train_state.append(state.detach().numpy())
        train_target.append(target.detach().numpy().astype(np.float32))

        if len(train_state) > 64:
            X_train, X_test, y_train, y_test = train_test_split(train_state, train_target, 
                                                                test_size=0.33)

            prev_loss = 0
            for epoch in range(100):
                train_loss = agent.train(X_train, y_train)
                y_pred = agent.policy_model(torch.tensor(np.array(X_test)))
                loss = agent.loss_function(y_pred, torch.tensor(y_test))
                if epoch % 10 == 0:
                    print(train_loss)
                    print(loss)

                #prev_loss = loss

                if e % UPDATE_TARGET_MODEL_FREQUENCY == 0:
                    agent.update_target_model()
                e+=1
            
            train_state = []
            train_target = []

    agent.save_weights("weights2.h5")