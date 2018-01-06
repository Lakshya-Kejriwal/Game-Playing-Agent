#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 14:24:04 2017

@author: lakshya
"""

import numpy as np
import copy
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

def min_value(board, type_fruit, alpha, beta, score_1, score_2, depth, num_moves, depth_reduced, start):
    if isTerminal(board):
        return utilityScore(score_1, score_2)
    
    infinity = float('inf')
    value = infinity
    
    utility = Utility(len(board), len(board[0]), copy.deepcopy(board))
    
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
        
    if num.count(1) > 20 and possible[0][2] >= 1:
        if not depth_reduced:
            if num.count(1) >= 50:
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
    
    
    for moves in possible:
        utility.setBoard(board)
        utility.dropFruits(moves[0][0], moves[0][1], moves[1])
        
        new_score2 = score_2 + moves[2]*moves[2]
        value = time.clock() - start
        

        return value


def alpha_beta(board, type_fruit, time_rem, start):
    infinity = float('inf')
    alpha = -infinity
    beta = infinity
     
    utility = Utility(len(board), len(board[0]), copy.deepcopy(board))
    
    utility.reduceBoard()
    possible_moves = utility.countFruits(type_fruit)
    possible_moves.sort(key=lambda x:x[2], reverse=True)
    
    time_node = 0.008
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
    elif time_rem >= 50:
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
    
    if len(possible) <= 15:
        depth = depth + 1
    
    if time_rem <= 50 and time_rem > 10:
        depth = 3
        num_moves = 10
        possible = possible[:num_moves]
    elif time_rem <= 10:
        depth = 2
        num_moves = 5
        possible = possible[:num_moves]

    for moves in possible:
        utility.setBoard(board)
        utility.dropFruits(moves[0][0], moves[0][1], moves[1])
        score_1 = moves[2]*moves[2]
        
        value = min_value(utility.board, type_fruit, alpha, beta, score_1, 0, depth-1, num_moves, depth_reduced, start)
    
        return value
    
    

board = np.array([[4, 6, 8, 3, 5, 3, 4, 2, 8, 9, 4, 1, 6, 7, 7, 8, 4, 5, 9, 8, 0, 7,
        9, 6, 1, 5],
       [5, 8, 6, 6, 3, 5, 9, 3, 5, 2, 6, 9, 3, 3, 0, 9, 7, 2, 6, 5, 2, 1,
        5, 7, 4, 5],
       [6, 7, 4, 9, 7, 5, 8, 9, 5, 6, 2, 0, 1, 4, 8, 7, 4, 6, 8, 1, 9, 5,
        4, 5, 2, 5],
       [0, 2, 9, 2, 1, 2, 8, 3, 4, 9, 3, 0, 3, 6, 9, 0, 7, 9, 2, 0, 7, 3,
        5, 9, 1, 6],
       [5, 1, 4, 1, 3, 0, 4, 6, 9, 2, 3, 5, 9, 3, 4, 9, 1, 1, 6, 0, 5, 2,
        4, 2, 0, 4],
       [9, 7, 4, 5, 9, 1, 9, 2, 0, 2, 8, 4, 4, 2, 9, 3, 4, 5, 0, 5, 1, 0,
        4, 2, 1, 4],
       [9, 0, 9, 9, 2, 4, 2, 6, 8, 2, 9, 2, 9, 5, 8, 6, 2, 3, 8, 5, 6, 6,
        9, 2, 3, 5],
       [1, 4, 7, 9, 3, 0, 2, 2, 7, 2, 6, 0, 0, 6, 9, 8, 1, 8, 4, 1, 6, 3,
        4, 1, 7, 4],
       [9, 6, 0, 6, 0, 0, 4, 7, 5, 2, 2, 7, 7, 7, 7, 2, 0, 1, 3, 9, 9, 4,
        6, 7, 4, 9],
       [7, 9, 0, 8, 8, 0, 6, 7, 4, 5, 3, 4, 5, 3, 5, 0, 7, 2, 9, 9, 5, 7,
        5, 2, 0, 0],
       [9, 4, 8, 6, 2, 0, 4, 8, 4, 2, 5, 5, 9, 6, 7, 9, 7, 4, 8, 3, 9, 0,
        0, 5, 4, 8],
       [8, 1, 8, 1, 1, 2, 9, 7, 5, 0, 4, 5, 4, 7, 0, 2, 1, 9, 1, 0, 2, 5,
        5, 7, 1, 7],
       [1, 2, 1, 3, 4, 3, 5, 1, 0, 5, 8, 0, 3, 1, 2, 4, 1, 0, 4, 1, 5, 9,
        7, 7, 4, 2],
       [0, 7, 8, 2, 8, 9, 2, 5, 6, 6, 0, 3, 0, 4, 2, 1, 7, 7, 5, 5, 4, 8,
        0, 3, 8, 5],
       [1, 8, 8, 7, 0, 6, 4, 8, 5, 7, 9, 2, 2, 8, 4, 2, 4, 0, 7, 6, 6, 5,
        3, 1, 4, 5],
       [9, 0, 9, 9, 8, 3, 2, 8, 7, 0, 9, 3, 9, 5, 1, 0, 1, 8, 3, 2, 3, 4,
        3, 4, 2, 4],
       [7, 5, 8, 4, 9, 6, 9, 4, 4, 3, 8, 2, 6, 1, 4, 3, 0, 1, 4, 9, 5, 4,
        4, 5, 8, 0],
       [9, 4, 1, 9, 4, 0, 7, 7, 3, 4, 1, 8, 6, 3, 3, 9, 2, 6, 6, 0, 2, 1,
        5, 6, 5, 8],
       [5, 3, 7, 3, 5, 8, 1, 1, 7, 1, 0, 1, 8, 4, 6, 7, 4, 6, 6, 4, 9, 1,
        8, 4, 7, 0],
       [9, 9, 6, 4, 4, 1, 4, 8, 7, 9, 1, 6, 6, 9, 5, 2, 5, 5, 0, 2, 2, 0,
        0, 2, 8, 5],
       [2, 9, 4, 9, 7, 5, 4, 5, 2, 9, 8, 5, 6, 2, 5, 9, 9, 8, 4, 6, 0, 2,
        3, 0, 3, 2],
       [8, 9, 8, 5, 7, 8, 2, 7, 3, 9, 8, 4, 3, 0, 3, 0, 3, 9, 4, 3, 2, 6,
        2, 3, 5, 5],
       [1, 5, 1, 5, 3, 6, 1, 8, 0, 5, 9, 4, 1, 0, 5, 6, 8, 7, 2, 5, 5, 6,
        6, 0, 4, 3],
       [5, 7, 9, 0, 7, 6, 8, 8, 2, 7, 5, 7, 6, 5, 7, 2, 6, 0, 9, 6, 6, 8,
        0, 6, 6, 7],
       [0, 4, 5, 8, 5, 3, 3, 6, 3, 1, 5, 3, 2, 3, 9, 5, 6, 1, 7, 3, 8, 8,
        6, 7, 9, 2],
       [2, 0, 4, 3, 8, 9, 9, 3, 5, 8, 0, 9, 8, 1, 1, 4, 6, 4, 3, 2, 0, 6,
        9, 4, 4, 0]], dtype=float)

type_fruit = board.flatten().tolist()
type_fruit = [fruit for fruit in type_fruit if ~np.isnan(fruit)]

type_fruit = list(set(type_fruit))

row = len(board)
col = len(board[0])

start = time.clock()
time = alpha_beta(board, type_fruit, 300.0, start)

with open("calibrate.txt", 'w+') as file:
    file.write(str(time))
 