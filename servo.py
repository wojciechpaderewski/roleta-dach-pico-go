from machine import Pin, PWM
from time import sleep

STOP = 1500000
FORWARD = 1000000
BACKWARD = 2000000

servo_pwm = PWM(Pin(7))
servo_pwm.freq(50)

def move_forward():
    servo_pwm.duty_ns(FORWARD)
    sleep(0.01)
        
def move_backward():
    servo_pwm.duty_ns(BACKWARD)
    sleep(0.01)
    
def stop():
    servo_pwm.duty_ns(STOP)
    sleep(0.01)