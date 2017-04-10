# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 09:16:09 2016

@author: Evan
"""

import os

class GameState:
    def __init__(self,questionNum,hintNum,finishedQuestion,gameScore):
        self.questionNum = questionNum
        self.hintNum = hintNum
        self.finishedQuestion = finishedQuestion
        self.gameScore = gameScore
        
class Question:
    # test
    def __init__(self,questionText,hintList,answerList,clueText,clueAnswer):
        self.questionText = questionText
        self.hintList = hintList
        self.answerList = answerList
        self.clueText = clueText
        self.clueAnswer = clueAnswer

def printFileMessage(fileLoc):
    messageList = fileToList(fileLoc)
    for m in messageList:
        print(m)

def fileToList(fileLoc):
    with open(fileLoc,'r') as file:
        lines = file.readlines()
    return lines

def populateDictFromList(keyValList, separator):
    # I'm mainly storing questions and game states in files
    # In a particular format, so write a function to put the values in a dictionary
    returnDict = {}
    for ln in keyValList:
        key = ln.split(separator)[0]
        value = ln.split(separator)[1].replace('\n',"") #remove the enter symbols
        returnDict[key] = value    
    return returnDict
    
def readGameState(fileLoc):
    gameStateList = fileToList(fileLoc)
    gameDict = populateDictFromList(gameStateList,":")
    # Now convert the game state to numbers, which we'll update / iterate throughout:
    for key, value in gameDict.items():
        gameDict[key] = int(value)
    return gameDict

def readQuestions(directoryLoc,fileList):
    # Build a list of questions - stored as objects or dictionaries - that
    # I will access by the index stored in the game state    
    questionDictList = []
    for f in fileList:
        fileLoc = directoryLoc + '\\' + f
        fileAsList = fileToList(fileLoc)
        questionDict = populateDictFromList(fileAsList, "$$")
        questionDictList += [questionDict]
    return questionDictList
           
def buildQuestions(directoryLoc):
    # Get only the question files
    fileList = os.listdir(directoryLoc)
    fileList = [x for x in fileList if 'question' in x]

    # Now convert the list of question files into a list of questions
    return readQuestions(directoryLoc,fileList)
                
def writeGameState(gameDict, fileLoc):
    # Write the dictionary to the file
    with open(fileLoc, 'w') as f:
        for key,value in gameDict.items():
            textStr = key + ":" + value + '\n'
            f.write(textStr)
    f.close()            

def viewGameState(gameDict):   
    for key, value in gameDict.items():
        print(key + " : " + value)

def askForInput(inputRequest):
    #print("The question is: ")
    print(" ")    
    print(inputRequest)
    return input("Please type your answer and press ENTER: ")

def textClean(inText):
    # Remove spaces and make lower case
    return inText.strip().lower()
    
def askQuestion(question, questionText, answerText, gameState, hintStatus=False):
    questionAnswered = False
    while questionAnswered != True:    
        # Ask for confirmation of the answer
        confirmation = 'NO'
        while confirmation != 'yes':
            # Ask the question, then confirmation
            answer = askForInput(questionText)
            print(" ")
            print("You answered: "  + answer)
            print(" ")
            confirmation = askForInput("Please type 'YES' to confirm")
            confirmation = textClean(confirmation)
            
        # Once we have the answer, sanitize it
        cleanAnswer = textClean(answer)
        # print("Final answer is " + cleanAnswer)
        
        # Check if the answered question is true
        questionAnswered = (answerText in cleanAnswer)
        
        # If the question was wrong and hints needed
        if hintStatus and not questionAnswered:
             gameState['Hint'] += 1 
             gameState['GameScore'] += 1
             if gameState['Hint'] < 3:
                 print(" ")
                 print("You need a hint.  Here you go!")
                 print(question['Hint' + str(gameState['Hint'])])
             else:
                 questionAnswered = True
    
    return gameState
        
def questionStack(gameState, questionList):
    # Ask the question
    question = questionList[gameState['QuestionNumber']]
    questionText = question['Question']
    questionAnswer = question['QuestionAnswerContains']
    gameState = askQuestion(question, questionText, questionAnswer, gameState, hintStatus=True)
    
    # Once the question has been answered, ask for the cipher
    if gameState['Hint'] < 3:
        print("Great!  Now you go look for a clue!")
    else:
        print("Well, you didn't do great on that one.  But the spirit bear intervened!")

    clueText = question['Clue']
    clueAnswer = question['ClueAnswer']
    gameState = askQuestion(question, clueText, clueAnswer, gameState, hintStatus=False)
    
    # When the question is answered and cypher give, update the gamestate 
    # for next question and move on
    print("Congratulations!  The next question awaits you!")         
    gameState['QuestionNumber'] += 1
    gameState['Hint'] = 0
    
    return gameState
    
# Begin Script
if __name__=='__main__':
    # Read in all the questions
    questionFileDir = r'C:\Users\Evan\Documents\Erin\ProposalCode\GameQuestions' 
    questionList = buildQuestions(questionFileDir)      
    
    # Read in the game state file
    inDir = r'C:\Users\Evan\Documents\Erin\ProposalCode'
    gameStateFileLoc = inDir + '\\' + 'game_state.txt'
    currGameState = readGameState(gameStateFileLoc)
    # These are the keys that retrieve the game state
    gameStateKeys = ['Question', 'Hint', 'GameScore']
        
    # Display the welcome message
    welcomeFileLoc = inDir + '\\' + 'welcome_message.txt'
    printFileMessage(welcomeFileLoc)  
    
    # Begin asking questions, but first, need indices
    while currGameState['QuestionNumber'] < len(questionList):
        currGameState = questionStack(currGameState,questionList)
        
    # Reveal the clue
    ringFileLoc = inDir + '\\' + 'ring_location.txt'
    printFileMessage(ringFileLoc)
    print(" ")
    
    # Give the final score
    numDaysUntilGirlfriendAward = 120
    fraction = (len(questionList)*3 - currGameState['GameScore'])/(3*len(questionList))
    daysOff = numDaysUntilGirlfriendAward * fraction
    print("You scored well!  You get " + str(daysOff) + " days off the time until")
    print("your Girlfriend of the Year award!")
    print("You'll have time to win that AND Fiancee of the Year!")