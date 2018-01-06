#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 19:20:56 2017

@author: lakshya
"""

import board_generator
import playing

for size in range(23, 26):
    for fruits in range(2, 11):
        board_generator.makeBoard(size, fruits)
        print(size, fruits)
        time_1, score_1, time_2, score_2 = playing.play()
        with open("test.txt", "a") as myfile:
            myfile.write(str(size) + " " + str(fruits) + "\n")
            myfile.write(str(time_1) + " " + str(score_1) + " " + str(time_2) + " " + str(score_2) + "\n")