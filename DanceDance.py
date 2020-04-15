import pygame
import pygame.freetype
import math


"""
Each menu and/or gameplay is a class in itself
This is to help with debugging and creating entirely new sets all together
Ff I want to make something similar to a current build,
                            I will design either a class or a function for that design

The Game class is there just to hold a few varialbes, and let the classes see what's happening                          Done
The mainMenu class is as the name suggests, a main menu                                                                 (next menu)

The Selection class is the class that handles selecting a song for the user to play                                     (gui, getFiles, selection, next menu)
The playSong class is the class that actually dictates what to show on screen when playing a songs                      (gui, keys, "scoring system"[tbd])
            It is also the class that upacks a the files and reads them to create the song notes on screen
The songOverlay class is the overlay of the screen when the user is playing a song                                      (gui, options buttons, esc key)
The songSound class is to designate what sound file is being played at the current time,                                (sound files, create sound)
                there will only be one songSound class in existance at a time (global)


ToDo:
    selection class:
        create gui
        create getfilesinfo function
        create a selection system for songs after getfiles
        send to next menu
    
    playSong class:
        create gui (just the scoring zone and notes)
        create key functions, to get the input
        create some "scoring system":
            player types key < time than maximum and > than minimum
                right note
            player doesn't:
                wrong note
    
    songOverlay class:
        Gui (extra stuff including background, the atmosphere, ext)
        options button
        create esc key sequence for exit (another class???)
    
    songSound class:
        look for specific file
        play specific file when told to
        if there is another specific file that is a song:
            stop playing current song and play the specific file song
"""



class Game: # game class that controls the game
    
    def __init__(self): # start the game by going to the main menu
        self.mode = "main menu"
        self.currentMode = mainMenu()
    
    def getMode(self): # get the string of the mode
        return self.mode
    
    def draw(self): # draw the game, whatever it may be
        self.currentMode.draw()
    
    def setMode(self, newMode, song=""):
        self.mode = newMode
        if newMode == "selection":
            self.currentMode = Selection("songList.txt")
        elif newMode == "main menu":
            self.currentMode = mainMenu()
        elif newMode == "play song":
            self.currentMode = playSong(song)


"""
        Main Menu class
"""

class mainMenu: # main menu class for the game object
    
    def __init__(self): # start the main menu
        global background
        background = white
        self.startButton = button(size[0]/2, size[1]*3/8, 70, 50, "Start", green) # create a start button that's green, and has the word "start" on it
        self.startButton.setHoverColor(lighterGreen) # make the hover color dark green to indicate you are hovering on it
        self.startButton.setOffset((2, 15))
        self.quitButton = button(size[0]/2, size[1]*5/8, 70, 50, "Quit", red)
        self.quitButton.setHoverColor(lighterRed)
        self.quitButton.setOffset((7, 15))
        self.lineX = size[0]/2
    
    def selfQuit(self):
        pygame.quit()
    
    def draw(self):
        #self.drawLines()
        self.startButton.draw()
        if self.startButton.getPressed(): #     MAKE MENU FOR SELECTING AND PLACE HERE INSTEAD OF CHAGING THE BACKGROUND
            game.setMode("selection")
        self.quitButton.draw()
        if self.quitButton.getPressed():
            pygame.quit()
        
    def drawLines(self): # lines for backgound, just for some visual effect
        self.lineX += .1*30/frameRate
        sinValue = math.sin(self.lineX) 
        xValue = sinValue/2+.5
        r = xValue * 255
        g = ((xValue +.2)%1) * 255
        b = ((xValue + .7)%1) * 255
        xValue = xValue*size[0] / 2
        pygame.draw.line(screen, (r, g, b), (xValue, 0),(xValue, size[1]), 12)
        pygame.draw.line(screen, (r, g, b) ,(size[0]-xValue, 0), (size[0]-xValue, size[1]), 12)
        
    
"""
        Selecting Song Class
"""

class Selection:
    
    def __init__(self, songListFileName):
        self.songPlayer = songSound("test")
        self.songListFileName = songListFileName
        self.getSongNames() # tuple (song name, songfilename.txt)
        self.getSongFiles() # the actual mp3 of the songs
        self.makeSongButtons()
        self.quitButton = button(45, 25, 90, 50, "Back", red)
        self.quitButton.setHoverColor(lighterRed)
        self.quitButton.setOffset((11, 15))
        global background
        background = blue
    
    def getSongNames(self):
        lines = self.getLines()
         # get the song names
        self.songNameList = []
        self.songNameOffset = []
        self.songFileNameList = []
        f = open(self.songListFileName, "r")
        tup = [0, 0, 0]
        for i in range(int(lines/3)):
            tup[0] = f.readline().strip("\n")
            tup[1] = f.readline().strip("\n")
            tup[2] = f.readline()
            self.songNameList.append(tup[0])
            self.songFileNameList.append(tup[1])
            self.songNameOffset.append(int(tup[2]))
        f.close()
    
    def makeSongButtons(self):
        self.songButtons = []
        y = 100
        for i in range(len(self.songNameList)):
            self.songButtons.append(button(size[0]/2, y, 300, 75, self.songNameList[i], lighterBlue))
            self.songButtons[i].setHoverColor(lighterOrange)
            self.songButtons[i].setOffset((self.songNameOffset[i], 22))
            y += 100
            if y == 600:
                break
    
    def getLines(self):
        f = open(self.songListFileName, "r")
        count = 0
        for line in f:
            count += 1
        return count
    
    def getSongFiles(self):
        self.songFileList = ["actual files"] # get sthe actual files from the harddrive
    
    def draw(self):
        self.quitButton.draw()
        if self.quitButton.getPressed():
            game.setMode("main menu")
        for i in range(len(self.songButtons)):
            self.songButtons[i].draw()
            if self.songButtons[i].getPressed():
                print(self.songNameList[i])
                print(self.songListFileName)
                game.setMode("play song", (self.songNameList[i], self.songFileNameList[i]))
    
class songSound:
    def __init__(self, songName):
        self.fileName = songName + ".mp3"



class playSong: # the actual game itself
    
    def __init__(self, song):
        global background
        background = white
        self.quitButton = button(45, 25, 90, 50, "Back", red)
        self.quitButton.setHoverColor(lighterRed)
        self.quitButton.setOffset((11, 15))
        self.name = song[0]
        self.file = song[1]
        self.song = songSound(self.name)
        self.arrowHeight = 30
        self.arrowStem = 30
        self.arrowWidth = 30
        self.arrowThick = 10
        self.arrowList = []
        self.currentTime = 0
        self.setArrows()
    
    
    def drawArrow(self, direction , y):
        # maybe later draw an image instead of a line
        y = self.currentTime - y
        y = y*self.speed
        if direction == "up":
            x = size[0]*2/5
            pygame.draw.polygon(screen, orange, [(x-self.arrowThick, y),(x-self.arrowWidth, y), (x, y-self.arrowHeight),
                                (x+self.arrowWidth, y), (x+self.arrowThick, y), (x+self.arrowThick, y+self.arrowStem),
                                                 (x-self.arrowThick, y+self.arrowStem)])
        elif direction == "right":
            x = size[0]*4/5
            pygame.draw.polygon(screen, orange, [(x, y-self.arrowThick), (x, y - self.arrowWidth), (x+self.arrowHeight, y),
                                (x, y+self.arrowWidth), (x, y+self.arrowThick), (x-self.arrowStem, y+self.arrowThick),
                                                 (x-self.arrowStem, y-self.arrowThick)])
        elif direction == "down":
            x = size[0]*3/5
            pygame.draw.polygon(screen, orange, [(x+self.arrowThick, y),(x+self.arrowWidth, y), (x,y+self.arrowHeight),
                                (x-self.arrowWidth, y), (x-self.arrowThick, y), (x-self.arrowThick, y-self.arrowStem),
                                                 (x+self.arrowThick, y-self.arrowStem)])
        elif direction == "left":
            x = size[0]/5
            pygame.draw.polygon(screen, orange, [(x, y+self.arrowThick),(x, y+self.arrowWidth), (x-self.arrowHeight, y),
                                (x, y-self.arrowWidth), (x, y-self.arrowThick), (x+self.arrowStem, y-self.arrowThick),
                                                 (x+self.arrowStem, y+self.arrowThick)])



    
    def draw(self):
        if self.quitButton.getPressed():
            game.setMode("selection")
        for i in self.arrowList:
            self.drawArrow(i[0], i[1])
        stopY = self.currentTime - self.arrowList[-1][1]
        stopY = stopY*self.speed
        if stopY >  600:
            game.setMode("selection") # eventually go into the score screen (not in plans right now)
        self.quitButton.draw()
        pygame.draw.line(screen,black, (0, 600), (size[0], 600)) # temparary until the overlay class is ready for functioning
        #if song should continue:
        self.currentTime += 1
    
    def setArrows(self):
        f = open(self.file, "r")
        self.speed = int(f.readline())/(upSpeed*30/frameRate)
        count = 1
        for line in f:
            count += 1
        f.close()
        f = open(self.file, "r")
        f.readline()
        for i in range(count):
            string = f.readline()
            if not string.find("l") == -1:
                self.arrowList.append(("left", int(i*self.speed)))
            if not string.find("u") == -1:
                self.arrowList.append(("up", int(i*self.speed)))
            if not string.find("r") == -1:
                self.arrowList.append(("right", int(i*self.speed)))
            if not string.find("d") == -1:
                self.arrowList.append(("down", int(i*self.speed)))
            if not string.find("s") == -1:
                self.arrowList.append(("stop", int(i*self.speed)))
        f.close()
    

        
        
        
    
    
    
class button:
    
    def __init__(self, x, y, width, height, name="", color=(51, 51, 51)):
        # the button will be centered at x, y
        self.x = x - width/2
        self.y = y - height/2
        self.width = width # the width of the button
        self.height = height  # the height of the button
        self.text = name  # the text that goes on the button as it is drawn
        self.color = color # the color the button is naturally
        self.hoverColor = color # the color the button is when hovered over by the mouse
        self.xOffset = 0
        self.yOffset = 0
        self.visible = True
        
    def setOffset(self, offset):
        self.xOffset = offset[0]
        self.yOffset = offset[1]
        
    def setHoverColor(self, color):  # set the color the button is when the mouse hovers over it
        self.hoverColor = color
    
    def moveRel(self, xOff, yOff):
        self.x += xOff
        self.y += yOff
    
    def setLocation(self, newX, newY):
        self.x = newX
        self.y = newY
    
    def setVisible(self, vis):
        self.visible = vis
    
    def draw(self):  #draw the button, if the mouse is hovering, then do the secondary color
        if not self.visible:
            return
        tempColor = self.color
        if self.mouseOver():
            tempColor = self.hoverColor
        pygame.draw.polygon(screen, tempColor, [(self.x, self.y), (self.x+self.width, self.y), (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)])
        textFont.render_to(screen, (self.x + self.xOffset,self.y+self.yOffset), self.text, black)
        
    def mouseOver(self): # checks to see if the mouse is on the button
        mouse = pygame.mouse.get_pos()
        if mouse[0] > self.x and mouse[0] < self.x + self.width:
            if mouse[1] > self.y and mouse[1] < self.y + self.height:
                return True
        return False
        
    def getPressed(self):  # gets if the button was pressed...
                        # if multiple buttons on the same location, all will get pressed
        global mouseClicked
        if not mouseClicked:
            return False
        mouse = pygame.mouse.get_pos()
        return self.mouseOver()


"""
        colors
"""
white = (255, 255, 255)
black = (0, 0, 0)
grey = (51, 51, 51)
orange = (255, 140, 0)
lighterOrange = (200, 100, 0)
darkOrnage = (128, 70, 0)
red = (255, 0, 0)
lighterRed = (200, 0, 0)
darkRed = (128, 0, 0)
green = (0, 255, 0)
lighterGreen = (0, 200, 0)
darkGreen = (0, 128, 0)
blue = (0, 0, 255)
lighterBlue = (0, 0, 200)
darkBlue = (0, 0, 128)



"""
        pygame setup
"""
global wasClicked
wasClicked = False # used to see if the mouse was just pressed or not

global mouseClicked
mouseClicked = False # true if the mouse is pressed this frame

size = (700, 700) # the size of the window
screen = pygame.display.set_mode(size) # seting the screen

global background
background = white # set the initial background to white

upSpeed = 25 # distance between
frameRate = 60 # speed of the song (times four for quarter notes)
pygame.display.set_caption("Dance Dance") # caption or title of the game on the top of the window
clock = pygame.time.Clock() # sets up the clock for the game to run at a specific FPS
pygame.freetype.init()  # set up the font library
textFont = pygame.freetype.SysFont("Comic Sans Ms", 30) # set the screen to write text to
pygame.joystick.init() # setup the joystick library
js = pygame.joystick.Joystick(0)  # create a joystick for possible use later
js.init() # set up the joystick
game = Game()  # create the actual game (multiple games are possible to run at the same time)




"""
        draw function
"""
def draw():
    screen.fill(background) # fill screen with white
    checkClick() # checks if the mouse was clicked this frame
    game.draw() # draw to memory
    render() # render what's in memory


"""
        render what's in the memory 
"""
def render():
    pygame.display.flip() # render the memory
    clock.tick(frameRate) # keep the game running at 60 FPS



def checkClick(): # check if the mouse was clicked
    pygame.event.get()
    global wasClicked
    global mouseClicked
    
    if pygame.mouse.get_pressed()[0]: # if the button is down
        if wasClicked: # and if it was down last frame
            mouseClicked = False # make it false
        else: # else, it wasn't down last frame
            wasClicked = True # so both are true
            mouseClicked = True
    else: # if it's not down, it wasn't clicked
        wasClicked = False
        mouseClicked = False


while True:  # main game loop, just draw game
    # the game updates while in the draw loop
    # there should be an update function before the draw
    # but i am too lazy to do that, and this is woring
    # so i will not do anything to make it more feasable until
    # something is going horribly wrong
    draw()
        