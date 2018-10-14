import random, re, datetime
import numpy as np
from math import *
from operator import eq
import time


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
    # a one-step-lookahead greedy agent that returns action with max vert1 advance
    def getAction(self, state):
        legal_actions = self.game.actions(state)

        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:
            max_vert1_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vert1_advance_one_step]
        else:
            max_vert1_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vert1_advance_one_step]
        self.action = random.choice(max_actions)


class RandomMinimaxAgent(Agent):
    #fixed
    d = 0.16
    e = 0
    a = 1
    #changing
    b = 0
    c = 0
    step = 0
    position = 'Start'
    vert = 0
    #best_eval = float('-inf')
    def getAction(self, state):
        print("b:", self.b, "c:", self.c)
        print("state:", self.position)
        start_time = time.time()
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)
        player = self.game.player(state)
        ### START CODE HERE ###
        _ = self.Heru(state, player)
        print(self.vert)
        if self.vert==3:
            self.step = 0
        if self.step < 3:
            #begin
            self.action = self.startAction(state, player)
            print(self.action)
            self.step += 1
        else:
            if self.position=='end':
                best_eval = float('-inf')
                print(best_eval)
                for action in legal_actions:
                    next_state = self.game.succ(state, action)
                    e = self.Heru(next_state, player)
                    if best_eval<e:
                        best_eval = e
                max_actions = []
                print(best_eval)
                for action in legal_actions:
                    next_state = self.game.succ(state, action)
                    e = self.Heru(next_state, player)
                    if abs(best_eval-e)<0.01:
                        max_actions.append(action)
                self.action = random.choice(max_actions)
                
            else:
            #minimax
                value = self.max_value(state, player, float('-inf'), float('inf'), 2, start_time)
                self.action = value[1]
                print("using minimax")
        print(self.position)
        



    def max_value(self, state, player, a, b, t, start_time):
        now_player = self.game.player(state)
        Action = None
        #depth
        if t == 0:
            return self.Heru(state, player), None
        v = float('-inf')
        next_t = t - 1
        for action in self.game.actions(state):
            now_time = time.time()
            if (now_time-start_time)>1.9:
                break
            if now_player==1 and (action[0][0]-action[1][0]<=0):
            	continue
            if now_player==2 and (action[0][0]-action[1][0]>=0):
            	continue
            next_state = self.game.succ(state, action)
            value = self.min_value(next_state, player, a, b, next_t, start_time)
            if value[0] > v :
                Action = action
                v = value[0]
            if v >= b:
                return v, Action
            a = max(a, v) 
        return v, Action

    def min_value(self, state, player, a, b, t, start_time):
        now_player = self.game.player(state)
        Action = None
        #depth
        if t == 0:
            return self.Heru(state, player), None
        v = float('inf')
        next_t = t - 1
        for action in self.game.actions(state):
            now_time = time.time()
            if (now_time-start_time)>1.9:
                break
            if now_player==1 and (action[0][0]-action[1][0]<0):
            	continue
            if now_player==2 and (action[0][0]-action[1][0]>0):
            	continue
            next_state = self.game.succ(state, action)
            value = self.max_value(next_state, player, a, b, next_t, start_time)
            if value[0] < v :
                Action = action
                v = value[0]
            if v <= a:
                return v, Action
            a = min(b, v) 
        return v, Action

    def Heru (self, state, player):
        vertical = np.zeros((10,))
        vertical_op = np.zeros((10,))
        horizontal = np.zeros_like(vertical)
        horizontal_op = np.zeros_like(vertical_op)
        cnt = 0
        cnt_op = 0
        In = 0
        In_op = 0
        Out_op = 0
        Out = 0
        for point,val in state[1].board_status.items():
            if val == 1:
                vertical[cnt]=point[0]
                if point[0]>=16:
                	Out+=1
                if point[0]<=4:
                	In+=1
                if point[0]<=10:
                    horizontal[cnt] =  2*point[1]-point[0]
                else:
                    horizontal[cnt] =  point[0]+2*point[1]-20
                cnt+=1
            elif val == 2:
                vertical_op[cnt_op]=point[0]
                if point[0]>=16:
                	In_op+=1
                if point[0]<=4:
                	Out_op+=1
                if point[0]<=10:
                    horizontal_op[cnt_op] =  2*point[1]-point[0]
                else:
                    horizontal_op[cnt_op] =  point[0]+2*point[1]-20
                cnt_op+=1
        if player == 1:
            ave_vert = 20 - np.sum(vertical)/10 
            variance = np.dot((vertical-ave_vert),(vertical-ave_vert).T)/10
            variance = sqrt(variance)
            ave_hori = np.sum(horizontal)/10
            variance_hori = np.dot((horizontal-ave_hori),(horizontal-ave_hori).T)/10
            variance_hori = sqrt(variance_hori)
            ave_vert_op = np.sum(vertical_op)/10
            self.vert = ave_vert
            if In >= 8:
                self.position = 'end'
                self.HeruUpdate(0,0)
            elif ave_vert<=5:
                self.position='start'
                self.HeruUpdate(self.d, self.e)
            else:
                self.position='half'
            eval = self.a*((ave_vert+ In - Out)-(ave_vert_op+ In_op - Out_op))-self.b*variance - self.c*variance_hori
        else:
            ave_vert = 20 - np.sum(vertical)/10 
            ave_vert_op = np.sum(vertical_op)/10 
            variance_op = np.dot((vertical_op-ave_vert_op),(vertical_op-ave_vert_op).T)/10
            variance_op = sqrt(variance_op)
            ave_hori_op = np.sum(horizontal_op)/10
            variance_hori_op = np.dot((horizontal_op-ave_hori_op),(horizontal_op-ave_hori_op).T)/10
            variance_hori_op = sqrt(variance_hori_op)
            self.vert = ave_vert_op
            if In_op >= 8:
                self.position = 'end'
                self.HeruUpdate(0,0)
            elif ave_vert_op<=5:
                self.position = 'start'
                self.HeruUpdate(self.d, self.e)
            else:
                self.position = 'half'
            eval = self.a*((ave_vert_op + In_op - Out_op)-(ave_vert+ In - Out))- self.b*variance_op - self.c*variance_hori_op
        return eval

    def HeruUpdate(self, b, c):
        self.b = b
        self.c = c

    def startAction(self, state, player):
        #pattens people usually follow at the beginning of the game
        print("Start:", self.step)
        if player == 1:
            if self.step==0:
                action = ((16,1),(15,2))
            elif self.step==1:
                action = ((18,1),(14,3))
            elif self.step==2:
                action = ((19,1),(13,3))
        else:
            if self.step==0:
                action = ((4,1),(5,2))
            elif self.step==1:
                action = ((2,1),(6,3))
            elif self.step==2:
                action = ((1,1),(7,3))
        return action
        ### END CODE HERE ###
    


