import os
import sys
import pyvisa
import random
import time
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import argrelextrema

def Normalize(data):
    maximum = data.max()
    data_new = []
    for i in range(len(data)):
        data_new.append(data[i]-maximum)
    return np.array(data_new, dtype=float)

def FindPeaks(data):
    maximum = []
    for i in range(len(data[1])):
        peaks, _ = find_peaks(data[1][i])
        maximum.append([])
        m = []
        for index in peaks:
            m.append(data[1][i][index])
        mf = np.array(m, dtype=float)
        max = mf.max()
        max_indexes = np.where(mf == max)
        maximum[i].append(data[0][peaks[max_indexes[0][0]]])
    return(maximum)

def SignalProcessing(X, Y, nb):
    peakind = argrelextrema(Y, np.greater)
    df = pd.DataFrame([Y[i] for i in peakind][0], [X[i] for i in peakind][0]).rolling(nb).max()
    return df.to_numpy()

def Plot(data, title, URL):
    fig, axs = plt.subplots(1)
    fig.suptitle(title)
    normalize_level = []
    for i in range(len(data[1])):
        process = SignalProcessing(np.array(data[0]), np.array(data[1][i]), 3)
        peaks = FindPeaks(data)
        normalize_level.append(Normalize(np.array(process[1])))
        color = (random.random(), random.random(), random.random())
        axs.plot(process, label='peak: %.2f' %peaks[i][0], color=color)

    axs.set_xlabel("Wavelength (nm)")
    axs.set_ylabel("Level (dB)")
    axs.legend()
    plt.savefig(URL, dpi=150)

def Print(file0, data, title):
    file = open(file0,"w")
    file.writelines(title)
    file.writelines('\n\nI\t\tlbd')
    for i in range(len(data[0])):
        file.writelines('\n%.2f\t\t%.2f' %(data[0][i], data[1][i]))
    file.close()

def PRO8000Error(instrument):
    err = instrument.query(':SYST:ERR?')
    if int(err[0]) == '0':
        print(err, end="\n\r")

def PRO8000WaitUntilSet_T(instrument, T):
    for i in range (50000):
        print('%f°C' %(float(instrument.query(':TEMP:ACT?')[10:])))
        if (T-T*(5/100) <= (float(instrument.query(':TEMP:ACT?')[10:])) <= T+T*(5/100)):
            break
        time.sleep(20)

def PRO8000WaitUntilSet_I(instrument, I):
    for i in range (50000):
        print('%fmA' %((float(instrument.query(':ILD:ACT?')[9:]))*1E3))
        if (I-I*(5/100) <= ((float(instrument.query(':ILD:ACT?')[9:]))*1E3) <= I+I*(5/100)):
            break
        time.sleep(1)

def OSAError(instrument):
    err = instrument.query('ERR?')
    if err != '000\r\n':
        print(err, end="\n\r")

def OSAWaitUntilEvent_SSI(instrument):
    instrument.write('*CLS')
    instrument.write('SSI')
    for i in range(50000):
        if int(instrument.query('ESR2?')) == 3:
            break
        time.sleep(1)

def OSAWaitUntilEvent_RST(instrument):
    instrument.write('*CLS')
    instrument.write('*ESE 61')
    instrument.write('ESE2')
    instrument.write('*SRE 36')
    instrument.write('*RST')
    for i in range(50000):
        if int(instrument.query('*STB?')) == 96:
            instrument.write('*ESE 0')
            instrument.write('*ESE2 0')
            instrument.write('*SRE 0')
            break
        time.sleep(1)

def OSAConversion(data):
    data = list(data.split('\r\n'))
    for i in range(len(data)-1):
        data[i] = float(data[i])
    return data[:-1]

def Data(name, I_start, I_end, I_pas, T, wavelength, Span, VBW, res, Smppnt):

    SLOT_T = 1
    SLOT_LD = 3
    PRO8000_offset = 5.0 #mA
    RLV = 2.51

    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())

        #PRO8000
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

        #OSA
    osa = rm.open_resource('GPIB0::8::INSTR')
    osa.read_termination = ''
    osa.write_termination = ''
    osa.baud_rate = 9600
    osa.delay = 500
    osa.timeout = 100000
    if osa.query('*IDN?') != 'ANRITSU,MS9710B,0,V3.11&V3.8\r\n':
        print('OSA not connected')
        sys.exit()
    osa.clear()
    # OSAWaitUntilEvent_RST(osa)
    osa.write('*CLS;HEAD OFF')

        #PRO8000
    pro8000.write(':SLOT %i' %SLOT_T)
    pro8000.write(':TEMP:SET %f' %T)
    pro8000.write(':TEC ON')
    PRO8000WaitUntilSet_T(pro8000, T)
    PRO8000Error(pro8000)

    pro8000.write(':SLOT %i' %SLOT_LD)
    if I_start != 0:
        value = I_start + PRO8000_offset #aucune idée de pourquoi un offset de 5
    else:
        value = I_start
    pro8000.write(':ILD:SET %fE-3' %value)
    pro8000.write(':LASER ON')
    PRO8000WaitUntilSet_I(pro8000, I_start)
    PRO8000Error(pro8000)

        #OSA
    osa.write('BUZ OFF')
    osa.write('CNT %f' %wavelength)
    osa.write('SPN %f' %Span)
    osa.write('RLV %f' %RLV)
    osa.write('VBW %i' %VBW)
    osa.write('RES %f' %res)
    osa.write('MPT %i' %Smppnt)
    osa.write('WDP AIR')
    osa.write('ATT OFF')
    osa.write('PKS PEAK')
    osa.write('GCL')
    OSAError(osa)

    Number = str("%s/" %name)
    Folder = str("Wavelength Spectrum")
    mode = 0o666
    Directory = os.path.join(Number, Folder)
    if not os.path.exists(Directory):
        os.makedirs(Directory, mode)
    title = str("%s Wavelength Spectrum {T=%.2f°C}" %(name, T))
    file = str("%s/Wavelength Spectrum.txt" %Directory)
    URL = str("%s/Wavelength Spectrum.png" %Directory)

    I = []
    for i in range(I_start, I_end+I_pas, I_pas):
        I.append(i)

    X = np.linspace(wavelength-(Span/2), wavelength+(Span/2), Smppnt)
    lbd = []
    curve = []

    for element in I:
        pro8000.write(':SLOT %i' %SLOT_LD)
        if I_start != 0:
            value = element + PRO8000_offset #aucune idée de pourquoi un offset de 5
        else:
            value = element
        pro8000.write(':ILD:SET %fE-3' %value)
        PRO8000WaitUntilSet_I(pro8000, element)
        PRO8000Error(pro8000)
        osa.write('GCL')
        OSAWaitUntilEvent_SSI(osa)
        OSAError(osa)
        lbd.append(float(list(osa.query('TMK?').split(','))[0]))
        curve.append(OSAConversion(osa.query('DMA?')))

    Print(file, [I, lbd], title)
    Plot([X, curve], title, URL)

        #PRO8000
    pro8000.write(':SLOT %i' %SLOT_T)
    pro8000.write(':TEC OFF')
    PRO8000Error(pro8000)

    pro8000.write(':SLOT %i' %SLOT_LD)
    pro8000.write(':LASER OFF')
    PRO8000Error(pro8000)

    pro8000.write('*RST')
    pro8000.close()

        #OSA
    osa.write('EMK')
    osa.write('GCL')
    osa.write('ZMK ERS')
    osa.close()

def Stop():

    SLOT_T = 1
    SLOT_LD = 3

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

        #OSA
    osa = rm.open_resource('GPIB0::8::INSTR')
    osa.write('EMK')
    osa.write('GCL')
    osa.write('ZMK ERS')
    osa.close()

    sys.exit()