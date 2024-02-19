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

import model

agent = model.DQNCarRacngAgent(epsilon=1)
agent.set_training()
agent.load_weights("weights.h5")
agent.optimizer.zero_grad()

file_names = ['dataset/dataset_batch047.pkl']
for i in range(29):
    file_names.append(f"dataset/dataset_batch{i}.pkl")

for file_name in tqdm(file_names):
    with open(file_name, 'rb') as file: 
        dataset = pickle.load(file) 

    train_state = []
    train_target = []

    for el in dataset["states"]:
        train_state.append([process_state_image(im) for im in el])

    for el in dataset["actions"]:
        steer = el[0]
        if el[0] == -1:
            state = [1, 0, 0]
        elif el[0] == 0:
            state = [0, 1, 0]
        else:
            state = [0, 0, 1]
        train_target.append(np.array(state).astype(np.float32))

    agent.optimizer = torch.optim.Adam(agent.policy_model.parameters(), 
                                    lr=agent.learning_rate, eps=1e-7)

    X_train, X_test, y_train, y_test = train_test_split(train_state, train_target, 
                                                        test_size=0.33)

    prev_loss = 0
    for epoch in tqdm(range(10)):
        train_loss = agent.train_on_dataset(X_train, y_train)
        y_pred = agent.policy_model(torch.tensor(np.array(X_test)))
        loss = agent.loss_function(y_pred, torch.tensor(y_test))
        print(loss)

        prev_loss = loss

    agent.save_weights("weights.h5")