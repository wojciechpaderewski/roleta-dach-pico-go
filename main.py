import HAcomunication
import control
import time

try:
    HAcomunication.init()
except OSError as e:
    HAcomunication.reconnect()
while True:
    HAcomunication.update()
    control.update()