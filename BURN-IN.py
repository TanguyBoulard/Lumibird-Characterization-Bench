# =============================================================================
# BURN-IN CONDITIONS
# =============================================================================

T = 100.0 #°C
SLOT_T = 1
I = 100.0 #A
SLOT_LD = 3
PRO8000_offset = 5.0 #mA
t = 24*60*60 #hour*min*sec

# =============================================================================
# LIBRAIRIES
# =============================================================================

import pyvisa
import sys
import time

# =============================================================================
# FUNCTION
# =============================================================================

def PRO8000WaitUntilSet_T(T):
    for i in range (50000):
        if (T-T*(5/100) <= (float(pro8000.query(':TEMP:ACT?')[10:])) <= T+T*(5/100)):
            break
        time.sleep(1)

def PRO8000WaitUntilSet_I(I):
    for i in range (50000):
        if (I-I*(5/100) <= ((float(pro8000.query(':ILD:ACT?')[9:]))*1E3) <= I+I*(5/100)):
            break
        time.sleep(1)

def PRO8000Error():
    err = pro8000.query(':SYST:ERR?')
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

# =============================================================================
# SET UP
# =============================================================================

rm = pyvisa.ResourceManager()
# print(rm.list_resources())

pro8000 = rm.open_resource('ASRL8::INSTR')
pro8000.read_termination = '\r\n'
pro8000.write_termination = '\r\n'
pro8000.baud_rate = 19200
query_delay = 0.1
if pro8000.query('*IDN?') != 'PROFILE, PRO8000, 0, Ver.4.28-1.22':
    print('pro8000 not connected')
    sys.exit()
# pro8000.clear()
# pro8000.write('*RST')
# pro8000.write('*CLS')

# =============================================================================
# INITIALIZATION
# =============================================================================

pro8000.write(':SLOT %i' %SLOT_T)
pro8000.write(':TEMP:SET %f' %T)
pro8000.write(':TEC ON')
PRO8000WaitUntilSet_T(T)
PRO8000Error()

pro8000.write(':SLOT %i' %SLOT_LD)
value = I + PRO8000_offset #aucune idée de pourquoi un offset de 5
pro8000.write(':ILD:SET %fE-3' %value)
pro8000.write(':LASER ON')
PRO8000WaitUntilSet_I(I)
PRO8000Error()

Timer(int(t), pro8000)

# =============================================================================
# END
# =============================================================================

pro8000.write(':SLOT %i' %SLOT_T)
pro8000.write(':TEMP:SET 25.0')
# pro8000.write(':TEC OFF')
PRO8000Error()

pro8000.write(':SLOT %i' %SLOT_LD)
pro8000.write(':LASER OFF')
PRO8000Error()

pro8000.write('*RST')
pro8000.close()
