#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 20:07:56 2017

@author: lakshya
"""

import random
import numpy as np

def makeBoard(size, type_fruits):
    #size = 1
    #type_fruits = 1
    
    board = np.random.randint(type_fruits, size=(size,size))
    #print board
        
    with open("input.txt","w") as file:
        file.write(str(len(board)) + "\n")
        file.write(str(type_fruits))
        file.write("\n")
        file.write(str(300) + "\n")
        for row in board:
            new_row = []
            for val in row:
                new_row.append(val)
            file.write(''.join(str(r) for r in new_row))
            file.write("\n")

makeBoard(26,2)