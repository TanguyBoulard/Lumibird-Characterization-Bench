import time
import sys
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import supervisor

kit = MotorKit(i2c=board.I2C())

def FORWARD():
    for i in range(100):
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        time.sleep(0.01)

def BACKWARD():
    for i in range(100):
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
        time.sleep(0.01)

def EXECUTE(value):
    if value == 'f':
            FORWARD()

    elif value == 'b':
            BACKWARD()

while True:
    if supervisor.runtime.serial_bytes_available:
        value = sys.stdin.read(1)
        EXECUTE(value)
