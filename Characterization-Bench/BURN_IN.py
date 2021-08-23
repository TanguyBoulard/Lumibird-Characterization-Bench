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

def Timer(hours, mins, secs, port, I, T, wavelength, file, Span, VBW, res, Smppnt):
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
        if ((i//60)==1) and (t > 100):
            i-=60
            # ARDUINO.Write(port, b'a\r\n') # Bolometer in
            # time.sleep(5)
            u_pow, opt_pow = LIV_OnePoint(str(wavelength))
            file.writelines('\nI=%smA\tT=%s°C\tP_opt=%smW\tU=%sV' %(I, T, opt_pow, u_pow))
            time.sleep(5)
            ARDUINO.Write(port, b'b\r\n') # Bolometer out
            time.sleep(5)
            ARDUINO.Write(port, b'z\r\n') # Sphere in
            time.sleep(5)
            peak = OSA_OnePoint(float(wavelength), Span, VBW, res, Smppnt)
            file.writelines('\tlbd=%snm' %peak)
            time.sleep(5)
            ARDUINO.Write(port, b'y\r\n') # Sphere out
            time.sleep(5)
            ARDUINO.Write(port, b'a\r\n') # Bolometer in
            time.sleep(5)
            t-=100
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
    title = str("Burn-in {T=%.2f°C, I=%.2fmA, t=%ih, %imin, %is}" % (T, I, hours, mins, secs))
    file = str("%s/Burn-in.txt" %Directory) 
    f = open(file,"w")
    f.writelines(title)

    pro8000 = PRO8000.Initialize(T, I)
    Timer(int(hours), int(mins), int(secs), port, I, T, wavelength, f, Span, VBW, res, Smppnt)
    PRO8000.Close(pro8000)
    
    f.close()
    return 1
    

def Stop():
    rm = pyvisa.ResourceManager()
    pro8000 = rm.open_resource("ASRL8::INSTR")
    PRO8000.Close(pro8000)
    sys.exit()
    return 1