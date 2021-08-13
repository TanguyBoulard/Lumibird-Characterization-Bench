# =============================================================================
# CREDITS
# =============================================================================
# Author : Tanguy BOULARD
# Date   : 28/06/2021
# Script : Burn-in

# =============================================================================
# MODULES
# =============================================================================

import PRO8000

import pyvisa
import sys
import time

# =============================================================================
# FUNCTIONS
# =============================================================================

def Timer(hours, mins, secs):
    t = hours*3600 + mins*60 + secs
    while t:
        hours, remainder = divmod(t, 3600)
        mins, secs = divmod(remainder, 60)
        timer = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
        print(timer, end='\n\r')
        time.sleep(1)
        t -= 1
    print('FIN')
    return 1

def main(I, T, hours, mins, secs):

    pro8000 = PRO8000.Initialize(T, I)
    Timer(int(hours), int(mins), int(secs))
    PRO8000.Close(pro8000)
    return 1
    

def Stop():
    rm = pyvisa.ResourceManager()
    pro8000 = rm.open_resource("ASRL8::INSTR")
    PRO8000.Close(pro8000)
    sys.exit()
    return 1