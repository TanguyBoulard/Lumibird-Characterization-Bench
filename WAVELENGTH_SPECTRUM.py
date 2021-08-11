# =============================================================================
# CREDITS
# =============================================================================
# Author : Tanguy BOULARD
# Date   : 28/06/2021
# Script : Data processing

# =============================================================================
# MODULES
# =============================================================================

import PRO8000
import OSA

import os
import sys
import pyvisa
import random
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import argrelextrema

# =============================================================================
# PARAMETERS
# =============================================================================

SLOT_T = 1
SLOT_LD = 3
PRO8000_offset = 5.0  # mA
RLV = 2.51

# =============================================================================
# FUNCTIONS
# =============================================================================

def Normalize(data):
    maximum = data.max()
    data_new = []
    for i in range(len(data)):
        data_new.append(data[i] - maximum)
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
    return maximum

def SignalProcessing(X, Y, nb):
    peakind = argrelextrema(Y, np.greater)
    df = (pd.DataFrame([Y[i] for i in peakind][0], [X[i] for i in peakind][0]).rolling(nb).max())
    return df.to_numpy()
    return 1

def Plot(data, title, URL):
    fig, axs = plt.subplots(1)
    fig.suptitle(title)
    normalize_level = []
    for i in range(len(data[1])):
        process = SignalProcessing(np.array(data[0]), np.array(data[1][i]), 3)
        peaks = FindPeaks(data)
        normalize_level.append(Normalize(np.array(process[1])))
        color = (random.random(), random.random(), random.random())
        axs.plot(process, label="peak: %.2f" % peaks[i][0], color=color)

    axs.set_xlabel("Wavelength (nm)")
    axs.set_ylabel("Level (dB)")
    axs.legend()
    plt.show()
    plt.savefig(URL, dpi=150)
    return 1

def Print(file0, data, title):
    file = open(file0, "w")
    file.writelines(title)
    file.writelines("\n\nI\t\tlbd")
    for i in range(len(data[0])):
        file.writelines("\n%.2f\t\t%.2f" % (data[0][i], data[1][i]))
    file.close()
    return 1

def Data(name, I_start, I_end, I_pas, T, wavelength, Span, VBW, res, Smppnt):
    
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    os.chdir(desktop)
    Number = str('%s' %name)
    Folder = str("\Wavelength Spectrum")
    mode = 0o666
    Directory = os.path.join(Number, Folder)
    if not os.path.exists(Directory):
        os.makedirs(Directory, mode)
    title = str("%s Wavelength Spectrum {T=%.2f°C}" % (name, T))
    file = str("%s/Wavelength Spectrum.txt" % Directory)
    URL = str("%s/Wavelength Spectrum.png" % Directory)

    I = []
    for i in range(I_start, I_end + I_pas, I_pas):
        I.append(i)

    X = np.linspace(wavelength - (Span / 2), wavelength + (Span / 2), Smppnt)
    lbd = []
    curve = []
    
    pro8000 = PRO8000.Initialize(T, I_start)
    osa = OSA.Initialize(I_start, I_end, I_pas, T, wavelength, Span, VBW, res, Smppnt)

    for element in I:
        PRO8000.SlotLD()
        value = PRO8000.Offset(element)
        PRO8000.Write(pro8000, ":ILD:SET %fE-3" %value)
        PRO8000.WaitUntilSet_I(pro8000, element)
        OSA.Write(osa, "GCL")
        OSA.WaitUntilEvent_SSI(osa)
        lbd.append(float(list(OSA.Query(osa, "TMK?").split(","))[0]))
        curve.append(OSA.Conversion(OSA.Query(osa, "DMA?")))

    Print(file, [I, lbd], title)
    Plot([X, curve], title, URL)

    PRO8000.Close(pro8000)
    OSA.Close(osa)
    return 1

def Stop():
    rm = pyvisa.ResourceManager()

    pro8000 = rm.open_resource("ASRL8::INSTR")
    osa = rm.open_resource("GPIB0::8::INSTR")
    
    PRO8000.Close(pro8000)
    OSA.Close(osa)

    sys.exit()
    return 1