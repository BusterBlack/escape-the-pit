########################################
# Reinforcement Learning agent to play the 
# game and learn from the game
########################################

# imports 
from typing import Tuple, Any, List
# standards
import random 
import numpy as np
from collections import deque
from keras.models import Sequential, clone_model
from keras.layers import Dense, Dropout, BatchNormalization
from keras.optimizers import Adam, SGD 
from keras.callbacks import ReduceLROnPlateau
from keras import backend as K


class agent:
    """
    Reinforcement Learning agent 
    """
    def __init__(self, state_size: int, cap: int, step_size: int) -> None:
        """
        initialise the agent
        """
        self.state_size = state_size        # size of the state tuple 
        self.numNewAgents = cap
        self.step_size = step_size
        self.action_space = self.getActionSpace(self.numNewAgents, self.step_size)
        self.action_size = len(self.action_space)      # Number of possible actions (int)
        self.memory = deque(maxlen=1000)    # memory length
        self.gamma = 0.90
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999      # rate at which exploration decays
        self.learning_rate = 0.001 
        self.counter = 0
        self.target_update_interval = 20
        self.model = self._build_model()
        self.target_model = self._build_target_model()
        # K.learning_phase(1)

    def _build_target_model(self) -> Sequential:
        """
        build the target prediction model
        """
        target_model = clone_model(self.model)
        target_model.build((None, self.state_size + self.action_size))
        target_model.set_weights(self.model.get_weights())
        return target_model


    def _build_model(self) -> Sequential:
        """
        Build the neural network the agent will use to learn
        """
        # define the learning model
        model = Sequential()
        model.add(Dense(64, input_dim=(self.state_size+self.action_size), activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(32, activation='relu'))
        # model.add(BatchNormalization())
        model.add(Dense(1))
        # compile the model
        # model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        optimizer = Adam(learning_rate=self.learning_rate)
        # optimizer = SGD(learning_rate=self.learning_rate)
        model.compile(loss='mse', optimizer=optimizer)

        model.summary()

        return model

    def lr_decay(self, epoch: int) -> float:
        """
        learning rate decay callback
        """
        
        K.set_value(self.model.optimizer.lr, self.learning_rate * np.power(0.5, np.floor((1+epoch)/10.0)) )


    def remember(self, state: Tuple[int], action: Tuple[int], reward: int, next_state: Tuple[int], done: int) -> None:
        """
        add results to move to the memory duffer
        """
        # convert action into action_space index
        action = np.where(self.action_space == action)[0][0]

        # create the state-action with embedded one-hot encoded action, indexed at the action number
        state_action = np.concatenate((state, np.array([np.eye(self.action_size)[action].astype(int)])), axis=1)
        # append to the memory buffer
        self.memory.append((state_action, reward, next_state, action, done))


    def act(self, state: List[int]) -> Any:
        """
        Choose action either by exploitation or exploration based on Greedy Algorithm
        The action is (selfish, selfless, collective)
        """
        if np.random.rand() <= self.epsilon:
            # return a random action 
            if len(state) > 1:
                # if there is more than one state (i.e. in replay state)
                action = np.random.randint(low=0, high=self.action_size, size=(len(state),1))
                return self.action_space[action]
            else:
                action = random.randrange(self.action_size)
                return self.action_space[action]

        if len(state) > 1:
            state_action_input = np.concatenate((np.repeat(state, self.action_size, axis=0), np.tile(np.eye(self.action_size).astype(int), (len(state),1))), axis=1)
            # predict for all inputs
            q_values = self.model.predict(state_action_input, verbose="0", batch_size=32)
            # reshape output for each state and its actions q-values
            reshaped_q_values = np.reshape(q_values, (len(state), self.action_size))
            # choose action with the highest q-value
            action = np.argmax(reshaped_q_values, axis=1)    # here the action is a list
        else:
            # create state-action 
            state_action_input = np.concatenate((np.repeat(state, self.action_size, axis=0), np.eye(self.action_size).astype(int)), axis=1)
            q_values = self.model.predict(state_action_input, verbose="0", batch_size=32)
            # choose action with the highest q-value
            action = np.argmax(q_values)

        # update counter
        self.counter += 1
        ### The action here is an integer of the one hot encoded action matrix. 
        ### The real action much to chosen. In the case of multiple state (replay) this indexes the action space with a list of actions
        real_action = self.action_space[action]

        return real_action

    
    def exploit(self, state: Tuple[int]) -> Any:
        """
        exploit learned knowledge with no random exploration step
        """
        # build the one hot embedded state-action 
        state_action_input = np.concatenate((np.repeat([state], self.action_size, axis=0), np.eye(self.action_size).astype(int)), axis=1)
        q_values = self.model.predict(state_action_input, verbose="0", batch_size=32)
        # choose action with hightest q-value
        action = np.argmax(q_values)
        return self.action_space[action]
        

    def load(self, name: str) -> None:
        """
        Load pre-trained weights into the model
        """
        self.model.load_weights(name)
    
    def save(self, name: str) -> None:
        """
        Save the trained wieghts for later use
        """
        self.model.save_weights(name)


    def replay(self, batch_size: int) -> None:
        """
        Perform the Q-Learning method
        """

        # get a mini batch from the memory buffer
        minibatch = random.sample(self.memory, batch_size)
        # get indiviuals from the batch
        batch_state_action = np.squeeze(np.array(list(map(lambda x: x[0], minibatch))))
        batch_reward = np.squeeze(np.array(list(map(lambda x: x[1], minibatch))))
        batch_next_state = np.squeeze(np.array(list(map(lambda x: x[2], minibatch))))
        batch_actions = np.squeeze(np.array(list(map(lambda x: x[3], minibatch))))
        batch_done = np.squeeze(np.array(list(map(lambda x: x[4], minibatch))))
        
        ## Get next-action
        next_action = np.squeeze(self.act(batch_next_state))
        # find index of where the list next_action is equal to the action space
        next_action = [np.where(self.action_space == target)[0][0] for target in next_action]

        ##
        # perform q-learning
        ##
        # create one hot encoded state-action pair
        next_state_action_input = np.concatenate((batch_next_state, np.eye(self.action_size)[next_action].astype(int)), axis=1)
        # get target q-values
        target_q_values = batch_reward + self.gamma * self.target_model.predict(next_state_action_input, verbose="0", batch_size=32)


        ############################
        # no need to predict based on state_action pair, as the regression gives a single output, not a vector
        # therefore all values will become the target_q_values
        ############################

        # train the model
        # self.model.fit(batch_state_action, target_q_values, verbose="0", batch_size=32)
        self.model.train_on_batch(batch_state_action, target_q_values)
        # update epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # update the training network
        if self.counter % self.target_update_interval == 0:
            self.target_model.set_weights(self.model.get_weights())


    def getActionSpace(self, cap: int, step_size: int):
        """
        get the actions space for a certain new agent cap and step size between actions
        """
        # define the output 
        output = []

        for i in range(0, cap+1, step_size):
            for j in range(cap, 0, -step_size):
                if i == cap:
                    j=0
                    l=0
                    output.append([i,j,l])
                    break
                if (j-i)<0:
                    break
                j=j-i
                l=cap-j-i
                output.append([i,j,l])

        return np.array(output)

#######################################################
###################### Q-LEARNING #####################
#######################################################

    # def _build_modelQ(self) -> Sequential:
    #     """
    #     Build the neural network the agent uses to learn
    #     """
    #     model = Sequential()
    #     model.add(Dense(64, input_dim=self.state_size, activation='relu'))
    #     model.add(Dense(32, activation='relu'))
    #     model.add(Dense(self.action_size, activation='linear'))
    #     # compile the model
    #     model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))

    #     model.summary()

    #     return model

    # def replayQ(self, batch_size: int) -> None:
    #     """
    #     Perform the Q-Learning method
    #     """
        
    #     minibatch = random.sample(self.memory, batch_size)
    #     ##
    #     # Code to generate batches of states, actions, rewards
    #     # next states out of a samples minibatch
    #     ##
    #     batch_state = np.squeeze(np.array(list(map(lambda x: x[0], minibatch))))
    #     batch_action = np.squeeze(np.array(list(map(lambda x: x[1], minibatch))))
    #     batch_reward = np.squeeze(np.array(list(map(lambda x: x[2], minibatch))))
    #     batch_next_state = np.squeeze(np.array(list(map(lambda x: x[3], minibatch))))
    #     batch_done = np.squeeze(np.array(list(map(lambda x: x[4], minibatch))))

    #     ###
    #     # Q-Learning
    #     ###
    #     # compute target with forward pass
    #     target = (batch_reward + self.gamma * np.amax(self.model.predict(batch_next_state, verbose="0", batch_size=32), 1))
    #     # replace target with reward (when done is true)
    #     target[batch_done == 1] = batch_reward[batch_done == 1]
    #     # do a forward pass using ```state```
    #     target_f = self.model.predict(batch_state, verbose="0", batch_size=32)

    #     for k in range(target_f.shape[0]):
    #         # for each action, update the parameter for target/action pair
    #         target_f[k][batch_action[k]] = target[k]
        
    #     # update the network 
    #     K.placeholder(shape=[32,189], dtype=float)
    #     self.model.train_on_batch(batch_state, target_f)
    #     if self.epsilon > self.epsilon_min:
    #         self.epsilon *= self.epsilon_decay



    # def actQ(self, state: Tuple[int]) -> Any:
    #     """
    #     Choose action either by exploitation or exploration
    #     """
    #     if np.random.rand() <= self.epsilon:
    #         action = random.randrange(self.action_size)
    #         real_action = self.action_space[action]
    #         return real_action
        
    #     act_values = self.model.predict(state, verbose="0", batch_size=32)
    #     action = np.argmax(act_values[0])
    #     real_action = self.action_space[action]
    #     # update counter
    #     self.counter += 1

    #     return real_action # return action

    # def rememberQ(self, state: Tuple[int], action: Tuple[int], reward: int, next_state: Tuple[int], done: int) -> None:
    #     """
    #     add results of move to the memory deque
    #     """
    #     action = np.where(self.action_space == action)[0][0]
    #     self.memory.append((state, action, reward, next_state, done))

