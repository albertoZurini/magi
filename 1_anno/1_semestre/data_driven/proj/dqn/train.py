import gym
from collections import deque
from tqdm import tqdm
from common import process_state_image, generate_state_frame_stack_from_queue
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2

import model

RENDER                        = True
STARTING_EPISODE              = 1
ENDING_EPISODE                = 100
SKIP_FRAMES                   = 3
TRAINING_BATCH_SIZE           = 64
SAVE_TRAINING_FREQUENCY       = 25
UPDATE_TARGET_MODEL_FREQUENCY = 5

if not os.path.exists("save"):
    os.mkdir("save")

#render_mode = "human" if RENDER else "rgb_array"
env = gym.make('CarRacing-v2', render_mode="rgb_array")

agent = model.DQNCarRacngAgent(epsilon=0.001)
agent.set_training()
agent.load_weights("weights2.h5")

if STARTING_EPISODE > 1:
    model_path = f"save/trial_{STARTING_EPISODE-1}.h5"
    agent.load_weights(model_path)

rewards = []
# with open("test.npy", "rb") as f:
#     rewards = np.load(f).tolist()

for e in tqdm(range(STARTING_EPISODE, ENDING_EPISODE+1)):
    init_state, _ = env.reset()
    init_state = process_state_image(init_state)

    total_reward = 0
    reward = 0
    negative_reward_counter = 0
    state_frame_stack_queue = deque([init_state]*agent.frame_stack_num, maxlen=agent.frame_stack_num)
    time_frame_counter = 1
    
    for i in range(2000):
        x = i % 2
        current_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)
        action = (agent.act(current_state_frame_stack)[0], 
                  x,# acceleration
                 0) # braking
        
#        for _ in range(SKIP_FRAMES+1):
        next_state, r, done, _, info = env.step(action)
        reward += r

        # If continually getting negative reward 10 times after the tolerance steps, terminate this episode
        negative_reward_counter = negative_reward_counter + 1 if time_frame_counter > 50 and r < 0 else 0

        if done:
            break

        total_reward += reward

        if RENDER:
            cv2.imshow("car", next_state)
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break
        
        if i % SKIP_FRAMES == 0:
            next_state = process_state_image(next_state)
            state_frame_stack_queue.append(next_state)
            next_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)

            agent.memorize(current_state_frame_stack, action, reward, next_state_frame_stack, done)

            reward = 0

            if done or negative_reward_counter >= 25 or total_reward < 0:
                print('Episode: {}/{}, Scores(Time Frames): {}, Total Rewards(adjusted): {:.2}, Epsilon: {:.2}'.format(e, ENDING_EPISODE, time_frame_counter, float(total_reward), float(agent.epsilon)))
                break
            if len(agent.memory) > TRAINING_BATCH_SIZE:
                agent.replay(TRAINING_BATCH_SIZE)
            time_frame_counter += 1
    
    rewards.append(total_reward)

    if e % UPDATE_TARGET_MODEL_FREQUENCY == 0:
        agent.update_target_model()

    if e % SAVE_TRAINING_FREQUENCY == 0:
        agent.save_weights('./save/trial_{}.h5'.format(e))
        with open('test.npy', 'wb') as f:
            np.save(f, np.array(rewards))


env.close()