#ICS3U FSE
#Mona Liu
#Due June 17, 2022

"""
Typing game with two modes and high score
"""

#imports
from pygame import *
from random import *
import time as t    #different name because theres already a time in pygame

#initialize modules
font.init()
mixer.init()



#global colours
BG_CLR = (49, 77, 74)
ACCENT_CLR = (70, 145, 138)
HIGHLIGHT_CLR = (95, 196, 187)
WHITE = (231, 247, 235)
RED = (246, 8, 4)



#import fonts
font25 = font.Font("files/AzeretMono-Regular.ttf", 25)
font20 = font.Font("files/AzeretMono-Regular.ttf", 20)
font40 = font.Font("files/AzeretMono-Regular.ttf", 40)
font60 = font.Font("files/AzeretMono-Regular.ttf", 60)
font28 = font.Font("files/AzeretMono-Regular.ttf", 28)


#import sounds
finishSound = mixer.Sound("files/tada.ogg")
buttonSound = mixer.Sound("files/button.ogg")



#---------ACTION FUNCTIONS-----------

def buttonClick(position, click, button):
    #draws border if mouse is hovering over button
    if button.collidepoint(position[0], position[1]):
        draw.rect(screen, HIGHLIGHT_CLR, button, 2, 10)
        #play sound and returns true if button is clicked
        if click:
            buttonSound.play()
            return True

def drawButton(button, text, font):
    #draws button rectangle and text
    buttonText = font.render(text, True, WHITE)
    draw.rect(screen, ACCENT_CLR, button, 0, 10)
    screen.blit(buttonText, (button.x + 10, button.y + 5))


def drawButtonText(button, text):
    #draws button text only
    buttonText = font25.render(text, True, WHITE)
    screen.blit(buttonText, (button.x + 10, button.y + 5))


def drawArrow(button):
    #draws arrow 20 px before the button
    arrow = font25.render("→", True, WHITE)
    screen.blit(arrow, (button.x - 20, button.y + 5))


def getData(file):
    #opens file from path (reading mode) and reads all lines as list
    dataFile = open(file, "r")
    data = dataFile.readlines()
    dataFile.close()

    #strip white space    
    for i in range(len(data)):
        data[i] = data[i].strip()

    #changes the list into a not-list if there's only one item in it
    if len(data) == 1:
        data = data[0]
        
    return data


def saveData(file, data):
    #open file from path (writing mode)
    dataFile = open(file, "w")

    #writes each element of list as a new line if there is a list
    #otherwise writes the data
    if type(data) == list:
        dataFile.write("\n".join(data))
    else:
        dataFile.write(data)

    #close and save file
    dataFile.close()


def drawCornerInfo(*lines):
    #imitates line breaks using a list of arguments
    #draws each one 30 px below the previous, starting at 20 px
    for i in range(len(lines)):
       infoText = font20.render(lines[i], True, WHITE)
       screen.blit(infoText, (20, 20 + i * 30))


def chooseOptions(settings):
    if settings[0] == "timer":
        options = [[Rect(380, 350, 180, 40), "30 seconds", "30"],
                   [Rect(380, 400, 180, 40), "60 seconds", "60"]]
    else:
        options = [[Rect(380, 350, 148, 40), "25 words", "25"],
                 [Rect(380, 400, 148, 40), "50 words", "50"],
                 [Rect(380, 450, 148, 40), "75 words", "75"]]
    return options



def drawGameSettings(settings, modes, options):
    #draw mode selection buttons (text only)
    for m in modes:
        drawButtonText(m[0], m[1])
        #draw arrow next to it if it's selected
        if settings[0] == m[2]:
            drawArrow(m[0])
    #same for options selection
    for t in options:
        drawButtonText(t[0], t[1])
        #check where to draw arrow based on what mode is selected
        if settings[0] == "timer":
            if settings[1] == t[2]:
                drawArrow(t[0])
        else:
            if settings[2] == t[2]:
                drawArrow(t[0])

                
       
def getWords(file, num):
    #open word list (reading mode) and get all words as a list
    wordFile = open(file, "r")
    allwords = wordFile.readlines()
    wordFile.close()

    #adds a randomly selected word from the list to new list until
    #   it reaches the set number
    words = []
    while len(words) < num:
        word = choice(allwords)
        #make sure it's not already been picked
        if word not in words:
            words.append(word.strip())

    return words


def makeGame(settings):
    global timer, wordcount, wordlist
    #if start game is clicked, get time and number of words from settings
    timer = int(settings[1])
    wordcount = int(settings[2])

    #change wordcount if it's timer mode and set timer to start at 0
    #   if it's stopwatch mode
    if settings[0] == "timer":
        wordcount = 100
    else:
        timer = 0

    #generate wordlist
    wordlist = getWords("files/wordlist.txt", wordcount)


def drawWordList(wordlist, index):
    #draws list of prompt words starting at current word
    #check that the end of the list hasn't been reached
    if index < len(wordlist):
        for i in range(len(wordlist[index:])):
            #each word is 60px below the previous, with the first one at 100px
            y = 100 + i * 60
            #only draw the words that are on screen
            if y < 700:
                #make text object and set as semi transparent
                wordText = font40.render(wordlist[index:][i], True, WHITE)
                wordText.set_alpha(150)
                screen.blit(wordText, (100, y))


def drawTypedWord(prompt, typed):
    #draws each letter in the currently typed word
    for i in range(len(typed)):
        #sets letter colour as white if it's correct and red if it isn't
        #extra letters are red if the typed word is longer than the prompt
        if i < len(prompt) and typed[i] == prompt[i]:
            colour = WHITE
        else:
            colour = RED

        #each letter is 26px to the right of the previous
        letterText = font40.render(typed[i], True, colour, BG_CLR)
        screen.blit(letterText, (100 + i * 26, 100))
        

def toMinutes(seconds):
    #changes seconds to minute format with double digits using string formatting
    #get minutes using integer division and remaining seconds using modulus
    return "%02i:%02i" %(seconds // 60, seconds % 60)


def drawTimer(elapsed, settings):
    #get time left and display if game is in timer mode
    if settings[0] == "timer":
        timeLeft = timer - elapsed
        timerText = font25.render(toMinutes(timeLeft), True, WHITE)
    #get time passed if game is in stopwatch mode
    else:
        timerText = font25.render(toMinutes(elapsed), True, WHITE)
    #draws timer in minute format at (400, 50)
    screen.blit(timerText, (400, 50))
            


def getCharacters(wordlist):
    characters = 0
    
    #counts number of characters in a list of strings by adding the length
    #   of each string to a counter
    for word in wordlist:
        characters += len(word)
        
    return characters


def getErrors(promptlist, wordlist, time):
    errors = 0

    #compares each letter in each word in the typed wordlist to the prompt
    #   wordlist and adds one to the counter if it is not the same or longer
    #   than the prompt
    for i in range(len(wordlist)):
        for j in range(len(wordlist[i])):
            if j >= len(promptlist[i]) or wordlist[i][j] != promptlist[i][j]:
                errors += 1

    #calculates average errors per minute                
    return errors, errors / (time / 60)


def getSpeed(wordlist, time, errors):
    #calculates characters per minute
    cpm = getCharacters(wordlist) / (time / 60)

    #calculates words per minute by dividing characters by 5 (for an
    #   average word length) and subtracting errors
    wpm = getCharacters(wordlist) / 5 / (time / 60) - errors
    
    return cpm, wpm


def getAccuracy(wordlist, errors):
    #calculates percentage wrong by dividing errors over total number of
    # characters
    frac = errors / getCharacters(wordlist)

    #calculate percentage CORRECT by subtracting percentage wrong from one
    #returns as a percentage (multiply by 100)
    return (1 - frac) * 100


def drawGameEnd(mode, settings):
    #draws "game complete" text and the mode and settings of the game
    screen.blit(font60.render("Game Complete", True, WHITE), (50, 50))
    screen.blit(font25.render(mode, True, WHITE), (70, 130))
    screen.blit(font25.render(settings, True, WHITE), (350, 130))


def drawResults(wpm, cpm, errors, accuracy):
    #2d list of results, each element has a "number" (actual result)
    #   and a "label" (smaller text to tell user what the result means)
    results = [["%.0f" %wpm, "WPM"],
               ["%.0f" %cpm, "CPM"],
               ["%.1f%%" %accuracy, "accuracy"],
               [str(errors), "errors"]]

    #draws results in a 2 line 2 column format (since there are 4)
    for i in range(len(results)):
        
        #sets x position based on whether the index is even (0, 2 and 1, 3)
        x = 100 + (i % 2) * 300

        #sets y position based on whether the index is first or second half
        #   (0, 1 and 2, 3)
        if i <= 1:
            y = 200
        else:
            y = 350

        #draw "result" text and "label" text separately
        #the label text is 70px below the result text
        resText = font60.render(results[i][0], True, WHITE)
        bottomText = font25.render(results[i][1], True, WHITE)
        screen.blit(resText, (x, y))
        screen.blit(bottomText, (x, y + 70))
    




#---------SCREEN FUNCTIONS----------

#instruction screen
def instructions():

    #exit button (rect, text, destination)
    close = [Rect(550, 10, 36, 40), "X", "home"]

    running = True

    #load & blit instructions image
    img = image.load("files/instructions.png")
    screen.blit(img,(0,0))
    

    while running:

        #variable for left click
        leftClick = False
        
        for evt in event.get():

            #close game if user presses close button
            if evt.type == QUIT:
                return "exit"

            #gets left click
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1:
                    leftClick = True


        #get mouse location
        mX,mY = mouse.get_pos()

        #draw close button
        drawButton(close[0], close[1], font25)
        
        #goes to home screen if close button is clicked        
        if buttonClick((mX, mY), leftClick, close[0]):
            return "home"

        display.flip()


    
#game screen
def game():
    #allow function to modify word counter, elapsed time counter, and list of
    #   typed words
    global counter, elapsed, typedwords
        
    #reset game variables except the prompt wordlist
    counter = 0
    elapsed = 0
    typedwords = []

    #exit button (rect, text, destination)
    close = [Rect(550, 10, 36, 40), "X"]

    #current typed word
    word = ""

    #get starting time
    start = t.time()

    running = True

    
    while running:

        #variable for left click
        leftClick = False

        for evt in event.get():

            #close game if user presses close button
            if evt.type == QUIT:
                return "exit"

            #get left click
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1:
                    leftClick = True

            #get key presses
            if evt.type == KEYDOWN:

                #add word to the list of typed words, current position counter,
                #   and clear current word when space key is pressed
                if evt.key == K_SPACE:
                    typedwords.append(word)
                    counter += 1
                    word = ""

                #remove last letter using slicing if backspace is pressed
                elif evt.key == K_BACKSPACE:
                    word = word[:-1]

                #add letter to current word if a letter key is pressed
                elif evt.unicode.isalpha():
                    word += evt.unicode

                            
        #get mouse location
        mX,mY = mouse.get_pos()

        screen.fill(BG_CLR)

        #draw game mode and setting
        drawCornerInfo(gameMode, gameInfo)

        #draw close button
        drawButton(close[0], close[1], font25)

        #goes to home screen if close button is clicked        
        if buttonClick((mX, mY), leftClick, close[0]):
            return "home"


        #draw line under first word prompt/current typed word                
        draw.line(screen, ACCENT_CLR, (50, 150), (550, 150), 5)

        #draw prompt wordlist
        drawWordList(wordlist, counter)

        #draw current typed word if it hasn't reached the end of the list
        if counter < len(wordlist):
            drawTypedWord(wordlist[counter], word)
        

        if word == "" and typedwords == []:
            #reset starting time if user hasn't typed anything
            start = t.time()

        #get elapsed time and draw timer
        elapsed = int(t.time() - start)
        drawTimer(elapsed, settings)

        
        #go to results screen if time reaches 0
        if settings[0] == "timer" and elapsed >= timer:
            typedwords.append(word)
            return "results"

        #go to results screen if end of wordlist is reached
        if settings[0] == "stopwatch" and counter >= wordcount:
            return "results"

        display.flip()



#results screen
def results():
    #modify highscore
    global highscore

    #variables for errors, errors per min,
    #   characters per min, words per min
    #   and accuracy
    errors, epm = getErrors(wordlist, typedwords, elapsed)
    cpm, wpm = getSpeed(typedwords, elapsed, epm)
    accuracy = getAccuracy(typedwords, errors)

    #2D list of buttons for options (rect, text)
    buttons = [[Rect(254, 498, 110, 43), "Retry"],
               [Rect(236, 548, 146, 43), "Restart"]]
    close = [Rect(267, 600, 84, 40), "Exit"]

    #load high score image
    newHighScoreImg = image.load("files/newhs.png")

    #check if highscore has been beat and set new highscore
    newhs = False
    if wpm > float(highscore):
        highscore = wpm
        newhs = True
        #play sound
        finishSound.play()

    running = True

    while running:
        
        #variable for left click
        leftClick = False

        for evt in event.get():

            #close game if user presses close button
            if evt.type == QUIT:
                return "exit"

            #get left click
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1:
                    leftClick = True

        #get mouse location
        mX,mY = mouse.get_pos()

        screen.fill(BG_CLR)

        #draw game ended header and results
        drawGameEnd(gameMode, gameInfo)
        drawResults(wpm, cpm, errors, accuracy)

        #display "new high score" if needed
        if newhs:
            screen.blit(newHighScoreImg, (100, 170))

        #draw buttons
        for b in buttons:
            drawButton(b[0], b[1], font28)
        drawButton(close[0], close[1], font25)


        #go back to game if "retry" is clicked
        if buttonClick((mX, mY), leftClick, buttons[0][0]):
            return "game"

        #go back to home is "restart" is clicked
        elif buttonClick((mX, mY), leftClick, buttons[1][0]):
            return "home"

        # close if "exit" is clicked
        elif buttonClick((mX, mY), leftClick, close[0]):
            return "exit"


        display.flip()


        
#home screen
def home():
    #modify global variables
    global settings, highscore, wordlist, timer, wordcount

    #load logo
    logo = image.load("files/logo.png")
    
    #main buttons (rect, text)
    start = [Rect(150, 531, 280, 58), "Start Game"]
    instr = [Rect(550, 10, 36, 40), "?"]
    clear = [Rect(20, 80, 80, 35), "Clear"]

    #2D list of settings buttons (rect, text, identifier for saving)
    modes = [[Rect(60, 350, 180, 40), "Timer Mode", "timer"],
             [Rect(60, 400, 244, 40), "Stopwatch Mode", "stopwatch"]]



    running = True
    
    while running:
        #variable for left click
        leftClick = False

        for evt in event.get():

            #close game if user presses close button
            if evt.type == QUIT:
                return "exit"

            #get left click
            if evt.type == MOUSEBUTTONDOWN:
                if evt.button == 1:
                    leftClick = True
                    

        #get mouse location
        mX,mY = mouse.get_pos()

        screen.fill(BG_CLR)
        screen.blit(logo, (40, 80))

        #draw start and help buttons
        drawButton(start[0], start[1], font40)
        drawButton(instr[0], instr[1], font25)
        
                    

        #change game settings selection options depending on mode
        options = chooseOptions(settings)

        #draw game settings
        drawGameSettings(settings, modes, options)

        #draw highscore and highscore clear button
        drawCornerInfo("HIGHSCORE:", "%.0f WPM" %highscore)
        drawButton(clear[0], clear[1], font20)

        #change mode and option settings if user clicks it
        for m in modes:
            if buttonClick((mX, mY), leftClick, m[0]):
                settings[0] = m[2]
        for t in options:
            if buttonClick((mX, mY), leftClick, t[0]):
                if settings[0] == "timer":
                    settings[1] = t[2]
                else:
                    settings[2] = t[2]


        if buttonClick((mX, mY), leftClick, start[0]):
            #change global game settings and go to game screen if
            #   "start game" is clicked
            makeGame(settings)
            return "game"

        elif buttonClick((mX, mY), leftClick, instr[0]):
            #go to instructions screen if help button is clicked
            return "instructions"
        
        elif buttonClick((mX, mY), leftClick, clear[0]):
            #clear highscore if clear button is clicked
            highscore = 0
            

        display.flip()



#--------------------------------
#set up screen
width,height = 600,700
screen = display.set_mode((width,height))

#change window title
display.set_caption("TypeThing - 2022 ICS3U FSE")

#load and change window icon
gameIcon = image.load("files/icon.png")
display.set_icon(gameIcon)


#get highscore and settings from file
settings = getData("files/settings.txt")
highscore = float(getData("files/highscore.txt"))


#game variables for generated words, typed words,
#   word position counter, and elapsed time
wordlist = []
typedwords = []
counter = 0
elapsed = 0


#start at home page
page = "home"

#keep running game unless user clicks close/exit
while page != "exit":
    
    if page == "home":
        page = home()
        
    if page == "instructions":
        page = instructions()
        
    if page == "game":
        #set up game mode variables before starting
        if settings[0] == "timer":
            gameMode = "TIMER MODE"
            gameInfo = str(timer) + " seconds"
        else:
            gameMode = "STOPWATCH MODE"
            gameInfo = str(wordcount) + " words"
        page = game()
        
    if page == "results":
        page = results()


#save highscore and settings on exit
saveData("files/highscore.txt", str(highscore))
saveData("files/settings.txt", settings)

quit()
