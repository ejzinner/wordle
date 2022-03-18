# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 20:39:31 2022

@author: ejzin
"""

def initKeyboard():
    keyboard =  {chr(x): -1 for x in range(97, 97+26)}
    return keyboard

def updateKeyboard(keyboard, guess, feedback):
    for (letter, score) in zip(guess, feedback):
        currValue = keyboard.get(letter, 0)
        newValue = max(currValue, score)
        keyboard.update({letter: newValue})
    #print(self.keyboard)
    return keyboard