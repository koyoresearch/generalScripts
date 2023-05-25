#A simple python fuzzer that sends mouse clicks to random locations in a specified application window, and sends random alpha-numeric characters to gui elements of the specified application. It switches between the application's gui elements by sending a tab keystroke before entering the random character.
#Note: for linux, need to use xorg window manager, not wayland, or the mouse cursor won't move
#TODO: command to get the window id in Windows
import os
import sys
import time
import random
import string
import subprocess
import pyautogui
import win32gui
#import x11

if len(sys.argv) < 2:
	print("Please provide the name or id of the application that you want to fuzz: fuzzer.py <name/id>")
	print("If you are running this script on Windows, just provide the name that is in the target application's title bar.")
	print("If you are running this script on Linux, you can get the window id by running the xwininfo command, and then click on the target app's window when prompted.")
	sys.exit()
	
targetApp = sys.argv[1]

def getLinuxAppWindowDimentions():
	result = subprocess.run(['xwininfo', '-id', targetApp], stdout=subprocess.PIPE)
	buf = str(result.stdout)
	#print("buf: ", buf)
    
	#extract x
	xStartLoc = buf.index("Absolute upper-left X: ")
	buf = buf[xStartLoc + 24:]
	xEndLoc = buf.index("\\n ")
	x = buf[0:xEndLoc]
	#print(x)
	buf = buf[xEndLoc:]
	#extract y
	yStartLoc = buf.index("Absolute upper-left Y: ")
	buf = buf[yStartLoc + 24:]
	yEndLoc = buf.index("\\n")
	y = buf[0:yEndLoc]
	#print(y)
	buf = buf[yEndLoc:]
	#extract width
	widthStartLoc = buf.index("Width: ")
	buf = buf[widthStartLoc + 7:]
	widthEndLoc = buf.index("\\n")
	width = buf[0:widthEndLoc]
	#print(width)
	buf = buf[widthEndLoc:]
	#extract height
	heightStartLoc = buf.index("Height: ")
	buf = buf[heightStartLoc + 8:]
	heightEndLoc = buf.index("\\n")
	height = buf[0:heightEndLoc]
	#print(height)
    
	returnList = [x, y, width, height]
	return returnList

def getWindowsAppWindowDimensions():
	hwnd = win32gui.FindWindow(None, targetApp)
	rect = win32gui.GetWindowRect(hwnd)
	x = rect[0]
	y = rect[1]
	width = rect[2] - x
	height = rect[3] - y
	
	returnList = [x, y, width, height]
	return returnList

#function to gitter mouse a little bit each way
#but this ends up sending the cursor down and to the right;
#the randomizer's weight is apparently on the positive side
def getRandPos():
	randPos = random.randint(-100, 100)
	return randPos

def getRandXPos(x, width):
	randPos = random.randint(int(x), int(x) + int(width))
	return randPos
	
def getRandYPos(y, height):
	randPos = random.randint(int(y), int(y) + int(height))
	return randPos
	
def getRandChar():
	randChar = random.choice(string.ascii_letters + string.digits)
	return randChar
	


#get application's window coordinates
if os.name == "posix":
	windowCoords = getLinuxAppWindowDimentions()
else:
	windowCoords = getWindowsAppWindowDimensions()

x = windowCoords[0]
y = windowCoords[1]
width = windowCoords[2]
height = windowCoords[3]

#fuzzing loop, doing a mouse click and a character entry each loop
while 1:
	time.sleep(1.5) #sleep each round, so have time to kill the script
	
	#do mouse click at random position
	#print("moving mouse")
	#print(pyautogui.position())
	
	#<moving the mouse relative to the previous position ends up sending the cursor down 
	#and to the right; the randomizer's weight is apparently on the positive side
	#x = getRandPos()
	#y = getRandPos()
	#while pyautogui.onScreen(x, y) != True:
	#    print("getting another coordinate")
	#    x = getRandPos()
	#    y = getRandPos()
	#pyautogui.moveRel(x, y, duration=0.2)
	#>
	
	#move to a random position each time
	pyautogui.moveTo(getRandXPos(x, width), getRandYPos(y, height), duration=0.2)
	pyautogui.click(button='left')
	
	#tab to the next gui element, and send a random alpha-numeric character
	#print("tabbing and inserting chars")
	pyautogui.press('tab')
	pyautogui.typewrite(getRandChar(), interval=.1)
	pyautogui.press('enter')