# =============================================================================
# CREDITS
# =============================================================================
# Author : Tanguy BOULARD
# Date   : 28/06/2021
# Script : Arduino

# =============================================================================
# MODULES
# =============================================================================

import serial
import time

# =============================================================================
# FUNCTIONS
# =============================================================================

def OpenPort():
    port = serial.Serial('COM16', 115200)
    if not port.isOpen():
        port.open()
    port.flush()
    return port

def Write(port, command):
    port.write(command)
    for _ in range(len(command)):
        port.read() # Read the loopback chars and ignore
    return 1

def Read(port):
    while True:
        reply = b''
        a = port.read()
        if a == b'\r':
            break
        else:
            reply += a
            time.sleep(0.01)
    return reply
