import time
import sys
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import supervisor

# Stepper motor 1 : bolometer
# Stepper motor 2 : sphere

kit = MotorKit(i2c=board.I2C())
angle_sphere = 100
angle_bolometer = 100

def BolometerIn(angle_bolometer):
    for i in range(angle_bolometer):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        time.sleep(0.01)
        
def BolometerOut(angle_bolometer):
    for i in range(angle_bolometer):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
        time.sleep(0.01)

def SphereIn(angle_sphere):
    for i in range(angle_sphere):
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        time.sleep(0.01)
        
def SphereOut(angle_sphere):
    for i in range(angle_sphere):
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
        time.sleep(0.01)

def EXECUTE(value, angle_sphere, angle_bolometer):
    if value == 'a':
            BolometerIn(angle_bolometer)

    elif value == 'b':
            BolometerOut(angle_bolometer)
            
    elif value == 'y':
            SphereIn(angle_sphere)

    elif value == 'z':
            SphereOut(angle_sphere)

while True:
    if supervisor.runtime.serial_bytes_available:
        value = sys.stdin.read(1)
        EXECUTE(value, angle_sphere, angle_bolometer)
