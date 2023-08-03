import HAcomunication
import control

try:
    HAcomunication.init()
except Exception as e:
    control.stop()
    HAcomunication.reconnect()
while True:
    HAcomunication.update()
    control.update()