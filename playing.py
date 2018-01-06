#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:52:54 2017

@author: lakshya
"""

import numpy as np
import homework as my_agent
import minimax_agent
import random_agent
import time

def isTerminal(board):
    bool_array = board.tolist()
    bool_array = ~np.isnan(bool_array)
    if(np.sum(bool_array)==0):
        return True
    else:
        return False

def play():
    data = [];
    with open("input.txt") as file:
        data = file.read().splitlines()
    
    row = int(data.pop(0))
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
    
    score_1 = 0
    score_2 = 0
    time_1 = 300.0
    time_2 = 300.0
    
    homework_agent = False
    
    while(~isTerminal(board)):
        
        try:
            if(homework_agent):
                start = time.clock()
                move_1 = my_agent.play()
                score_1 = score_1 + move_1[2] * move_1[2]
                time_1 = time_1 - (time.clock() - start)
            else:
                start = time.clock()
                move_2 = minimax_agent.play()
                score_2 = score_2 + move_2[2] * move_2[2]
                time_2 = time_2 - (time.clock() - start)
        except:
            print(time_1, score_1, time_2, score_2)
            return time_1, score_1, time_2, score_2
            break
        
        data = [];
        with open("output.txt") as file:
            data = file.read().splitlines()
        
        move = data.pop(0)
        values = [];
        for val in data:
            val = list(val)
            new_val = [x if x != '*' else 'nan' for x in val]
            values.append(list(new_val))
        
        board = np.array(values, dtype=float)
        
    # =============================================================================
    #     if(~isTerminal(board)):
    #         break
    # =============================================================================
        
        with open("input.txt", 'w+') as file:
            file.write(str(len(board)) + "\n")
            file.write(str(len(type_fruit)) + "\n")
            file.write(str(time_1) + "\n")
            for row in board:
                new_row = []
                for val in row:
                    if np.isnan(val):
                        new_row.append('*')
                    else:
                        new_row.append(str(int(val)))
                file.write(''.join(str(r) for r in new_row))
                file.write("\n")
        
        try:
            if(homework_agent):
                start = time.clock()
                move_2 = minimax_agent.play()
                score_2 = score_2 + move_2[2] * move_2[2]
                time_2 = time_2 - (time.clock() - start)
            else:
                start = time.clock()
                move_1 = my_agent.play()
                score_1 = score_1 + move_1[2] * move_1[2]
                time_1 = time_1 - (time.clock() - start)
        except:
            print(time_1, score_1, time_2, score_2)
            return time_1, score_1, time_2, score_2
            break
        
        data = []
        with open("output.txt") as file:
            data = file.read().splitlines()
        
        move = data.pop(0)
        values = [];
        for val in data:
            val = list(val)
            new_val = [x if x != '*' else 'nan' for x in val]
            values.append(list(new_val))
        
        board = np.array(values, dtype=float)
        
        with open("input.txt", 'w+') as file:
            file.write(str(len(board)) + "\n")
            file.write(str(len(type_fruit)) + "\n")
            file.write(str(time_2) + "\n")
            for row in board:
                new_row = []
                for val in row:
                    if np.isnan(val):
                        new_row.append('*')
                    else:
                        new_row.append(str(int(val)))
                file.write(''.join(str(r) for r in new_row))
                file.write("\n")
                
play()