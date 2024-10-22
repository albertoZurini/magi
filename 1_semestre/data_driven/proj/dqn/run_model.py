import gym
from collections import deque
from tqdm import tqdm
from common import process_state_image, generate_state_frame_stack_from_queue, export_video

import model

EPISODES_NUMBER = 10
#MODEL_PATH = "./save/trial_1000.h5"
MODEL_PATH = "./weights.h5"

env = gym.make('CarRacing-v2', render_mode="human")
agent = model.DQNCarRacngAgent(epsilon=0) # Set epsilon to 0 to ensure all actions are instructed by the agent
agent.load_weights(MODEL_PATH)

for e in range(EPISODES_NUMBER):
    init_state, _ = env.reset()
    # frames = [init_state]
    init_state = process_state_image(init_state)

    total_reward = 0
    punishment_counter = 0
    state_frame_stack_queue = deque([init_state]*agent.frame_stack_num, maxlen=agent.frame_stack_num)
    time_frame_counter = 1
    
    
    for x in [1,0]*2000:
        env.render()

        current_state_frame_stack = generate_state_frame_stack_from_queue(state_frame_stack_queue)
        action = (agent.act(current_state_frame_stack)[0], x, 0)
        next_state, r, done, _, info = env.step(action)
        # frames.append(next_state)

        total_reward += r

        next_state = process_state_image(next_state)
        state_frame_stack_queue.append(next_state)

        if done:
            print('Episode: {}/{}, Scores(Time Frames): {}, Total Rewards: {:.2}'.format(e+1, EPISODES_NUMBER, time_frame_counter, float(total_reward)))
            break
        time_frame_counter += 1

    # export_video(frames, f"trial{e}")