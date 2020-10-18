import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, GreedyQPolicy
from rl.memory import SequentialMemory
import random
import subprocess
memory = SequentialMemory(limit=50000, window_length=1)
model = Sequential()
num_actions = 10
model.add(Flatten(input_shape=(1,) + tuple([3])))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(num_actions))
model.add(Activation('linear'))
print(model.summary())
#policy = EpsGreedyQPolicy()
policy = GreedyQPolicy()
dqn = DQNAgent(model=model, nb_actions=num_actions, memory=memory, nb_steps_warmup=1,
               target_model_update=1e-2, policy=policy)

dqn.compile(Adam(lr=1e-3), metrics=['mae'])
def build_callbacks(env_name):
    checkpoint_weights_filename = 'dqn_' + env_name + '_weights_{step}.h5f'
    log_filename = 'dqn_{}_log.json'.format(env_name)
    callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=5000)]
    callbacks += [FileLogger(log_filename, interval=100)]
    return callbacks
class Router():
    state = [0,0,0]
    def step(self, action):
        print(action)
        #os.system("sudo python measure.py")
        res = subprocess.check_output("python M3.py", shell = True)
        res = str(res)
        res = str(res).replace('\\r','').replace('b','').replace("'","").split("\\n")[:3]
        self.state = [int(res[0]), int(res[1]), int(res[2])]
        done = False
        reward = self.get_reward()     
        return self.state,reward,done,{}
    
    def reset(self):
        self.state = [0,0,0]
        return [0,0,0]

    def get_reward(self):
        delay = self.state[0]
        delay /= 5
        delay = 10 - delay

        loss = self.state[1]
        loss /= 10
        loss = 10 - loss

        return (delay*1.5 + loss*0.5)/2
env = Router()
#dqn.fit(env,nb_steps=10000)
dqn.test(env, nb_episodes=1000, visualize=False)
