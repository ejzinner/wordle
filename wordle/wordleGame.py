# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 18:01:04 2022

@author: Evan Zinner-
"""
# Wordle
class WordleGame:
    def __init__(self, truth, maxGuesses = 6):
        self.truth = truth.lower()
        self.numGuesses = 0
        self.maxGuesses = maxGuesses
        self.keyboard = self.initKeyboard()
        
    def guessWordle(self, guess):
        assert(self.numGuesses < self.maxGuesses)
        feedback = scoreWordle(guess, self.truth)
        
        self.keyboard = self.updateKeyboard(guess, feedback)
        self.numGuesses += 1
        return feedback
    

    
def scoreWordle(guess, truth):
    # Scores a guess according to Wordle rules
    # Inputs
    #   guess - the word to be scored
    #   truth - the key to score against
    # Output
    #   feedback - an array of the same length as the input words
    #       0 - letter does not appear in truth
    #       1 - letter appears but not in this position
    #       2 - letter in right position
    
    assert(type(guess) == str)
    assert(type(truth) == str)
    assert(len(guess) == len(truth))
    
    guess = [letter for letter in guess]
    truth = [letter for letter in truth]
    feedback = [0] * len(guess)    
    indicesCorrect = []
    updatedGuess = guess;
    updatedTruth = truth;
    
    for (i, (guessLetter, truthLetter)) in enumerate(zip(guess, truth)):
        if guessLetter == truthLetter:
            feedback[i] = 2
            updatedTruth[i] = ' '
            updatedGuess[i] = ' '
            indicesCorrect.append(i)
            
    for i, letterGuess in enumerate(updatedGuess):
        for j, letterTruth in enumerate(updatedTruth):
            if letterGuess == letterTruth and i not in indicesCorrect:
                feedback[i] = 1
                updatedTruth[j] = ' '
                indicesCorrect.append(i)
    return feedback
                
        
def runTests():
    testHelper('boots', 'boots', [2] * 5)
    testHelper('abcde', 'fghij', [0] * 5)
    testHelper('abcde', 'bcdea', [1] * 5)
    testHelper('aaaaa', 'aaaaa', [2] * 5)
    testHelper('aaaaa', 'aabaa', [2, 2, 0, 2, 2])
    testHelper('', '', [])
    testHelper('boots', 'boot', [2] * 5, True)
    testHelper([1, 2, 3, 4, 5], 'boots', [2] * 5, True)
    testHelper('bootsy', 'bootsy', [2] * 6)
    testHelper('aaabc', 'gadef', [0, 2, 0, 0, 0])
    testHelper('gadef', 'aaabc', [0, 2, 0, 0, 0])
    testHelper('ababa', 'cabaa', [1, 1, 1, 0, 2])
    
def testHelper(guess, truth, expectedAnswer, expectError = False):
    try:
        score = scoreWordle(guess, truth)
    except Exception as e:
        if not expectError:
            print(f'Test case errored with guess {guess} & truth {truth}')
            print(f'Received Error: {e}')
        return    
        
    if not expectedAnswer == score:
        print(f'Test case failed with guess {guess} & truth {truth}')
        print(f'Expected {expectedAnswer}. Actual Value is {score}')
        
 
    
if __name__ == '__main__':
    runTests()
    