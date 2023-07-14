from machine import Pin
from servo import move_forward, move_backward, stop
from encoder import getDistance, resetEncoder
from time import time

builtin_led = Pin("LED", Pin.OUT)
maxEncoderValue = 570

firstClickTime = 0
secondClickTime = 0

doubleClickTime = 550

doubleClickDetected = False
detectedButton = 'none'

endstop = Pin(2, Pin.IN, Pin.PULL_UP)
isDown = False
isUp = False

up_button = Pin(4, Pin.IN, Pin.PULL_DOWN)
down_button = Pin(5, Pin.IN, Pin.PULL_DOWN)
mode_button = Pin(6, Pin.IN, Pin.PULL_DOWN)

detectDoubleClickState = 0

def milis():
    return time() * 1000

while True:
    print('working')
    if not endstop.value():
        isDown = True
        resetEncoder()
    elif endstop.value():
        isDown = False
    if getDistance() < maxEncoderValue:
        isUp = False
    elif getDistance() > maxEncoderValue:
        isUp = True

    if up_button.value() and not isUp:
        move_forward()
    elif down_button.value() and not isDown:
        move_backward()
    elif mode_button.value():
        resetEncoder()
    else:
        stop()

    if doubleClickDetected and detectedButton == 'up':
        while getDistance() < maxEncoderValue:
            if down_button.value() or not endstop.value():
                stop()
                break
            move_forward()

    if doubleClickDetected and detectedButton == 'down':
        while endstop.value():
            if up_button.value() or getDistance() > maxEncoderValue:
                stop()
                break
            move_backward()

    if(milis() - firstClickTime > doubleClickTime):
        detectDoubleClickState = 0
        doubleClickDetected = False

    if detectDoubleClickState == 0:
        if up_button.value():
            firstClickTime = milis()
            detectDoubleClickState = 1
            detectedButton = 'up'
        elif down_button.value():
            firstClickTime = milis()
            detectDoubleClickState = 1
            detectedButton = 'down'
    elif detectDoubleClickState == 1:
        if detectedButton == 'up' and not up_button.value():
            detectDoubleClickState = 2
        elif detectedButton == 'down' and not down_button.value():
            detectDoubleClickState = 2
    elif detectDoubleClickState == 2:
        if detectedButton == 'up' and up_button.value():
            secondClickTime = milis()
            detectDoubleClickState = 3
        elif detectedButton == 'down' and down_button.value():
            secondClickTime = milis()
            detectDoubleClickState = 3
    elif detectDoubleClickState == 3:
        if detectedButton == 'up' and not up_button.value():
            detectDoubleClickState = 0
            if milis() - firstClickTime < doubleClickTime:
                doubleClickDetected = True
            else:
                doubleClickDetected = False
        elif detectedButton == 'down' and not down_button.value():
            detectDoubleClickState = 0
            if milis() - firstClickTime < doubleClickTime:
                doubleClickDetected = True
            else:
                doubleClickDetected = False