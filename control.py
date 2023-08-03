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
isEncoderCiriticalError = False

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
    global isHommed
    global isEncoderCiriticalError
    
    if isEncoderCiriticalError:
        if mode_button.value() == 1:
            isEncoderCiriticalError = False
            isHommed = True
        stop()
        return
    encoderNotMovingProtection()
    if not isHommed:
        autoHome()
        return
    handelMoveBackward()
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
    
    if isAnyButtonPressed():
        isHommed = True
    
    if not endstop.value():
        stop()
        state = 'ready'
        isHommed = True
        resetEncoder()
        return

    move_backward()    

def encoderNotMovingProtection():
    global state
    global lastEncoderValue
    global lastEncoderValueTime
    global isEncoderCiriticalError
    
    if state == 'moveBackward' or not isHommed:
        if lastEncoderValue - 0.20 < getDistance() and getDistance() != 0 and lastEncoderValue != 0:
            if lastEncoderValueTime + 500 < milis():
                print(lastEncoderValue, getDistance(), 'backward')
                isEncoderCiriticalError = True
                return
        else:
            lastEncoderValue = getDistance()
            lastEncoderValueTime = milis()
    elif state == 'moveForward':
        if lastEncoderValue + 0.20 > getDistance() and getDistance() != 0 and lastEncoderValue != 0:
            if lastEncoderValueTime + 500 < milis():
                print(lastEncoderValue, getDistance(), 'forward')
                isEncoderCiriticalError = True
                return
        else:
            lastEncoderValue = getDistance()
            lastEncoderValueTime = milis()
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

    if getDistance() <= maxEncoderValue and up_button.value():
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
