import PRO8000

import pyvisa
import sys
import time

def Timer(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(timer, end='\n\r')
        time.sleep(1)
        t -= 1
    print('FIN')
    return 1

def Action(I, T, t):
    
    instrument = PRO8000.Initialize()

    PRO8000.SlotT()
    PRO8000.Write(instrument, ':TEMP:SET %f' %T)
    PRO8000.Write(instrument, ':TEC ON')
    PRO8000.WaitUntilSet_T(instrument, T)

    PRO8000.SlotLD()
    value = PRO8000.Offset(I)
    PRO8000.Write(instrument, ':ILD:SET %fE-3' %value)
    PRO8000.Write(instrument, ':LASER ON')
    PRO8000.WaitUntilSet_I(instrument, I)

    Timer(int(t))

    PRO8000.SlotT()
    PRO8000.Write(instrument, ':TEC OFF')

    PRO8000.SlotLD()
    PRO8000.Write(instrument, ':LASER OFF')

    PRO8000.Write(instrument, '*RST')
    instrument.close()


def Stop():
    rm = pyvisa.ResourceManager()
    instrument = rm.open_resource("ASRL8::INSTR")
    
    PRO8000.SlotT()
    PRO8000.Write(instrument, ':TEC OFF')

    PRO8000.SlotLD()
    PRO8000.Write(instrument, ':LASER OFF')

    PRO8000.Write(instrument, '*RST')
    instrument.close()
    sys.exit()