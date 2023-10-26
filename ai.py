import random
from collections import deque
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import Adam
import numpy as np

# TODO https://www.mlq.ai/deep-reinforcement-learning-for-trading-with-tensorflow-2-0/
# https://karan-jakhar.medium.com/100-days-of-code-day-4-6fbc672171e4



class AI_Trader():

    def __init__(self, state_size, action_space=3, model_name='AITrader'):
        self.state_size = state_size
        self.action_space = action_space
        self.memory = deque(maxlen=2000)
        self.inventory = []
        self.model_name = model_name
        self.gamma = 0.95  # учетная ставка
        self.epsilon = 1.0
        self.epsilon_final = 0.01
        self.epsilon_decay = 0.995
        self.model = self.model_builder

    def model_builder(self):
        model = Sequential()
        model.add(Dense(units=32, activation='relu', input_dim=self.state_size))
        model.add(Dense(units=64, activation='relu'))
        model.add(Dense(units=128, activation='relu'))
        model.add(Dense(units=self.action_space, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=0.001))
        return model

    def trade(self, state):
        if random.random() <= self.epsilon:
            return random.randrange(self.action_space)

        actions = self.model.predict(state)
        return np.argmax(actions[0])











