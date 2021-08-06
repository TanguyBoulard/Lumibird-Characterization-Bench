import pyvisa
import sys
import time

SLOT_T = 1
slot_T = ':SLOT %i' % SLOT_T
SLOT_LD = 3
slot_LD = ':SLOT %i' % SLOT_LD
PRO8000_offset = 5.0  # mA

def Offset(I):
    if I != 0 and I != 10:
        value = I + PRO8000_offset  # i do not know why a 5mV offset for i>0mA
    elif I == 10:
        value = I + 5
    else:
        value = I
    return value

def SlotLD(instrument):
    Write(instrument, slot_LD)

def SlotT(instrument):
    Write(instrument, slot_T)

def Initialize():
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())

    instrument = rm.open_resource('ASRL8::INSTR')
    instrument.read_termination = '\r\n'
    instrument.write_termination = '\r\n'
    instrument.baud_rate = 19200
    instrument.query_delay = 0.1
    if Query(instrument, '*IDN?') != 'PROFILE, PRO8000, 0, Ver.4.28-1.22':
        print('Le PRO8000 n\'est pas connecté')
        sys.exit()
    instrument.clear()
    Write(instrument, '*RST')
    Write(instrument, '*CLS')
    
    return instrument

def Write(instrument, command):
    instrument.write(command)
    Error(instrument)

def Query(instrument, command):
    value = instrument.query(command)
    Error(instrument)
    return value

def WaitUntilSet_T(instrument, T):
    for i in range(50000):
        if ((T-T*(5/100)) <= (float(Query(instrument, ':TEMP:ACT?')[10:])) <= (T+T*(5/100))):
            break
        time.sleep(1)
    return 1

def WaitUntilSet_I(instrument, I):
    for i in range(50000):
        if ((I-I*(5/100)) <= ((float(Query(instrument, ':ILD:ACT?')[9:]))*1e3) <= (I+I*(5/100))):
            break
        time.sleep(1)
    return 1

def Error(instrument):
    err = instrument.query(":SYST:ERR?")
    if int(err[0]) == "0":
        print(err, end="\n\r")
        sys.exit()
    return 1

def Timer(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(timer, end="\n\r")
        time.sleep(1)
        t -= 1
    print("FIN")
    return 1