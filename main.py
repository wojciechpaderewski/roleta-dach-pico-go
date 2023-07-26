import HAcomunication
import control
import time

print('Starting main.py')

try:
    HAcomunication.init()
except OSError as e:
    HAcomunication.reconnect()
while True:
    HAcomunication.update()
    control.update()