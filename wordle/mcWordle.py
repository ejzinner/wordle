# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 21:28:59 2022

@author: ejzin
"""

from solveWordle import playWordle
from collections import Counter

numGuesses = []
for i in range(1000):
    numGuess = playWordle('snarl', i)
    numGuesses.append(numGuess)
    if i % 50 == 0:
        print(i)
c = Counter(numGuesses)
