from machine import Pin
from time import sleep

pinA = Pin(1, Pin.IN, Pin.PULL_UP)
pinB = Pin(0, Pin.IN, Pin.PULL_UP)

radius = 7.5  # mm
pulsesPerRevolution = 1200  # pulses per revolution

position = 0
distance = 0


def A_hendler(pin):
    global position
    if pinA.value():  # RISING
        if pinB.value():
            position -= 1
        else:
            position += 1
    else:  # FALLING
        if pinB.value():
            position += 1
        else:
            position -= 1
    calc_distance()


def B_hendler(pin):
    global position
    if pinB.value():  # RISING
        if pinA.value():
            position += 1
        else:
            position -= 1
    else:  # FALLING
        if pinA.value():
            position -= 1
        else:
            position += 1
    calc_distance()


def calc_distance():
    global distance
    distance = position * 2 * 3.14 * radius / pulsesPerRevolution


def getDistance():
    return distance


def resetEncoder():
    global position
    position = 0
    calc_distance()


pinA.irq(trigger=Pin.IRQ_FALLING, handler=A_hendler)
pinB.irq(trigger=Pin.IRQ_FALLING, handler=B_hendler)