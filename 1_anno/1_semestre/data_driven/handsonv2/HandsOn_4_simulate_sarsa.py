from scipy.io import loadmat
import numpy as np
from numpy import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pickle
from control import lqr, ss
from control.matlab import lsim
import random
from tqdm import tqdm
import os


def load_or_init_qtable(file_name):
    if os.path.exists(file_name):
        return np.load(file_name)
    else:
        return np.zeros(tuple(numberOfBins) + (action_size, ))

def save_qtable(qtable, file_name):
    #if os.path.exists(file_name):
    #    os.system(f"mv {file_name} old/`date +\"%Y-%m-%dT%H:%M:%S%z\"`_{file_name}")
    with open(file_name, "wb") as f:
        np.save(f, qtable)

lowerBounds = [
    deg2rad(-25),
    -1,
    -5,
    -2
]
upperBounds = [- i for i in lowerBounds]
max_steps= 1000

def get_random_initial_state():
    return np.array([np.deg2rad(random.uniform(-1,1)), random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1)]) # start out of equilibrium

numberOfBins = [
    10,
    10,
    10,
    10
]

action_size = 2 # left or right

class StateDiscretizer:
    def __init__(self, numberOfBins):
        self.poleAngleBin = np.linspace(lowerBounds[0],upperBounds[0],numberOfBins[0])
        self.poleAngleVelocityBin = np.linspace(lowerBounds[1],upperBounds[1],numberOfBins[1])
        self.cartPositionBin = np.linspace(lowerBounds[2],upperBounds[2],numberOfBins[2])
        self.cartVelocityBin = np.linspace(lowerBounds[3],upperBounds[3],numberOfBins[3])
        self.numberOfBins = numberOfBins


    def discretize_state(self, state):
        angle    =      state[0]
        angularVelocity=state[1]
        position =      state[2]
        velocity =      state[3]

        indexAngle=np.maximum(np.digitize(angle,self.poleAngleBin)-1,0)
        indexAngularVelocity=np.maximum(np.digitize(angularVelocity,self.poleAngleVelocityBin)-1,0)
        indexPosition=np.maximum(np.digitize(position,self.cartPositionBin)-1,0)
        indexVelocity=np.maximum(np.digitize(velocity,self.cartVelocityBin)-1,0)

        return tuple([indexAngle,indexAngularVelocity,indexPosition,indexVelocity])
    
    def is_terminal_state(self, dstate):
        if dstate[0] == 0 or dstate[0] == self.numberOfBins[0]-1:
            return True
        if dstate[2] == 0 or dstate[2] == self.numberOfBins[2]-1:
            return True
        return False

discretizer = StateDiscretizer(numberOfBins)

total_episodes = 40000
learning_rate = 0.01
gamma = 0.95                  # Discounting rate

# Exploration parameters
epsilon = 1.0                 # Exploration rate
max_epsilon = 1.0             # Exploration probability at start
min_epsilon = 0.01            # Minimum exploration probability 
decay_rate = 0.0001            # Exponential decay rate for exploration prob

qtable_sarsa = load_or_init_qtable("qtable_sarsa.npy")
rewards_sarsa = []
epsilon_decay = 10000

def episilon_greedy_policy(epsilon, qtable, state):
    exp_exp_tradeoff = random.uniform(0, 1)
        
    ## If this number > greater than epsilon --> exploitation (taking the biggest Q value for this state)
    if exp_exp_tradeoff > epsilon:
        action = np.argmax(qtable[state])

    # Else doing a random choice --> exploration
    else:
        action = random.randint(0,1)

    return action

def cart_and_pole_odeint(x, t, F):
    dxdt = np.zeros_like(x)

    dxdt[0] = x[1] #tetap
    dxdt[1] = (g*sin(x[0])+ cos(x[0])*((-F-m*l*(x[1]**2)*sin(x[0]))/(mc+m))-((miup*x[1])/(m*l))) / (l*((4/3)-((m*(cos(x[0])**2))/(mc+m))))    #teta2p
    dxdt[2] = x[3] #xp
    dxdt[3] = (F+m*l*((x[1]**2)*sin(x[0])-dxdt[1]*cos(x[0])))/(mc+m) #x2p
    return dxdt

g = 9.8 # gravitational acceleration
mc = 1  # cart mass [kg]
l = 0.5 # half-pole length [m]
m = 0.1 # pole mass [kg]
miup = 2e-6 # pole friction coefficient

time_step=0.02
t0_odeint=0
t1_odeint = t0_odeint+0.02
t_odeint = np.array([t0_odeint, t1_odeint])


for episode in tqdm(range(total_episodes)):
    # Reset the environment
    episode_reward = 0
    state_c = get_random_initial_state()
    state = discretizer.discretize_state(state_c)
    
    action = episilon_greedy_policy(epsilon, qtable_sarsa, state)

    for step in range(max_steps):
        new_action = episilon_greedy_policy(epsilon, qtable_sarsa, state)
            
        # convert action into force
        if action == 1:
            F = 10
        else:
            F = -10

        # Simulate the system
        x_odeint = odeint(cart_and_pole_odeint, state_c, t_odeint, args=(F, ))
        new_state_c = x_odeint[1]
        new_state = discretizer.discretize_state(new_state_c)
        
        if discretizer.is_terminal_state(new_state):
            reward = -100
        else:
            reward = 1

        qtable_sarsa[state + (action,)] = qtable_sarsa[state + (action,)] + \
        learning_rate * (reward + gamma * qtable_sarsa[new_state + (new_action,)] - qtable_sarsa[state + (action,)])
        
        episode_reward += reward
        
        # Our new state is state
        state = new_state
        state_c = new_state_c
        action = new_action

        # If done (if we're dead) : finish episode
        if discretizer.is_terminal_state(new_state):
            break
        
    # Reduce epsilon (because we need less and less exploration)
    epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*epsilon_decay)
    epsilon_decay += 1 
    rewards_sarsa.append(episode_reward)

    if episode % 5000 == 0:
        print(np.average(rewards_sarsa[-5000:]))

print ("Score over time: " +  str(sum(rewards_sarsa)/total_episodes))
print("Epsilon:", epsilon)

save_qtable(qtable_sarsa, "qtable_sarsa.npy")

plt.plot(np.convolve(rewards_sarsa,np.ones(1000)/1000,mode='valid'))

simulate_qtable(qtable_sarsa)