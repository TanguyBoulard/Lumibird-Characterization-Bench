# =============================================================================
# CREDITS
# =============================================================================
# Author : Tanguy BOULARD
# Date   : 28/06/2021
# Script : Light-Current-Voltage Characteristics

# =============================================================================
# MODULES
# =============================================================================

import PRO8000
import P_LINK
import KEYSIGHT

import os
import pyvisa
import matplotlib.pyplot as plt

# =============================================================================
# FUNCTIONS
# =============================================================================

def Plot(data, title, URL):
    fig, axs = plt.subplots(2)
    fig.suptitle(title)

    axs[0].plot(data[0], data[2], color="b")
    axs[1].plot(data[0], data[1], color="r")

    axs[0].set_ylabel("Output Power (mW)")
    axs[1].set_xlabel("Forward Current (mA)")
    axs[1].set_ylabel("Forward Voltage (V)")

    plt.savefig(URL, dpi=150)
    plt.show()
    return 1

def Print(file, data, title):
    file = open(file, "w")
    file.writelines(title)
    file.writelines("\n\nI\t\tU\t\tP_opt")
    for i in range(len(data[0])):
        file.writelines("\n%f\t%f\t%f" % (data[0][i], data[1][i], data[2][i]))
    file.close()
    return 1

def Data(name, I_start, I_end, I_pas, T, wavelength):

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    os.chdir(desktop)
    Name = str("%s/" % name)
    Folder = str("Light-Current-Voltage Characteristics")
    mode = 0o666
    Directory = os.path.join(Name, Folder)
    if not os.path.exists(Directory):
        os.makedirs(Directory, mode)
    title = str("Light-Current-Voltage Characteristics {T=%.2f°C}" %T)
    file = str("%s/Light-Current-Voltage Characteristics.txt" %Directory)
    URL = str("%s/Light_Current_Voltage_Characteristics.png" %Directory)
    
    I = [i for i in range(I_start, I_end + int(I_pas), int(I_pas))]
    U = []
    P_opt = []

    pro8000 = PRO8000.Initialize(T, I_start)
    multimeter = KEYSIGHT.Initialize()
    bolometer = P_LINK.Initialize(wavelength)
    
    offset = P_LINK.Read(bolometer)
    print('offset bolometre = %fmW' %offset)

    for element in I:
        PRO8000.SlotLD(pro8000)
        value = PRO8000.Offset(element)
        PRO8000.Write(pro8000, ":ILD:SET %fE-3" %value)
        PRO8000.WaitUntilSet_I(pro8000, element)
        U.append(KEYSIGHT.Read(multimeter))
        P_opt.append(P_LINK.Read(bolometer) * 1E3)  # VALUE

    data = [I, U, P_opt]
    Plot(data, title, URL)
    Print(file, data, title)
    
    PRO8000.Close(pro8000)
    KEYSIGHT.Close(multimeter)
    P_LINK.Close(bolometer)
    return 1

def Stop():
    rm = pyvisa.ResourceManager()
    pro8000 = rm.open_resource("ASRL8::INSTR")
    multimeter = rm.open_resource("USB0::0x2A8D::0xB318::MY58260020::INSTR")
    bolometer = rm.open_resource("ASRL5::INSTR")
    
    PRO8000.Close(pro8000)
    KEYSIGHT.Close(multimeter)
    P_LINK.Close(bolometer)
    return 1