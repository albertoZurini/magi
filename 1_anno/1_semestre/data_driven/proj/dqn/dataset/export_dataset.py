import gym
import glob
import io
import base64
from moviepy.editor import ImageSequenceClip

import cv2
import numpy as np 
import matplotlib.pyplot as plt
import os

import random
import math


env = gym.make('CarRacing-v2')

observation, _ = env.reset()
env.render() 
rewardsum = 0  
previous_error = 0    

frames = []
frames.append(observation)

class ImageProcessor:
    def green_mask(self, observation):
        hsv = cv2.cvtColor(observation, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

        ## slice the green
        imask_green = mask_green>0
        green = np.zeros_like(observation, np.uint8)
        green[imask_green] = observation[imask_green]
        return(green)

    def blur_image(self, observation):
        blur = cv2.GaussianBlur(observation, (5, 5), 0)
        return blur

    def canny_edge_detector(self, observation):
        canny = cv2.Canny(observation, 50, 150)
        return canny

    def find_error(self, observation, previous_error):
        cropped = observation[63:65, 24:73]

        green = self.green_mask(cropped)
        blur  = self.blur_image(green)
        canny = self.canny_edge_detector(blur)
        #canny = self.canny_edge_detector(green)
        
        # Find all non zero values in the cropped strip.
        # These non zero points(white pixels) corresponds to the edges of the road
        # The highest is the right boundary, while the lowest is the left boundary
        nz = cv2.findNonZero(canny)

        # Horizontal cordinates of center of the road in the cropped slice
        mid  = 24
        
        return(((nz[:,0,0].max() + nz[:,0,0].min())/2) - mid)
        #            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    ^^^  
        #                             |-----------------------|--- position of the car
        #                                                     |--- wanted position

class ImageProcessor2(ImageProcessor):
    def braking_force(self, canny):
        idx = [0 for i in range(4)]
        idx[0] = cv2.findNonZero(canny[0, 0:95])
        idx[1] = cv2.findNonZero(canny[0:83, 95])
        idx[2] = cv2.findNonZero(canny[83, 0:95])
        idx[3] = cv2.findNonZero(canny[0:83, 0])

        for i in range(len(idx)):
            if idx[i] is not None:
                idx[i] = idx[i].max()
        
        return idx
        
    def find_error_braking_position(self, observation, previous_error):
        green = self.green_mask(observation)
        blur  = self.blur_image(green)
        canny = self.canny_edge_detector(blur)
        
        idx = self.braking_force(canny)
        canny = canny[63:65, 24:73]
        
        nz = cv2.findNonZero(canny)
        mid  = 24
        
        if nz is not None:
            predicted_position = ((nz[:,0,0].max() + nz[:,0,0].min())/2)
            if (nz[:,0,0].max() - nz[:,0,0].min()) > 5:
                # needed in case only one edge of the street is visible
                steer = (predicted_position - mid)
            else:
                #if nz[:,0,0].max() <30 and nz[:,0,0].max()>20:
                #    steer = previous_error
                if nz[:,0,0].max() >= mid:
                    steer = -15
                else:
                    steer = +15
        else:
            predicted_position = -1
            steer = previous_error

            # # steer < 0 => going left
            if idx[1] is not None:
                # check it's going to the right
                if steer < 0:
                    steer = 5
            if idx[3] is not None:
                # check it's going to the left
                if steer > 0:
                    steer = -5
        
        braking_force = 0
        if idx[1] is not None:
            braking_force = idx[1]/83
            
        if idx[3] is not None:
            braking_force = idx[3]/83
        
        return steer, braking_force, predicted_position

braking_forces = []
steerings = []
frames = []
target_speeds = []
true_speeds = []
positions = []
steerings = []
steerings_errors = []
accelerations = []

IP2 = ImageProcessor2()

SPEEDS = [1, 0, 1]
BRAKING_FORCE_FACTOR = 0.9
CORNERING_SPEED = 20
STRAIGHT_SPEED = 40

org = (60, 90)
org_steering = (10, 90)
font = cv2.FONT_HERSHEY_SIMPLEX 
fontScale = 0.5
color = (255, 0, 0) 
thickness = 2

slow_down_count = 0
previous_error = 0
previous_speed_error = 0

def pid_speed(error,previous_error):
    Kp = 0.0001
    Ki = 0.03
    Kd = 0.3

    speed = Kp * error + Ki * (error + previous_error) + Kd * (error - previous_error)

    return speed

def pid(error,previous_error,Kp=0.02):
    #Kp = 0.02
    Ki = 0.03
    Kd = 0.5    

    steering = Kp * error + Ki * (error + previous_error) + Kd * (error - previous_error)

    return steering

from collections import deque

frames_collection = []


from tqdm import tqdm


# I have to store state, action, reward, next_state
for k in tqdm(range(1)):
    dataset = []
    cumulative_reward = 0
    for i in tqdm(range(1)):
        env.reset()
        for _ in range(100):
            observation, reward, done, _, info = env.step((0,0,0))

        negative_reward_counter = 0
        total_reward = 0
        for i in range(3000):
            cv2.imshow("car", observation)
            if cv2.waitKey(1) & 0xFF == ord('x'):
                break

            error, braking_force, position = IP2.find_error_braking_position(observation, previous_error)
            true_speed = np.sqrt(
                np.square(env.car.hull.linearVelocity[0])
                + np.square(env.car.hull.linearVelocity[1])
            )
            
            steering = pid(error,previous_error)
            
            # START PID CONTROLLER FOR SPEED
            
            if braking_force > 0:
                # cornering
                speed_target = CORNERING_SPEED
            else:
                speed_target = STRAIGHT_SPEED
                
            if true_speed > CORNERING_SPEED + 10 and (abs(steering) > 1 or abs(error) > 1):
                speed_target = CORNERING_SPEED
                #observation = cv2.putText(observation, "s", org_steering, font,  
                #        fontScale, color, thickness, cv2.LINE_AA)
                braking_force_reference = 0.1 + abs(true_speed - CORNERING_SPEED)/max(true_speed, CORNERING_SPEED)
                braking_force = max(braking_force, braking_force_reference)
                Kp = 0.05
            else:
                Kp = 0.03
            steering = pid(error,previous_error,Kp=Kp)
            speed_error = speed_target - true_speed
            acceleration = pid(speed_error, previous_speed_error)
            previous_speed_error = speed_error
            
            if acceleration < 0 or true_speed > CORNERING_SPEED + 5:
                bf = braking_force * BRAKING_FORCE_FACTOR
            else:
                bf = 0
            # END PID CONTROLLER FOR SPEED
                
            # TODO: save the cumulative reward an not the immediate
            
            if abs(steering) < 0.2:
                steering = 0
            elif steering > 0:
                steering = 1
            else:
                steering = -1
            action = (steering, acceleration, bf)

            # Collect data for dataset
            if i % 3 == 0:
                frames_collection.append(observation)
            
            if len(frames_collection) == 4:
                dataset.append([frames_collection[:3], action, cumulative_reward, frames_collection[1:], done])
                frames_collection.clear()
            
            # target_speeds.append(speed_target)
            # true_speeds.append(true_speed)
            # positions.append(position)
            # steerings.append(steering)
            # steerings_errors.append(error)
            # accelerations.append(acceleration)
            # braking_forces.append(bf)
                
            observation, reward, done, _, info = env.step(action)

            negative_reward_counter = negative_reward_counter + 1 if reward < 0 else 0
            if negative_reward_counter > 100:
                done = True
            cumulative_reward += reward

            previous_error = error
            
            # observation = cv2.putText(observation, str(int(bf*10)/10), org, font,  
            #            fontScale, color, thickness, cv2.LINE_AA)
            # observation = cv2.putText(observation, str(int(steering*10)/10), org_steering, font,  
            #                fontScale, color, thickness, cv2.LINE_AA)
            # frames.append(observation)

            if done :
                dataset[-1][-1] = True
                break

    import pickle 

    with open(f"./dataset/dataset_batch{k}.pkl", 'wb') as file: 
        pickle.dump(dataset, file) 

env.close()