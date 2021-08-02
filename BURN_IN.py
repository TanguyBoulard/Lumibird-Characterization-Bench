SLOT_T = 1
SLOT_LD = 3
PRO8000_offset = 5.0 #mA

import pyvisa
import sys
import time

def PRO8000WaitUntilSet_T(instrument, T):
    for i in range (50000):
        if (T-T*(5/100) <= (float(instrument.query(':TEMP:ACT?')[10:])) <= T+T*(5/100)):
            break
        time.sleep(1)

def PRO8000WaitUntilSet_I(instrument, I):
    for i in range (50000):
        if (I-I*(5/100) <= ((float(instrument.query(':ILD:ACT?')[9:]))*1E3) <= I+I*(5/100)):
            break
        time.sleep(1)

def PRO8000Error(instrument):
    err = instrument.query(':SYST:ERR?')
    if int(err[0]) == '0':
        print(err, end="\n\r")

def Timer(t, my_instrument):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\n\r")
        time.sleep(1)
        t -= 1
    print('FIN')
    return 1

def Connection():
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())

    pro8000 = rm.open_resource('ASRL8::INSTR')
    pro8000.read_termination = '\r\n'
    pro8000.write_termination = '\r\n'
    pro8000.baud_rate = 19200
    pro8000.query_delay = 0.1
    if pro8000.query('*IDN?') != 'PROFILE, PRO8000, 0, Ver.4.28-1.22':
        print('pro8000 not connected')
        sys.exit()
    pro8000.clear()
    pro8000.write('*RST')
    pro8000.write('*CLS')

    return pro8000

def Initialize(I, T, t):

    pro8000 = Connection()
    
    pro8000.write(':SLOT %i' %SLOT_T)
    pro8000.write(':TEMP:SET %f' %T)
    pro8000.write(':TEC ON')
    PRO8000WaitUntilSet_T(pro8000, T)
    PRO8000Error(pro8000)

    pro8000.write(':SLOT %i' %SLOT_LD)
    value = I + PRO8000_offset #aucune idée de pourquoi un offset de 5
    pro8000.write(':ILD:SET %fE-3' %value)
    pro8000.write(':LASER ON')
    PRO8000WaitUntilSet_I(pro8000, I)
    PRO8000Error(pro8000)

    Timer(int(t), pro8000)
    
    return pro8000

def End(I, T, t):
    
    pro8000 = Initialize(I, T, t)
    
    pro8000.write(':SLOT %i' %SLOT_T)
    pro8000.write(':TEC OFF')
    PRO8000Error(pro8000)

    pro8000.write(':SLOT %i' %SLOT_LD)
    pro8000.write(':LASER OFF')
    PRO8000Error(pro8000)

    pro8000.write('*RST')
    pro8000.close(pro8000)
    
def Stop():
    rm = pyvisa.ResourceManager()

    pro8000 = rm.open_resource('ASRL8::INSTR')
    pro8000.write(':SLOT %i' %SLOT_T)
    pro8000.write(':TEC OFF')
    PRO8000Error(pro8000)

    pro8000.write(':SLOT %i' %SLOT_LD)
    pro8000.write(':LASER OFF')
    PRO8000Error(pro8000)

    pro8000.write('*RST')
    pro8000.close(pro8000)
    sys.exit()