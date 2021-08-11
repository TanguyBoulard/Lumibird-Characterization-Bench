# =============================================================================
# CREDITS
# =============================================================================
# Author : Tanguy BOULARD
# Date   : 28/06/2021
# Script : Data processing

# =============================================================================
# MODULES
# =============================================================================

import pyvisa
import sys

# =============================================================================
# FUNCTIONS
# =============================================================================

def Read(instrument):
    return float(Query("MEAS:PRIM:VOLT:DC?"))

def Write(instrument, command):
    instrument.write(command)
    Error(instrument)
    return 1

def Query(instrument, command):
    value = instrument.query(command)
    Error(instrument)
    return value

def Error(instrument):
    err = instrument.query(":SYST:ERR?")
    if int(err[1]) != 0:
        print(err, end="\n\r")
        sys.exit()
    return 1

def Initialize():
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())
    
    instrument = rm.open_resource("USB0::0x2A8D::0xB318::MY58260020::INSTR")
    instrument.read_termination = "\n"
    instrument.write_termination = "\r\n"
    instrument.baud_rate = 9600
    if (Query(instrument, "*IDN?")!= "Keysight Technologies,34450A,MY58260020,01.02-01.00"):
        print("KEYSIGHT 34450A not connected")
        sys.exit()
    instrument.clear()
    instrument.write(instrument, "*RST")
    instrument.write(instrument, "*CLS")
    instrument.write(instrument, ":CONF:VOLT:DC")
    
    return instrument
    
def Close(instrument):
    Write("*RST")
    instrument.close()
    return 1