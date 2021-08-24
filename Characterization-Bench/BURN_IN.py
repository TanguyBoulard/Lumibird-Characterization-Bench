# =============================================================================
# CREDITS
# =============================================================================
# Author : Tanguy BOULARD
# Date   : 28/06/2021
# Script : Burn-in

# =============================================================================
# MODULES
# =============================================================================

import PRO8000
import ARDUINO
import KEYSIGHT
import P_LINK
import OSA

import pyvisa
import sys
import os
import time

# =============================================================================
# FUNCTIONS
# =============================================================================

def LIV_OnePoint(wavelength):
    multimeter = KEYSIGHT.Initialize()
    bolometer = P_LINK.Initialize(str(wavelength))
    u_pow = KEYSIGHT.Read(multimeter)
    opt_pow = P_LINK.Read(bolometer)
    KEYSIGHT.Close(multimeter)
    P_LINK.Close(bolometer)
    return str(u_pow), str(opt_pow)

def OSA_OnePoint(wavelength, Span, VBW, res, Smppnt):
    osa = OSA.Initialize(float(wavelength), Span, VBW, float(res), Smppnt)
    OSA.Write(osa, "GCL")
    OSA.WaitUntilEvent_SSI(osa)
    lbd = float(list(OSA.Query(osa, "TMK?").split(","))[0])
    OSA.Close(osa)
    return lbd

def Timer(hours, mins, secs, port, I, T, wavelength, Span, VBW, res, Smppnt):
    
    title = str("Burn-in {T=%.2f°C, I=%.2fmA, t=%ih, %imin, %is}" % (float(T), float(I), int(hours), int(mins), int(secs)))
    file_1h = str("Burn-in 1h.txt")
    file_20min = str("Burn-in 20min.txt") 
    f_1h = open(file_1h,"w")
    f_1h.writelines(title)
    
    t = hours*3600 + mins*60 + secs
    i = 0
    while t>=0:
        hours, remainder = divmod(t, 3600)
        mins, secs = divmod(remainder, 60)
        timer = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
        print(timer, end='\n\r')
        time.sleep(1)
        t-=1
        i+=1
        if ((i%1200)==0) and (t > 20):
            f_20min = open(file_20min,"w")
            u_pow0, opt_pow0 = LIV_OnePoint(str(wavelength))
            f_20min.writelines('t=%ih, %imin, %is\tU=%sV\tP_opt=%smW' %(int(hours), int(mins), int(secs), str(u_pow0), str(opt_pow0)))
            f_20min.close()
        if ((i%3600)==0) and (t > 100):
            f_1h = open(file_1h,"w")
            # ARDUINO.Write(port, b'a\r\n') # Bolometer in
            # time.sleep(5)
            u_pow, opt_pow = LIV_OnePoint(str(wavelength))
            file_1h.writelines('\nI=%smA\tT=%s°C\tP_opt=%smW\tU=%sV' %(float(I), float(T), str(opt_pow), str(u_pow)))
            time.sleep(5)
            ARDUINO.Write(port, b'b\r\n') # Bolometer out
            time.sleep(5)
            ARDUINO.Write(port, b'z\r\n') # Sphere in
            time.sleep(5)
            peak = OSA_OnePoint(float(wavelength), Span, VBW, res, Smppnt)
            file_1h.writelines('\tlbd=%snm' %str(peak))
            time.sleep(5)
            ARDUINO.Write(port, b'y\r\n') # Sphere out
            time.sleep(5)
            ARDUINO.Write(port, b'a\r\n') # Bolometer in
            time.sleep(5)
            t-=100
            f_1h.close()
    return 1

def main(I, T, hours, mins, secs, port, wavelength, name, Span, VBW, res, Smppnt):

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    os.chdir(desktop)
    Name = str("%s/" %name)
    Folder = str("Burn-in")
    mode = 0o666
    Directory = os.path.join(Name, Folder)
    if not os.path.exists(Directory):
        os.makedirs(Directory, mode)
    os.chdir(Directory)

    pro8000 = PRO8000.Initialize(T, I)
    Timer(int(hours), int(mins), int(secs), port, I, T, wavelength, Span, VBW, res, Smppnt)
    PRO8000.Close(pro8000)
    
    return 1
    

def Stop():
    rm = pyvisa.ResourceManager()
    pro8000 = rm.open_resource("ASRL8::INSTR")
    PRO8000.Close(pro8000)
    sys.exit()
    return 1