#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 17:02:26 2017

@author: lakshya
"""

import numpy as np
import copy
import random

class Player:
    
    def __init__(self, number, score):
        self.num = number
        self.score = score

player_1 = Player(1,0)
player_2 = Player(2,0)

# Utility functions to count fruits matrix
class Utility:
 
    def __init__(self, row, col, g):
        self.ROW = row
        self.COL = col
        self.board = g
 
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


    def setBoard(self, board):
        self.board = copy.deepcopy(board)
        
    def countFruits(self, num_fruit):

        # Initially all cells are unvisited
        visited = [[False for j in range(self.COL)]for i in range(self.ROW)]
 
        #Count to keep track of position of fruits, their type and count
        count = []
        for type_fruit in num_fruit:
            for i in range(self.ROW):
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

def play():
    data = [];
    with open("input.txt") as file:
        data = file.read().splitlines()
    
    type_fruit = int(data.pop(0))
    time_rem = float(data.pop(0))
    
    values = [];
    for val in data:
        val = list(val)
        new_val = [x if x != '*' else 'nan' for x in val]
        values.append(list(new_val))
    
    board = np.array(values, dtype=float)
    
    type_fruit = board.flatten().tolist()
    
    type_fruit = list(set(type_fruit))
    
    row = len(board)
    col = len(board[0])
        
    g= Utility(row, col, board)

    moves = g.countFruits(type_fruit)
    
    move_made = moves[random.randint(0, len(moves)-1)]
    #print("--- %s seconds ---" % (time.clock() - start))
    g.dropFruits(move_made[0][0], move_made[0][1], move_made[1])
    score = move_made[1]*move_made[1]
    #print move
    #print g.board
    
    with open("output.txt", 'w+') as file:
        for row in g.board:
            new_row = []
            for val in row:
                if np.isnan(val):
                    new_row.append('*')
                else:
                    new_row.append(str(int(val)))
            file.write(''.join(str(r) for r in new_row))
            file.write("\n")
    
    return move_made