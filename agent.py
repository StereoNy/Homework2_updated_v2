import random, re, datetime
import numpy as np


class Agent(object):
    def __init__(self, game):
        self.game = game

    def getAction(self, state):
        raise Exception("Not implemented yet")


class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)


class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getAction(self, state):
        legal_actions = self.game.actions(state)

        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)


class TeamNameMinimaxAgent(Agent):
    step = 0

    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        ### START CODE HERE ###
        if TeamNameMinimaxAgent.step < 3:
            #begin
            self.action = self.startAction(state, player)
            TeamNameMinimaxAgent.step += 1
        else:
            #minimax
            value = self.max_value(state, player, float('-inf'), float('inf'), 0)
            self.action = value[1]
        
        



    def max_value(self, state, player, a, b, t):
        #depth
        if t == 1:
            return self.Heru(state, player), None
        v = float('-inf')
        next_t = t + 1
        for action in self.game.actions(state):
            '''
            de = action[0][0] - action[1][0]
            if player == 1:
                next_e = e + de
            else:
                next_e = e - de
            '''
            next_state = self.game.succ(state, action)
            value = self.min_value(next_state, 3 - player, a, b, next_t)
            if value[0] > v :
                Action = action
                v = value[0]
            if v >= b:
                return v, Action
            a = max(a, v) 
        return v, Action

    def min_value(self, state, player, a, b, t):
        #depth
        if t == 1:
            return self.Heru(state, player), None
        v = float('inf')
        next_t = t + 1
        for action in self.game.actions(state):
            '''
            de = action[0][0] - action[1][0]
            if player == 2:
                next_e = e + de
            else:
                next_e = e - de
            '''
            next_state = self.game.succ(state, action)
            value = self.max_value(next_state, 3 - player, a, b, next_t)
            if value[0] < v :
                Action = action
                v = value[0]
            if v <= a:
                return v, Action
            a = min(b, v) 
        return v, Action

    def Heru (self, state, player):
        a = 1
        b = 0
        c = 0
        if player == 1:
            a = -a
        #distance = 0
        #board = []
        vertical = np.zeros((10,))
        horizontal = np.zeros_like(vertical)
        cnt = 0
        for point,val in state[1].board_status.items():
            if val == player:
                vertical[cnt]=point[0]
                
                if point[0]<=10:
                    #board.append((point[0],2*point[1]-point[0]))
                    horizontal[cnt] =  2*point[1]-point[0]
                else:
                    #board.append((point[0],point[0]+2*point[1]-20))
                    horizontal[cnt] =  point[0]+2*point[1]-20
                cnt+=1
        '''
        for p in point:
            if player==2:
                distance += (p[0]-1)**2+(p[1]-1)**2
            else:
                distance += (p[0]-19)**2+(p[1]-19)**2
        '''
        ave_vert = np.sum(vertical)/10
        variance = np.dot((vertical-ave_vert),(vertical-ave_vert).T)/10
        ave_hori = np.sum(horizontal)/10
        variance_hori = np.dot((horizontal-ave_hori),(horizontal-ave_hori).T)/10
        eval = a * ave_vert - b * variance_hori - c * variance 
        return eval

    def startAction(self, state, player):
        #pattens people usually follow at the beginning of the game
        if player == 1:
            if TeamNameMinimaxAgent.step==0:
                action = ((16,1),(15,2))
            elif TeamNameMinimaxAgent.step==1:
                action = ((18,1),(14,3))
            elif TeamNameMinimaxAgent.step==2:
                action = ((19,1),(13,3))
        else:
            if TeamNameMinimaxAgent.step==0:
                action = ((4,1),(5,2))
            elif TeamNameMinimaxAgent.step==1:
                action = ((2,1),(6,3))
            elif TeamNameMinimaxAgent.step==2:
                action = ((1,1),(7,3))
        return action
        ### END CODE HERE ###
    


