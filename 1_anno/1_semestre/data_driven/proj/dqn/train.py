import gym
import cv2
from collections import deque
import numpy as np
from tqdm import tqdm

import model

RENDER                        = False
STARTING_EPISODE              = 1
ENDING_EPISODE                = 1000
SKIP_FRAMES                   = 2
TRAINING_BATCH_SIZE           = 64
SAVE_TRAINING_FREQUENCY       = 25
UPDATE_TARGET_MODEL_FREQUENCY = 5

env = gym.make('CarRacing-v2', render_mode="rgb_array")

def process_state_image(state):
    state = state[0:84, :]
    state = cv2.cvtColor(state, cv2.COLOR_BGR2GRAY)
    state = state.astype(np.float32)
    state /= 255.0
    return state

def generate_state_frame_stack_from_queue(deque):
    frame_stack = np.array(deque)
    # Move stack dimension to the channel dimension (stack, x, y) -> (x, y, stack)
    sp = frame_stack.shape
    return frame_stack.reshape(3, 84, 96) # np.transpose(frame_stack, (1, 2, 0))

agent = model.DQNCarRacngAgent()
agent.set_training()

# TODO: if model exists load it

for e in tqdm(range(STARTING_EPISODE, ENDING_EPISODE+1)):
    init_state, _ = env.reset()
    init_state = process_state_image(init_state)

    total_reward = 0
    negative_reward_counter = 0
    state_frame_stack_queue = deque([init_state]*agent.frame_stack_num, maxlen=agent.frame_stack_num)
    time_frame_counter = 1
    
    for x in [1,0]*2000:
        if RENDER:
            env.render()

        current_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)
        action = (agent.act(current_state_frame_stack)[0], 
                  x,# acceleration
                 0) # braking

        reward = 0
        for _ in range(SKIP_FRAMES+1):
            next_state, r, done, _, info = env.step(action)
            reward += r
            if done:
                break

        # If continually getting negative reward 10 times after the tolerance steps, terminate this episode
        negative_reward_counter = negative_reward_counter + 1 if time_frame_counter > 100 and reward < 0 else 0

        # Extra bonus for the model if it uses full gas
        #if action[1] == 1 and action[2] == 0:
        #    reward *= 1.5

        total_reward += reward

        next_state = process_state_image(next_state)
        state_frame_stack_queue.append(next_state)
        next_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)

        agent.memorize(current_state_frame_stack, action, reward, next_state_frame_stack, done)

        if done or negative_reward_counter >= 25 or total_reward < 0:
            print('Episode: {}/{}, Scores(Time Frames): {}, Total Rewards(adjusted): {:.2}, Epsilon: {:.2}'.format(e, ENDING_EPISODE, time_frame_counter, float(total_reward), float(agent.epsilon)))
            break
        if len(agent.memory) > TRAINING_BATCH_SIZE:
            agent.replay(TRAINING_BATCH_SIZE)
        time_frame_counter += 1

    if e % UPDATE_TARGET_MODEL_FREQUENCY == 0:
        agent.update_target_model()

    if e % SAVE_TRAINING_FREQUENCY == 0:
        agent.save('./save/trial_{}.h5'.format(e))

env.close()