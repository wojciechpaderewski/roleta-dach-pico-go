from machine import Pin
import machine
from servo import move_forward, move_backward, stop
from encoder import getDistance, resetEncoder
from time import time

maxEncoderValue = 570

state = 'ready'

endstop = Pin(2, Pin.IN, Pin.PULL_UP)
up_button = Pin(4, Pin.IN, Pin.PULL_DOWN)
down_button = Pin(5, Pin.IN, Pin.PULL_DOWN)
mode_button = Pin(6, Pin.IN, Pin.PULL_DOWN)

lastEncoderValue = 0
lastEncoderValueTime = 0

isHommed = False

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
    encoderNotMovingProtection()
    handelMoveBackward()
    if not isHommed:
        autoHome()
        return
    handelMoveForward()
    handelStop()
    hendelMoveToPosition()
    handelSingelClicks()

def handelMoveBackward():
    global state
    
    if state != 'moveBackward':
        return
    
    if not endstop.value() or getDistance() <= 0: 
        stop()
        state = 'ready'
        return
    
    if isAnyButtonPressed():	
        state = 'ready'
        return
    
    move_backward()
    
def getEndstopValue():
    return endstop.value()

def autoHome():
    global state
    global isHommed
    
    if not endstop.value():
        stop()
        state = 'ready'
        isHommed = True
        resetEncoder()
        return
    
    state = 'moveBackward'

def encoderNotMovingProtection():
    global state
    global lastEncoderValue
    global lastEncoderValueTime
    
    if state == 'moveBackward' or state == 'moveForward':
        if lastEncoderValue == getDistance():
            if lastEncoderValueTime + 1000 < milis():
                stop()
                state = 'ready'
                return
        else:
            lastEncoderValue = getDistance()
            lastEncoderValueTime = milis()
    
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
        
    if getDistance() <= goal and state == 'moveBackward':
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

def milis():
    return time() * 1000

def handelSingelClicks():
    global state

    if up_button.value() and getDistance() <= maxEncoderValue:
        move_forward()
    elif down_button.value():
        if endstop.value() == 0:
            onEndstopReached()
            return
        move_backward()
    elif mode_button.value():
        stop()
        state = 'ready'
        resetEncoder()

def onEndstopReached():
    global state
    stop()
    resetEncoder()
    state = 'ready'

def isAnyButtonPressed():
    if up_button.value() or down_button.value() or mode_button.value():
        return True
    else:
        return False
