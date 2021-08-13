# =============================================================================
# CREDITS
# =============================================================================
# Author : Tanguy BOULARD
# Date   : 28/06/2021
# Script : OSA

# =============================================================================
# MODULES
# =============================================================================

import pyvisa
import time
import sys

# =============================================================================
# PARAMETERS
# =============================================================================

RLV = 2.51

# =============================================================================
# FUNCTIONS
# =============================================================================

def Write(instrument, command):
    instrument.write(command)
    Error(instrument)
    return 1

def Query(instrument, command):
    value = instrument.query(command)
    Error(instrument)
    return value

def Error(instrument):
    err = instrument.query("ERR?")
    if err != "000\r\n":
        print(err, end="\n\r")
        sys.exit()
    return 1

def WaitUntilEvent_SSI(instrument):
    instrument.write("*CLS")
    instrument.write("SSI")
    for i in range(50000):
        if int(instrument.query("ESR2?")) == 3:
            break
        time.sleep(1)
    return 1

def WaitUntilEvent_RST(instrument):
    instrument.write("*CLS")
    instrument.write("*ESE 61")
    instrument.write("ESE2")
    instrument.write("*SRE 36")
    instrument.write("*RST")
    for i in range(50000):
        if int(instrument.query("*STB?")) == 96:
            instrument.write("*ESE 0")
            instrument.write("*ESE2 0")
            instrument.write("*SRE 0")
            break
        time.sleep(1)
    return 1

def Conversion(data):
    data = list(data.split("\r\n"))
    for i in range(len(data) - 1):
        data[i] = float(data[i])
    return data[:-1]

def Initialize(I_start, I_end, I_pas, T, wavelength, Span, VBW, res, Smppnt):
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())
    
    instrument = rm.open_resource("GPIB0::8::INSTR")
    instrument.read_termination = ""
    instrument.write_termination = ""
    instrument.baud_rate = 9600
    instrument.delay = 500
    instrument.timeout = 100000
    if Query(instrument, "*IDN?") != "ANRITSU,MS9710B,0,V3.11&V3.8\r\n":
        print("OSA not connected")
        sys.exit()
    instrument.clear()
    WaitUntilEvent_RST(instrument)
    Write(instrument, "*CLS;HEAD OFF")
    Write(instrument, "BUZ OFF")
    Write(instrument, "CNT %f" % wavelength)
    Write(instrument, "SPN %f" % Span)
    Write(instrument, "RLV %f" % RLV)
    Write(instrument, "VBW %i" % VBW)
    Write(instrument, "RES %f" % res)
    Write(instrument, "MPT %i" % Smppnt)
    Write(instrument, "WDP AIR")
    Write(instrument, "ATT OFF")
    Write(instrument, "PKS PEAK")
    Write(instrument, "GCL")
    
    return instrument
    
def Close(instrument):
    instrument.write(instrument, "EMK")
    instrument.write(instrument, "GCL")
    instrument.write(instrument, "ZMK ERS")
    instrument.close()
    return 1