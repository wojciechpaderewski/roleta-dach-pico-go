import HAcomunication
import control

HAcomunication.init()

while True:
    control.updateManualControl()
    HAcomunication.update()