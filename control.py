from machine import Pin
from servo import move_forward, move_backward, stop
from encoder import getDistance, resetEncoder
from time import time

maxEncoderValue = 570

firstClickTime = 0
secondClickTime = 0

doubleClickTime = 550

doubleClickDetected = False
currentButton = 'none'
detectDoubleClickState = 0

isDown = False
isUp = False

endstop = Pin(2, Pin.IN, Pin.PULL_UP)
up_button = Pin(4, Pin.IN, Pin.PULL_DOWN)
down_button = Pin(5, Pin.IN, Pin.PULL_DOWN)
mode_button = Pin(6, Pin.IN, Pin.PULL_DOWN)


def updateManualControl():
    updateEndstop()
    updateEncoder()
    handelSingelClicks()
    handelDoubleClicks()

def milis():
    return time() * 1000

def updateEndstop():
    global isDown
    if not endstop.value():
        isDown = True
        resetEncoder()
    elif endstop.value():
        isDown = False

def updateEncoder():
    global isUp
    if getDistance() < maxEncoderValue:
        isUp = False
    elif getDistance() > maxEncoderValue:
        isUp = True

def handelSingelClicks():
    if up_button.value() and not isUp:
        move_forward()
    elif down_button.value() and not isDown:
        move_backward()
    elif mode_button.value():
        resetEncoder()
    else:
        stop()

def openCover():
    while getDistance() < maxEncoderValue:
        if isAnyButtonPressed() or not endstop.value():
            stop()
            break
        move_forward()

def closeCover():
    while endstop.value():
            if isAnyButtonPressed() or getDistance() > maxEncoderValue:
                stop()
                break
            move_backward()

def moveToPosition(position):
    if position > maxEncoderValue:
        position = maxEncoderValue
    elif position < 0:
        position = 0

    while getDistance() < position:
        if isAnyButtonPressed() or not endstop.value():
            stop()
            break
        move_forward()

    while endstop.value():
        if isAnyButtonPressed() or getDistance() > position:
            stop()
            break
        move_backward()

def isAnyButtonPressed():
    if up_button.value() or down_button.value() or mode_button.value():
        return True
    else:
        return False


def watchDoubleClickTimers():
    global doubleClickDetected
    global detectDoubleClickState

    if(milis() - firstClickTime > doubleClickTime):
        detectDoubleClickState = 0
        doubleClickDetected = False

def doubleClickStateMachine():
        global detectDoubleClickState
        global doubleClickDetected
        global currentButton
        global firstClickTime
        global secondClickTime

        if detectDoubleClickState == 0:
            if up_button.value():
                firstClickTime = milis()
                detectDoubleClickState = 1
                currentButton = 'up'
            elif down_button.value():
                firstClickTime = milis()
                detectDoubleClickState = 1
                currentButton = 'down'
        elif detectDoubleClickState == 1:
            if currentButton == 'up' and not up_button.value():
                detectDoubleClickState = 2
            elif currentButton == 'down' and not down_button.value():
                detectDoubleClickState = 2
        elif detectDoubleClickState == 2:
            if currentButton == 'up' and up_button.value():
                secondClickTime = milis()
                detectDoubleClickState = 3
            elif currentButton == 'down' and down_button.value():
                secondClickTime = milis()
                detectDoubleClickState = 3
        elif detectDoubleClickState == 3:
            if currentButton == 'up' and not up_button.value():
                detectDoubleClickState = 0
                if milis() - firstClickTime < doubleClickTime:
                    doubleClickDetected = True
                else:
                    doubleClickDetected = False
            elif currentButton == 'down' and not down_button.value():
                detectDoubleClickState = 0
                if milis() - firstClickTime < doubleClickTime:
                    doubleClickDetected = True
                else:
                    doubleClickDetected = False
    

def handelDoubleClicks(): 
    if doubleClickDetected and currentButton == 'up':
        openCover()

    if doubleClickDetected and currentButton == 'down':
        closeCover()
    
    watchDoubleClickTimers()
    doubleClickStateMachine()
