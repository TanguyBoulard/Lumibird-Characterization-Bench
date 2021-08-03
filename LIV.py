import os
import sys
import pyvisa
import time
import matplotlib.pyplot as plt

SLOT_T = 1
SLOT_LD = 3
PRO8000_offset = 5.0 #mA

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

def PRO8000Error(instrument):
    err = instrument.query(':SYST:ERR?')
    if int(err[0]) == '0':
        print(err, end="\n\r")

def KEYSIGHTError(instrument):
    err = instrument.query(':SYST:ERR?')
    if int(err[1]) != 0:
        print(err, end="\n\r")

def PRO8000WaitUntilSet_T(instrument, T):
    for i in range (50000):
        print('T = %.2f°C' %(float(instrument.query(':TEMP:ACT?')[10:])))
        if (T-T*(5/100) <= (float(instrument.query(':TEMP:ACT?')[10:])) <= T+T*(5/100)):
            break
        time.sleep(20)

def PRO8000WaitUntilSet_I(instrument, I):
    for i in range (50000):
        print('I = %.2fmA' %((float(instrument.query(':ILD:ACT?')[9:]))*1E3))
        if (I-I*(5/100) <= ((float(instrument.query(':ILD:ACT?')[9:]))*1E3) <= I+I*(5/100)):
            break
        time.sleep(1)

def Data(name, I_start, I_end, I_pas, T, wavelength):

    Name = str("%s/" %name)
    Folder = str("Light-Current-Voltage Characteristics")
    mode = 0o666
    Directory = os.path.join(Name, Folder)
    if not os.path.exists(Directory):
        os.makedirs(Directory, mode)
    title = str("%s Light-Current-Voltage Characteristics {T=%.2f°C}" %(name, T))
    file = str("%s/Light-Current-Voltage Characteristics.txt" %Directory)
    URL = str("%s/Light-Current-Voltage Characteristics.png" %Directory)

    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())

        #Modular Platform
    pro8000 = rm.open_resource('ASRL8::INSTR')
    pro8000.read_termination = '\n'
    pro8000.write_termination = '\n'
    pro8000.baud_rate = 19200
    pro8000.query_delay = 0.1
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
    bolometer.delay = 100
    if bolometer.query('*NAM') != 'UP19K-30H-H5\t':
        print('Gentec-eo U-link not connected')
        sys.exit()
    bolometer.clear()

        #PRO8000
    pro8000.write(':SLOT %i' %SLOT_T)
    pro8000.write(':TEMP:SET %f' %T)
    pro8000.write(':TEC ON')
    PRO8000WaitUntilSet_T(pro8000, T)
    PRO8000Error(pro8000)

    pro8000.write(':SLOT %i' %SLOT_LD)
    if I_start != 0 and I_start != 10:
        value = I_start + PRO8000_offset #aucune idée de pourquoi un offset de 5
    elif I_start == 10:
        value = I_start + 5
    else:
        value = I_start
    pro8000.write(':ILD:SET %fE-3' %value)
    pro8000.write(':LASER ON')
    PRO8000WaitUntilSet_I(pro8000, I_start)
    PRO8000Error(pro8000)

        #MULTIMETER
    multimeter.write(':CONF:VOLT:DC')
    KEYSIGHTError(multimeter)

        #BOLOMETER
    bolometer.query('*ANT')
    bolometer.query('*CFT')
    bolometer.query('*CMX')
    bolometer.query('*FAS')
    l = len(str(wavelength))
    if l != 4:
        for i in range(l):
            wavelength = '0'+wavelength[:]
    bolometer.query('*PWC%s' %str(wavelength))
    bolometer.query('*MUL10.0E+00')
    bolometer.write('*CVU')
    bolometer.read() #ACK
    offset = float(bolometer.read()) #VALUE

    I = [i for i in range(I_start, I_end+int(I_pas), int(I_pas))]
    U = []
    P_opt = []

    for element in I:
        pro8000.write(':SLOT %i' %SLOT_LD)
        if element != 0 and I_start != 10:
            value = element + PRO8000_offset #aucune idée de pourquoi un offset de 5
        elif I_start == 10:
            value = element + 5 #aucune idée de pourquoi un offset de 8
        else:
            value = element
        pro8000.write(':ILD:SET %fE-3' %value)
        PRO8000WaitUntilSet_I(pro8000, element)
        U.append(float(multimeter.query('MEAS:PRIM:VOLT:DC?')))
        bolometer.write('*CVU')
        bolometer.read() #ACK
        P_opt.append(float(bolometer.read())*1E3) #VALUE

    data = [I, U, P_opt]
    Plot(data, title, URL)
    Print(file, data, title)

def Stop():
    rm = pyvisa.ResourceManager()

        #PRO8000
    pro8000 = rm.open_resource('ASRL8::INSTR')
    pro8000.write(':SLOT %i' %SLOT_T)
    pro8000.write(':TEC OFF')
    PRO8000Error(pro8000)

    pro8000.write(':SLOT %i' %SLOT_LD)
    pro8000.write(':LASER OFF')
    PRO8000Error(pro8000)

    pro8000.write('*RST')
    pro8000.close()

        #MULTIMETER
    multimeter = rm.open_resource('USB0::0x2A8D::0xB318::MY58260020::INSTR')
    multimeter.write('*RST')
    multimeter.close()

        #BOLOMETER
    bolometer = rm.open_resource('ASRL5::INSTR')
    bolometer.write('*RST')
    bolometer.close()