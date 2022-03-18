# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 07:28:38 2022

@author: ejzin
"""
from wordleGame import WordleGame
from collections import Counter
from nltk.corpus import words
import random



if __name__ == '__main__':
    pass

def playWordle(firstGuess = 'snarl', randomSeed = 1):
    numLetters = len(firstGuess)
    wordList = generateWordList(numLetters)
    random.seed(randomSeed) 
    truthInt = random.randint(0, len(wordList))
    truth = wordList[truthInt]
    #print(truth)
    game = WordleGame(truth)
    
    instancesPerLetter = initInstancesPerLetter()
    optsPerIndex = initOptsPerIndex()
    
    feedback = [0] * numLetters
    perfectFeedback = [2] * numLetters
    countGuesses = 0
    while not feedback == perfectFeedback:
        countGuesses += 1
        # print(countGuesses)
        # is this len business the best way to check isEmpty()
        if countGuesses == 1: 
            guess = firstGuess
        else:
            '''# We should make the algorithm for choosing the next 
            guess a function that we pass in'''            
            #guess = generateGuess(wordList, instancesPerLetter, optsPerIndex)
            guess, wordList = generateMostCommonGuessV2(wordList, instancesPerLetter, optsPerIndex)
        # print(guess)
        feedback = game.guessWordle(guess)
        # print(feedback)
        instancesPerLetter = updateInstancesPerLetter(guess, feedback, instancesPerLetter)
        optsPerIndex = updateOptsPerIndex(optsPerIndex, guess, feedback)
        # print(instancesPerLetter)
    return countGuesses


def guessFirstWord(firstGuess = 'aalii', randomSeed = 1, numLetters = 5):
    # Tries a first guess against a random truth word
    # Returns the number of possible words in the word list after the first guess
    
    #generate random truth word
    wordList = generateWordList(numLetters)
    random.seed(randomSeed) 
    truthInt = random.randint(0, len(wordList))
    truth = wordList[truthInt]

    #initialize the game and the playing logic
    game = WordleGame(truth)
    instancesPerLetter = initInstancesPerLetter()
    optsPerIndex = initOptsPerIndex()
    
    #try the first word, update playing logic, count number of possible guesses
    feedback = game.guessWordle(firstGuess)
    instancesPerLetter = updateInstancesPerLetter(firstGuess, feedback, instancesPerLetter)
    optsPerIndex = updateOptsPerIndex(optsPerIndex, firstGuess, feedback)
    numPossibleGuesses = countPossibleGuesses(wordList, instancesPerLetter, optsPerIndex)
    return numPossibleGuesses


def generateMostCommonGuess(wordList, rangeInstancesPerLetter, optsPerIndex):
    numEachLetter = {chr(x): 0 for x in range(97, 97+26)}
    newWordList = []
    # find the possible words, look at the which letters are most frequent in these words
    for word in wordList:
        if isGuessPossible(word, rangeInstancesPerLetter, optsPerIndex):
            newWordList.append(word)
            for letter in word:
                numEachLetter[letter] = numEachLetter[letter] + 1
    #numVowels = numEachLetter[a] + numEachLetter[e] + numEachLetter[i] + numEachLetter[o] + numEachLetter[u] + numEachLetter[a]
    # for each possible word, score how 'common' the word is based on how common each letter is
    wordCommonalityScores = []
    for word in newWordList:
        score = 0
        for letter in word:
            score = score + numEachLetter[letter]
        wordCommonalityScores.append(score)
    index = wordCommonalityScores.index(max(wordCommonalityScores))    
    return newWordList[index]

def generateMostCommonGuessV2(wordList, rangeInstancesPerLetter, optsPerIndex):
    numEachLetter = {chr(x): 0 for x in range(97, 97+26)}
    newWordList = []
    # find the possible words, look at the which letters are most frequent in these words
    # prefer consonants to vowels
    # don't count the frequency from subsequent instances of a letter
    for word in wordList:
        if isGuessPossible(word, rangeInstancesPerLetter, optsPerIndex):
            newWordList.append(word)
            for letter in word:
                numEachLetter[letter] = numEachLetter[letter] + 1
    
    for letter in numEachLetter:
        pass
    
    # for each possible word, score how 'common' the word is based on how common each letter is
    wordCommonalityScores = []
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    for word in newWordList:
        c = Counter(word) #iterate over Counter to avoid rewarding multiple letters
        score = 0
        for letter in c:
            if letter in vowels: #give less points for vowels, 4 is arbitrary
                score = score + (numEachLetter[letter] / 4)
            if not letter in vowels: 
                score = score + numEachLetter[letter]
            
        wordCommonalityScores.append(score)
    index = wordCommonalityScores.index(max(wordCommonalityScores))    
    return newWordList[index], newWordList


def generateWordList(numLetters = 5):
    #list comprehension
    wordList = [word.lower() for word in words.words() if len(word) == 5]
    return wordList

def generateGuess(wordList, rangeInstancesPerLetter, optsPerIndex):
    # iterates through the word list until it finds a word that can be the truth
    for word in wordList:
        if isGuessPossible(word, rangeInstancesPerLetter, optsPerIndex):
            return word
        

def isGuessPossible(guess, rangeInstancesPerLetter, optsPerIndex):
    c = Counter(guess)
    for (letter, letterBank) in zip(guess, optsPerIndex):
        if not letter in letterBank:
            return False
        
    for letter in rangeInstancesPerLetter:
        numOccurences = c[letter]
        minInstances = rangeInstancesPerLetter[letter][0]
        maxInstances = rangeInstancesPerLetter[letter][1]
        if numOccurences < minInstances or numOccurences > maxInstances:
            return False
        
    return True    
   
def countPossibleGuesses(wordList, rangeInstancesPerLetter, optsPerIndex):
    count = 0
    for word in wordList:
        if isGuessPossible(word, rangeInstancesPerLetter, optsPerIndex):
            count += 1
    return count

def initOptsPerIndex(numLetters = 5):
    # This is a list of n dictionaries of letters
    # When initialized each dictionary has all letters
    # When letters can no longer occur at that index, they will be removed from the dict
    # the value associated with a letter means nothing, only whether it is present in dict matters
    
    # optsPerIndex = [{chr(x) for x in range(97, 97+26)} for letter in range(numLetters)]
    optsPerIndex = []
    for letter in range(numLetters):    
        # set comprehension
        optsPerIndex.append({chr(x) for x in range(97, 97+26)})
    return optsPerIndex
    
def initInstancesPerLetter(numLetters = 5):
    rangeInstancesPerLetter = {chr(x): [0, numLetters] for x in range(97, 97+26)}
    return rangeInstancesPerLetter

def updateInstancesPerLetter(guess, output, rangeInstancesPerLetter):
    lettersIveSeen = {chr(x): 0 for x in range(97, 97+26)}
    lettersNotIn = set()
    for (letter, score) in zip(guess, output):
        if score > 0:
            lettersIveSeen[letter] = lettersIveSeen.get(letter, 0) + 1
        else: # score == 0
            lettersNotIn.add(letter)
    
    for letter in lettersIveSeen:
        newMin = max(rangeInstancesPerLetter[letter][0], lettersIveSeen[letter])
        rangeInstancesPerLetter[letter][0] = newMin
        
    for letter in lettersNotIn:
        if not letter in lettersIveSeen:
            newMax = 0
        else:
            newMax = lettersIveSeen[letter]
        rangeInstancesPerLetter[letter][1] = newMax
        
    return rangeInstancesPerLetter        

def updateOptsPerIndex(optsPerIndex, guess, output):  
    lettersIveSeenOne = set()
    for (i, (letter, score)) in enumerate(zip(guess, output)):
        if score == 2:
            #at this index in optsPerIndex, remove all other letters
            #I do this by remove all letters, then adding back the one thats correct
            optsPerIndex[i].clear()
            optsPerIndex[i].add(letter)
        elif score == 1:
            lettersIveSeenOne.add(letter)            
            #since it is not a 2, it cannot be this letter at this index
            #the only thing this explicitly tells us is that this letter cannot be in thisindex
            optsPerIndex[i].remove(letter) #From the ith dictionary in optsPerIndex, remove the key for this letter
        elif score == 0:
            letterBank = optsPerIndex[i]
            if letter in letterBank:
                letterBank.remove(letter)
            #lettersIveSeen[letter] = 0
            if not letter in lettersIveSeenOne:
                for letterBank in optsPerIndex[i:]:
                    if letter in letterBank:
                        letterBank.remove(letter)
        else:
            raise ValueError('What happened? Must be 0, 1, or 2')
    return optsPerIndex

def runTests():
    testIsGuessPossible('water', [0,0,0,0,0], 'water', False)
    testIsGuessPossible('water', [0,0,0,0,0], 'sinch', True)
    testIsGuessPossible('boooo', [0,2,1,0,0], 'loops', False) # cannot be o in second 
    testIsGuessPossible('boooo', [0,2,1,0,0], 'oozie', True)
    testIsGuessPossible('abcde', [1,0,0,0,0], 'fghij', False) #There must be an a
    testIsGuessPossible('abcde', [1,0,0,0,0], 'fahij', True)
    testIsGuessPossible('abcde', [1,0,0,0,0], 'aghij', False) #'a' cannot be zeroth
    testIsGuessPossible('aabcd', [1,0,0,0,0], 'zzazz', True)
    testIsGuessPossible('aabcd', [1,0,0,0,0], 'zzaaz', False) # can only be 1 a
    testIsGuessPossible('water', [2,2,2,2,2], 'water', True)
    testIsGuessPossible('water', [2,2,2,0,0], 'watch', True)
    testIsGuessPossible('water', [2,0,0,2,2], 'wiper', True)   
    print('You ran the tests')
    
    
def testIsGuessPossible(firstGuess, feedback, secondGuess, expectedAnswer, expectError = False):
    try:
        instancesPerLetter = initInstancesPerLetter()
        instancesPerLetter = updateInstancesPerLetter(firstGuess, feedback, instancesPerLetter)
        optsPerIndex = initOptsPerIndex()
        optsPerIndex = updateOptsPerIndex(optsPerIndex, firstGuess, feedback)
        isPossible = isGuessPossible(secondGuess, instancesPerLetter, optsPerIndex)

    except Exception as e:
        if not expectError:
            print(f'Test case errored with first guess {firstGuess}, feedback {feedback}, and second guess {secondGuess}')
            print(f'Received Error: {e}')
        return    
        
    if not isPossible == expectedAnswer:
        print(f'Test case failed with first guess {firstGuess}, feedback {feedback}, and second guess {secondGuess}')
        print(f'Expected {expectedAnswer}. Actual Value is {isPossible}')
 
    
if __name__ == '__main__':
    runTests()