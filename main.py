import HAcomunication
import control
import time


print('Starting main.py')
initziled = HAcomunication.init()

while True:
    if initziled:
        HAcomunication.update()
        control.updateManualControl()