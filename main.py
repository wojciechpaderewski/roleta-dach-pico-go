import HAcomunication
import control

try:
    HAcomunication.init()
except OSError as e:
    HAcomunication.reconnect()
while True:
    HAcomunication.update()
    control.update()