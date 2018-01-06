#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 14:24:04 2017

@author: lakshya
"""

import numpy as np
import copy
from itertools import groupby
import time
import math

# Utility functions to count fruits matrix
class Utility:
 
    def __init__(self, row, col, g):
        self.ROW = row
        self.COL = col
        self.board = g
        self.start = 0
 
    # A function to check if a given cell (row, col) can be included in DFS
    def isSafe(self, i, j, visited, type_fruit):
        return (i >= 0 and i < self.ROW and j >= 0 and j < self.COL and not visited[i][j] and self.board[i][j]==type_fruit)
             
    # A utility function to do DFS for a matrix. It only considers the 4 neighbours as adjacent vertices
    def dfs(self, i, j, visited, type_fruit):
 
        # These arrays are used to get row and column numbers of 4 neighbours of a given cell
        row = [-1,  0, 0, 1];
        col = [ 0, -1, 1, 0];
         
        # Mark this cell as visited
        visited[i][j] = True
 
        # Recur for all connected neighbours
        count_fruits = 0
        for k in range(4):
            if self.isSafe(i + row[k], j + col[k], visited, type_fruit):
                count_fruits += self.dfs(i + row[k], j + col[k], visited, type_fruit)
 
        return count_fruits+1

    #Function to drop fruits and generate new board position    
    def dropFruits(self, row, col, type_fruit):
        
        visited = [[False for j in range(self.COL)]for i in range(self.ROW)]
        positions = []
        self.dfsPositions(row, col, visited, type_fruit, positions)
        
        for pos in positions:
            self.board[pos[0]][pos[1]] = np.nan
        
        for col_idx, cols in enumerate(self.board.T):
            index = np.argwhere(np.isnan(cols))
            if(index.size == 0):
                continue
            new_cols = np.delete(cols, index)
            
            val = len(index)
            cols = np.insert(new_cols, 0, [np.nan]*val)
            self.board.T[col_idx] = cols
    
    # A utility function to do DFS for a matrix and calculate adjacent positions of a particular fruit
    def dfsPositions(self, i, j, visited, type_fruit, positions):
        # These arrays are used to get row and column numbers of 4 neighbours of a given cell
        row = [-1,  0, 0, 1];
        col = [ 0, -1, 1, 0];
         
        # Mark this cell as visited
        visited[i][j] = True
        
        positions.append([i,j])

        # Recur for all connected neighbours
        for k in range(4):
            if self.isSafe(i + row[k], j + col[k], visited, type_fruit):
                self.dfsPositions(i + row[k], j + col[k], visited, type_fruit, positions)


    def setBoard(self, board):
        self.board = copy.deepcopy(board)
    
    def reduceBoard(self):
        
        for row in self.board:
            bool_array = row.tolist()
            bool_array = ~np.isnan(bool_array)
            if(np.sum(bool_array)==0):
                self.start = self.start + 1
        
    def countFruits(self, num_fruit):

        # Initially all cells are unvisited
        visited = [[False for j in range(self.COL)]for i in range(self.ROW)]
 
        #Count to keep track of position of fruits, their type and count
        count = []
        for type_fruit in num_fruit:
            for i in range(self.start, self.ROW):
                for j in range(self.COL):
                    # If a cell with value 1 is not visited yet
                    fruits = 0
                    if visited[i][j] == False and self.board[i][j] == type_fruit:
                        fruits = self.dfs(i, j, visited, type_fruit)
                        count.append([(i,j), type_fruit, fruits])
     
        return count

def isTerminal(board):
    bool_array = board.tolist()
    bool_array = ~np.isnan(bool_array)
    if(np.sum(bool_array)==0):
        return True
    else:
        return False

def utilityScore(score_1, score_2):
    return score_1 - score_2

def min_value(board, type_fruit, alpha, beta, score_1, score_2, depth, num_moves, depth_reduced):
    if isTerminal(board):
        return utilityScore(score_1, score_2)
    
    infinity = float('inf')
    value = infinity
    
    utility = Utility(len(board), len(board), copy.deepcopy(board))
    
    utility.reduceBoard()
    possible_moves = utility.countFruits(type_fruit)
    possible_moves.sort(key=lambda x:x[2], reverse=True)
    
    
    if depth <= 0:
        new_score2 = score_2 + possible_moves[0][2]*possible_moves[0][2]
        return utilityScore(score_1, new_score2)

    #num_moves = 20
    if len(possible_moves) >= num_moves:
        possible = possible_moves[:num_moves]
        i = num_moves
        num = [moves[2] for moves in possible]
        while i < len(possible_moves):
            if (possible[-1][-1] == possible_moves[i][-1]) or (possible[0][-1] <=3 and num.count(3) <= 2):
                possible.append(possible_moves[i])
            else:
                break
            i = i+1
        num = [moves[2] for moves in possible]
    else:
        possible = possible_moves
        num = [moves[2] for moves in possible]
        
    if num.count(1) > 15 and possible[0][2] >= 1:
        if not depth_reduced:
            if num.count(1) >= 40 or possible[0][2] == 1:
                depth = depth - 2
            else:
                depth = depth - 1
            depth_reduced = True
    
    if len(possible) >= 25 or num.count(1) >= 10:
        if not depth_reduced:
            depth = depth - 1
            depth_reduced = True
    
    if depth <= 0:
        new_score2 = score_2 + possible_moves[0][2]*possible_moves[0][2]
        return utilityScore(score_1, new_score2)
    
    #print depth
    
    for moves in possible:
        utility.setBoard(board)
        utility.dropFruits(moves[0][0], moves[0][1], moves[1])
        
        #print("--- %s min---" % len(possible_moves))
        
        new_score2 = score_2 + moves[2]*moves[2]
        value = min(value, max_value(utility.board, type_fruit, alpha, beta, score_1, new_score2, depth-1, num_moves, depth_reduced))
        
        if value <= alpha:
            #print("--- %s min-pruned---")
            return value
        
        beta = min(beta, value)
    
    return value

def max_value(board, type_fruit, alpha, beta, score_1, score_2, depth, num_moves, depth_reduced):
    if isTerminal(board):
        return utilityScore(score_1, score_2)
    
    infinity = float('inf')
    value = -infinity
    
    utility = Utility(len(board), len(board), copy.deepcopy(board))
    
    utility.reduceBoard()
    possible_moves = utility.countFruits(type_fruit)
    possible_moves.sort(key=lambda x:x[2], reverse=True)
    
    if depth <= 0:
        new_score1 = score_1 + possible_moves[0][2]*possible_moves[0][2]
        
        utility.dropFruits(possible_moves[0][0][0], possible_moves[0][0][1], possible_moves[0][1])
        new_moves = utility.countFruits(type_fruit)
        new_moves.sort(key=lambda x:x[2], reverse=True)
        
        if not new_moves:
            return utilityScore(new_score1, score_2)
        else:
            new_score2 = score_2 + new_moves[0][2]*new_moves[0][2]
            
            if new_score1 > new_score2:
                return utilityScore(new_score1, new_score2)
            else:
                return utilityScore(score_1, score_2)

    #num_moves = 20
    if len(possible_moves) >= num_moves:
        possible = possible_moves[:num_moves]
        i = num_moves
        num = [moves[2] for moves in possible]
        while i < len(possible_moves):
            if (possible[-1][-1] == possible_moves[i][-1]) or (possible[0][-1] <=3 and num.count(3) <= 2):
                possible.append(possible_moves[i])
            else:
                break
            i = i+1
        num = [moves[2] for moves in possible]
    else:
        possible = possible_moves
        num = [moves[2] for moves in possible]
    
    if num.count(1) > 15 and possible[0][2] >= 1:
        if not depth_reduced:
            if num.count(1) >= 40 or possible[0][2] == 1:
                depth = depth - 2
            else:
                depth = depth - 1
            depth_reduced = True
    
    if len(possible) >= 25 or num.count(1) >= 10:
        if not depth_reduced:
            depth = depth - 1
            depth_reduced = True
    
    if depth <= 0:
        new_score1 = score_1 + possible_moves[0][2]*possible_moves[0][2]
        
        utility.dropFruits(possible_moves[0][0][0], possible_moves[0][0][1], possible_moves[0][1])
        new_moves = utility.countFruits(type_fruit)
        new_moves.sort(key=lambda x:x[2], reverse=True)
        
        if not new_moves:
            return utilityScore(new_score1, score_2)
        else:
            new_score2 = score_2 + new_moves[0][2]*new_moves[0][2]
            
            if new_score1 > new_score2:
                return utilityScore(new_score1, new_score2)
            else:
                return utilityScore(score_1, score_2)
    
    #print depth
    
    for moves in possible:
        utility.setBoard(board)
        utility.dropFruits(moves[0][0], moves[0][1], moves[1])
        
        #print("--- %s max---" % len(possible_moves))
        #print("--- %s seconds ---" % (time.clock() - start))
        
        new_score1 = score_1 + moves[2]*moves[2]
        value = max(value, min_value(utility.board, type_fruit, alpha, beta, new_score1, score_2, depth-1, num_moves, depth_reduced))
        
        
        if value >= beta:
            #print("--- %s max-pruned---")
            return value
        
        alpha = max(alpha, value)
    
    return value

def alpha_beta(board, type_fruit, time_rem, time_node):
    infinity = float('inf')
    alpha = -infinity
    beta = infinity
     
    utility = Utility(len(board), len(board), copy.deepcopy(board))
    
    utility.reduceBoard()
    possible_moves = utility.countFruits(type_fruit)
    possible_moves.sort(key=lambda x:x[2], reverse=True)
    
    if time_node <= 0.25:
        time_node = 0.01
    else:
        time_node = 0.1
        
    max_moves = len(possible_moves)
    
    depth_reduced = False
    
    if time_rem < 1.0:
        return possible_moves[0]
    
    num_moves = 0
    time_allowed = 1
    
    if time_rem >= 200:
        time_allowed = (time_rem/max_moves) * 800
        num_moves = 10
    elif time_rem >= 100:
        time_allowed = (time_rem/max_moves) * 800
        num_moves = 10
    elif time_rem >= 60:
        time_allowed = (time_rem/max_moves) * 800
        num_moves = 10
        
    if len(possible_moves) >= 15 and num_moves != 0:
        possible = possible_moves[:num_moves]
        i = num_moves
        while i < len(possible_moves):
            if (possible[-1][-1] == possible_moves[i][-1]):
                possible.append(possible_moves[i])
            else:
                break
            i = i+1
            
        if len(possible) >= 20 or possible[0][2] <= 8 or max_moves <= 45:
            branching_factor = len(possible)
            depth = math.floor(math.log((time_allowed/time_node), 10))-1
        else:
            branching_factor = len(possible)
            depth = math.floor(math.log((time_allowed/time_node), 10))
    
    else:
        possible = possible_moves
        depth = math.floor(math.log((time_allowed/time_node), 10)) + 1
    
    num = [moves[2] for moves in possible]
    
    if max_moves <= 30 and max_moves >= 15:
        depth = depth + 1
    elif possible[0][-1] > 1 and num.count(1) < 10 and max_moves <= 100 and len(set(num)) > 1 and (len(type_fruit) < 3 or len(board) < 15):
        depth = depth + 1


    if len(type_fruit)==2 and depth%2 != 0:
        if len(board) <= 15:
            depth = depth + 1
        else:
            depth = depth - 1
    if len(type_fruit)==2 and time_rem <= 160:
        if len(board) >= 20:
            if depth % 2 == 0 and depth > 4:
                depth = depth - 2
            else:
                depth = depth - 1  
    
    if time_rem <= 60 and time_rem > 20:
        depth = 3
        num_moves = 10
        possible = possible[:num_moves]
    elif time_rem <= 20:
        depth = 2
        num_moves = 5
        possible = possible[:num_moves]
    
    #possible = copy.deepcopy(possible_moves)
    #depth = 4
    #print depth, max_moves, len(possible), num.count(1)

    for moves in possible:

        #print("--- %s initial---" % len(possible_moves))
        utility.setBoard(board)
        utility.dropFruits(moves[0][0], moves[0][1], moves[1])
        score_1 = moves[2]*moves[2]
        
        value = min_value(utility.board, type_fruit, alpha, beta, score_1, 0, depth-1, num_moves, depth_reduced)
        
        #print("--- %s seconds ---" % (time.clock() - start))
        
        if value > alpha:
            alpha = value
            chosen_state = moves
        
        #print alpha
        #print chosen_state
    
    return chosen_state

def play():
    
    mapping = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E' ,6:'F' ,7:'G' ,8:'H' ,9:'I', 10:'J', 11:'K', 12:'L', 13:'M', 14:'N', 15:'O', 16:'P', 17:'Q', 18:'R', 19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z' }
    
    try:
        with open("calibration.txt") as file:
            time_node = file.read().splitlines()
        
        time_node = float(time_node[0])
    except:
        time_node = 0.01
    
    data = []
    with open("input.txt") as file:
        data = file.read().splitlines()    
    
    row = int(data.pop(0))
    type_fruit = int(data.pop(0))
    time_rem = float(data.pop(0))
    
    values = []
    for val in data:
        val = list(val)
        new_val = [x if x != '*' else 'nan' for x in val]
        values.append(list(new_val))
    
    board = np.array(values, dtype=float)
    
    type_fruit = board.flatten().tolist()
    type_fruit = [fruit for fruit in type_fruit if ~np.isnan(fruit)]
    
    type_fruit = list(set(type_fruit))
    
    row = len(board)
    col = len(board)
        
    g= Utility(row, col, board)
    
    try:
        start = time.clock()
        move = alpha_beta(board, type_fruit, time_rem, time_node)
        print("--- %s seconds ---" % (time.clock() - start))
        g.dropFruits(move[0][0], move[0][1], move[1])
        print move
        #print g.board
    except:
        moves = g.countFruits(type_fruit)
        moves.sort(key=lambda x:x[2], reverse=True)
        move = moves[0]
        g.dropFruits(move[0][0], move[0][1], move[1])
    
    ans_row = move[0][0]
    ans_col = move[0][1]
    
    ans = mapping.get(ans_col+1) + str(ans_row+1)
    
    with open("output.txt", 'w+') as file:
        file.write(ans)
        file.write("\n")
        for row in g.board:
            new_row = []
            for val in row:
                if np.isnan(val):
                    new_row.append('*')
                else:
                    new_row.append(str(int(val)))
            file.write(''.join(str(r) for r in new_row))
            file.write("\n")
    
    return move

play()