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

agent = model.DQNCarRacngAgent(epsilon=1)
agent.set_training()
agent.load_weights("weights.h5")
agent.optimizer.zero_grad()

file_names = []
for i in range(29):
    file_names.append(f"dataset/dataset_batch{i}.pkl")
file_names.append('dataset/dataset_batch047.pkl')

for file_name in tqdm(file_names):
    with open(file_name, 'rb') as file: 
        dataset = pickle.load(file) 

    train_state = []
    train_target = []

    values, counts = np.unique(np.array(dataset["actions"])[:, 0], return_counts=True)
    min_count = min(counts)
    p0 = int(10 * min_count / counts[0])
    p1 = int(10 * min_count / counts[1])
    p2 = int(10 * min_count / counts[2])

    for i in range(len(dataset["actions"])):
        el = dataset["actions"][i]
        steer = el[0]
        if steer == -1:
            action = [1, 0, 0]
        elif steer == 0:
            action = [0, 1, 0]
        else:
            action = [0, 0, 1]

        if action[0] == 1:
            if random.randint(0,9) > p0:
                continue        
        if action[1] == 1:
            if random.randint(0,9) > p1:
                continue
        if action[2] == 1:
            if random.randint(0,9) > p2:
                continue  
        train_target.append(np.array(action).astype(np.float32))
        train_state.append([process_state_image(im) for im in dataset["states"][i]])

    agent.optimizer = torch.optim.Adam(agent.policy_model.parameters(), 
                                    lr=agent.learning_rate, eps=1e-7)

    X_train, X_test, y_train, y_test = train_test_split(train_state, train_target, 
                                                        test_size=0.33)

    prev_loss = 0
    for epoch in tqdm(range(20)):
        train_loss = agent.train_on_dataset(X_train, y_train)
        #y_pred = agent.policy_model(torch.tensor(np.array(X_test)))
        #loss = agent.loss_function(y_pred, torch.tensor(y_test))
        print(train_loss)

        #prev_loss = loss

    agent.save_weights("weights.h5")