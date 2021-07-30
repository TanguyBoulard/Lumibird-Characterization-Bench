# =============================================================================
# LIV CONDITIONS
# =============================================================================

numero = '1146 après burn-in'

name = 'LD-PD'
wavelength = '0980' #nm format 0000
T = 25.0 #°C
SLOT_T = 1
I_start = 0 #mA
I_end = 500 #mA
pas = 10 #mA
SLOT_LD = 3
PRO8000_offset = 5.0 #mA

# =============================================================================
# LIBRAIRIES
# =============================================================================

import os
import sys
import pyvisa
import time
import matplotlib.pyplot as plt

# =============================================================================
# FOLDER
# =============================================================================

Number = str("%s/" %numero)
Folder = str("Light-Current-Voltage Characteristics")
mode = 0o666
Directory = os.path.join(Number, Folder)
if not os.path.exists(Directory):
    os.makedirs(Directory, mode)
title = str("%s Light-Current-Voltage Characteristics {T=%f°C}" %(name, T))
file = str("%s/Light-Current-Voltage Characteristics.txt" %Directory)
URL = str("%s/Light-Current-Voltage Characteristics.png" %Directory)

# =============================================================================
# FUNCTIONS
# =============================================================================

def Plot(data, title, URL):
    fig, axs = plt.subplots(2)
    fig.suptitle(title)

    axs[0].plot(data[0], data[2], color='b')
    axs[1].plot(data[0], data[1], color='r')

    axs[0].set_ylabel("Output Power (mW)")
    axs[1].set_xlabel("Forward Current (mA)")
    axs[1].set_ylabel("Forward Voltage (V)")

    plt.savefig(URL, dpi=150)

def Print(file, data, title):
    file = open(file,"w")
    file.writelines(title)
    file.writelines('\n\nI\t\tU\t\tP_opt')
    for i in range(len(data[0])):
        file.writelines('\n%f\t%f\t%f' %(data[0][i], data[1][i], data[2][i]))
    file.close()

def PRO8000Error():
    err = pro8000.query(':SYST:ERR?')
    if int(err[0]) == '0':
        print(err, end="\n\r")

def KEYSIGHTError():
    err = multimeter.query(':SYST:ERR?')
    if int(err[1]) != 0:
        print(err, end="\n\r")

def PRO8000WaitUntilSet_T(T):
    for i in range (50000):
        print('T = %.2f°C' %(float(pro8000.query(':TEMP:ACT?')[10:])))
        if (T-T*(5/100) <= (float(pro8000.query(':TEMP:ACT?')[10:])) <= T+T*(5/100)):
            break
        time.sleep(20)

def PRO8000WaitUntilSet_I(I):
    for i in range (50000):
        print('I = %.2fmA' %((float(pro8000.query(':ILD:ACT?')[9:]))*1E3))
        if (I-I*(5/100) <= ((float(pro8000.query(':ILD:ACT?')[9:]))*1E3) <= I+I*(5/100)):
            break
        time.sleep(1)

I = [i for i in range(0, I_end+pas, pas)]

U = []
P_opt = []

# =============================================================================
# SET UP
# =============================================================================

rm = pyvisa.ResourceManager()
# print(rm.list_resources())

    #Modular Platform
pro8000 = rm.open_resource('ASRL8::INSTR')
pro8000.read_termination = '\n'
pro8000.write_termination = '\n'
pro8000.baud_rate = 19200
query_delay = 0.1
if pro8000.query('*IDN?') != 'PROFILE, PRO8000, 0, Ver.4.28-1.22\r':
    print('pro8000 not connected')
    sys.exit()
pro8000.clear()
pro8000.write('*RST')
pro8000.write('*CLS')

    #MULTIMETER

multimeter = rm.open_resource('USB0::0x2A8D::0xB318::MY58260020::INSTR')
multimeter.read_termination = '\n'
multimeter.write_termination = '\r\n'
multimeter.baud_rate = 9600
if multimeter.query('*IDN?') != 'Keysight Technologies,34450A,MY58260020,01.02-01.00':
    print('KEYSIGHT 34450A not connected')
    sys.exit()
multimeter.clear()
multimeter.write('*RST')
multimeter.write('*CLS')

    #BOLOMETER

bolometer = rm.open_resource('ASRL5::INSTR')
bolometer.read_termination = '\r\r\n'
bolometer.write_termination = '\n'
bolometer.baud_rate = 57600
delay = 100
if bolometer.query('*NAM') != 'UP19K-30H-H5\t':
    print('Gentec-eo U-link not connected')
    sys.exit()
bolometer.clear()
# bolometer.write('*RST')

# =============================================================================
# INITIALIZATION
# =============================================================================

    #PRO8000

pro8000.write(':SLOT %i' %SLOT_T)
pro8000.write(':TEMP:SET %f' %T)
pro8000.write(':TEC ON')
PRO8000WaitUntilSet_T(T)
PRO8000Error()

pro8000.write(':SLOT %i' %SLOT_LD)
if I_start != 0:
    value = I_start + PRO8000_offset #aucune idée de pourquoi un offset de 5
else:
    value = I_start
pro8000.write(':ILD:SET %fE-3' %value)
pro8000.write(':LASER ON')
PRO8000WaitUntilSet_I(I_start)
PRO8000Error()

    #MULTIMETER

multimeter.write(':CONF:VOLT:DC')
KEYSIGHTError()

    #BOLOMETER

bolometer.query('*ANT')
bolometer.query('*CFT')
bolometer.query('*CMX')
bolometer.query('*FAS')
bolometer.query('*PWC%s' %str(wavelength))
bolometer.query('*MUL10.0E+00')
bolometer.write('*CVU')
bolometer.read() #ACK
offset = float(bolometer.read()) #VALUE

# =============================================================================
# ACQUISITION
# =============================================================================

for element in I:
    pro8000.write(':SLOT %i' %SLOT_LD)
    if element != 0:
        value = element + PRO8000_offset #aucune idée de pourquoi un offset de 5
    else:
        value = element
    pro8000.write(':ILD:SET %fE-3' %value)
    PRO8000WaitUntilSet_I(element)
    U.append(float(multimeter.query('MEAS:PRIM:VOLT:DC?')))
    bolometer.write('*CVU')
    bolometer.read() #ACK
    P_opt.append(float(bolometer.read())*1E3) #VALUE

# =============================================================================
# END
# =============================================================================

    #PRO8000

pro8000.write(':SLOT %i' %SLOT_T)
pro8000.write(':TEC OFF')
PRO8000Error()

pro8000.write(':SLOT %i' %SLOT_LD)
pro8000.write(':LASER OFF')
PRO8000Error()

pro8000.write('*RST')
pro8000.close()

    #MULTIMETER

multimeter.write('*RST')
multimeter.close()

    #BOLOMETER

bolometer.write('*RST')
bolometer.close()

# =============================================================================
# PLOT
# =============================================================================

data = [I, U, P_opt]
Plot(data, title, URL)
Print(file, data, title)
