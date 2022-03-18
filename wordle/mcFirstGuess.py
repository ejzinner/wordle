# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:06:20 2022

@author: ejzin
"""

from solveWordle import guessFirstWord
#from collections import Counter

numWordsRemaining = []
for i in range(1000):
    tempWordsRemaining = guessFirstWord('slant', i, 5)
    numWordsRemaining.append(tempWordsRemaining)
    if i % 50 == 0:
        print(i)
maxRemaining = max(numWordsRemaining)
print(f'Max words remaining = {maxRemaining}')
averageRemaining = sum(numWordsRemaining) / len(numWordsRemaining)
print(f'Average words remaining = {averageRemaining}')