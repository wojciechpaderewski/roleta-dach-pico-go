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

state = 'ready'

endstop = Pin(2, Pin.IN, Pin.PULL_UP)
up_button = Pin(4, Pin.IN, Pin.PULL_DOWN)
down_button = Pin(5, Pin.IN, Pin.PULL_DOWN)
mode_button = Pin(6, Pin.IN, Pin.PULL_DOWN)

goal = 0

def setState(newState):
    global state
    state = newState

def moveToGoal(newGoal):
    global state
    global goal
    goal = newGoal
    state = 'moveToPosition'

def update():
    handelMoveForward()
    handelMoveBackward()
    handelStop()
    hendelMoveToPosition()
    updateEndstop()
    updateEncoder()
    handelSingelClicks()
    handelDoubleClicks()

def handelMoveBackward():
    global state
    
    if state != 'moveBackward':
        return
    
    if not endstop.value(): 
        stop()
        state = 'ready'
        return
    
    if isAnyButtonPressed():	
        state = 'ready'
        return
    
    move_backward()
    
def getEndstop():
    return endstop.value()
    
def handelMoveForward():
    global state
    
    if state != 'moveForward':
        return
    
    if getDistance() >= maxEncoderValue: 
        stop()
        state = 'ready'
        return
    
    if isAnyButtonPressed():
        state = 'ready'
        return
    
    move_forward()


def handelStop():
    if isAnyButtonPressed() or state == 'moveToPosition':
        return
    
    if state == 'moveBackward' or state == 'moveForward':
        return
    
    stop()


def hendelMoveToPosition():
    global state
    global goal
    
    if goal > maxEncoderValue:
        goal = maxEncoderValue
    elif goal < 0:
        goal = 0

    if getDistance() > goal and state == 'moveToPosition':
        if isAnyButtonPressed():
            state = 'ready'
            return
        state = 'moveBackward'
        
    if getDistance() <= goal and state == 'moveBackward' and goal != 0:
        state = 'ready'
        return
        
    if getDistance() < goal and state == 'moveToPosition':
        if isAnyButtonPressed():
            state = 'ready'
            return
        state = 'moveForward'
        
    if getDistance() >= goal and state == 'moveForward':
        state = 'ready'
        return

def getState():
    return state

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
    global state
    if up_button.value() and not isUp:
        move_forward()
    elif down_button.value() and not isDown:
        move_backward()
    elif mode_button.value():
        stop()
        state = 'ready'
        resetEncoder()


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
        moveToGoal(maxEncoderValue)

    if doubleClickDetected and currentButton == 'down':
        moveToGoal(0)
    
    watchDoubleClickTimers()
    doubleClickStateMachine()
