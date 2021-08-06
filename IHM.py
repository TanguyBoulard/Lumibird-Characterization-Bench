import BURN_IN
import LIV
import WAVELENGTH_SPECTRUM

import tkinter as tk
from functools import partial
from tkinter import ttk

import serial
import time

ended = False

port = serial.Serial('COM16', 115200)
if not port.isOpen():
    port.open()
port.flush()

def Write(command):
    port.write(command)
    for _ in range(len(command)):
       port.read() # Read the loopback chars and ignore

def Read():
    while True:
        reply = b''
        a = port.read()
        if a == b'\r':
            break
        else:
            reply += a
            time.sleep(0.01)
    return reply

class Characterization(tk.Toplevel):

    command = []

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Caractérisation")

        # State display (0,0)
        self.lf_state_display = tk.LabelFrame(self, text="Etat")
        self.lf_state_display.grid(row=0, column=0, sticky="nesw")

        # Error (0,0) -> (0,1)
        self.text_error = tk.Label(self.lf_state_display, text="")
        self.text_error.grid(row=0, column=1, sticky="nesw")

        # Separator (1,[...])
        separator = tk.Label(self, text="P(I)")
        separator.grid(row=1, columnspan=10, sticky="ew")

        # Measurment conditions

        # Temperature  (2,1)
        self.lf_Temperature = tk.LabelFrame(self, text="Température")
        self.lf_Temperature.grid(row=2, column=1, sticky="nesw")

        # T  (2,1) -> (0,[0,1,2])
        text_temperature = tk.Label(self.lf_Temperature, text="Température :")
        text_temperature.grid(row=0, column=0, sticky="e")
        input_temperature = tk.Entry(self.lf_Temperature, textvariable="")
        self.command.append(input_temperature)
        input_temperature.grid(row=0, column=1, sticky="nesw")
        text_temperature_unit = tk.Label(self.lf_Temperature, text="°C")
        text_temperature_unit.grid(row=0, column=2, sticky="w")

        # Intensity (2,0)
        self.lf_Intensity = tk.LabelFrame(self, text="Intensité")
        self.lf_Intensity.grid(row=2, column=0, sticky="nesw")

        # I_start (2,0) -> (0,[0,1,2])
        text_I_start = tk.Label(self.lf_Intensity, text="I_début :")
        text_I_start.grid(row=0, column=0, sticky="e")
        input_I_start = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_I_start)
        input_I_start.grid(row=0, column=1, sticky="nesw")
        text_I_start_unit = tk.Label(self.lf_Intensity, text="mA")
        text_I_start_unit.grid(row=0, column=2, sticky="w")

        # I_end (2,0) -> (1,[0,1,2])
        text_I_end = tk.Label(self.lf_Intensity, text="I_fin :")
        text_I_end.grid(row=1, column=0, sticky="e")
        input_I_end = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_I_end)
        input_I_end.grid(row=1, column=1, sticky="nesw")
        text_I_end_unit = tk.Label(self.lf_Intensity, text="mA")
        text_I_end_unit.grid(row=1, column=2, sticky="w")

        # Step (2,0) -> (2,[0,1,2])
        text_step = tk.Label(self.lf_Intensity, text="pas :")
        text_step.grid(row=2, column=0, sticky="e")
        input_step = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_step)
        input_step.grid(row=2, column=1, sticky="nesw")
        text_step_unit = tk.Label(self.lf_Intensity, text="mA")
        text_step_unit.grid(row=2, column=2, sticky="w")
        
        # Intensity OSA (4,0)
        self.lf_IntensityOSA = tk.LabelFrame(self, text="Intensité")
        self.lf_IntensityOSA.grid(row=4, column=0, sticky="nesw")

        # I_start (2,0) -> (0,[0,1,2])
        text_I_startOSA = tk.Label(self.lf_IntensityOSA, text="I_début :")
        text_I_startOSA.grid(row=0, column=0, sticky="e")
        input_I_startOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_I_startOSA)
        input_I_startOSA.grid(row=0, column=1, sticky="nesw")
        text_I_startOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_I_startOSA_unit.grid(row=0, column=2, sticky="w")

        # I_end (2,0) -> (1,[0,1,2])
        text_I_endOSA = tk.Label(self.lf_IntensityOSA, text="I_fin :")
        text_I_endOSA.grid(row=1, column=0, sticky="e")
        input_I_endOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_I_endOSA)
        input_I_endOSA.grid(row=1, column=1, sticky="nesw")
        text_I_endOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_I_endOSA_unit.grid(row=1, column=2, sticky="w")

        # Step (2,0) -> (2,[0,1,2])
        text_stepOSA = tk.Label(self.lf_IntensityOSA, text="pas :")
        text_stepOSA.grid(row=2, column=0, sticky="e")
        input_stepOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_stepOSA)
        input_stepOSA.grid(row=2, column=1, sticky="nesw")
        text_stepOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_stepOSA_unit.grid(row=2, column=2, sticky="w")

        # Temperature  (2,1)
        self.lf_TemperatureOSA = tk.LabelFrame(self, text="Température")
        self.lf_TemperatureOSA.grid(row=4, column=1, sticky="nesw")

        # T  (2,1) -> (0,[0,1,2])
        text_temperatureOSA = tk.Label(self.lf_TemperatureOSA, text="Température :")
        text_temperatureOSA.grid(row=0, column=0, sticky="e")
        input_temperatureOSA = tk.Entry(self.lf_TemperatureOSA, textvariable="")
        self.command.append(input_temperatureOSA)
        input_temperatureOSA.grid(row=0, column=1, sticky="nesw")
        text_temperatureOSA_unit = tk.Label(self.lf_TemperatureOSA, text="°C")
        text_temperatureOSA_unit.grid(row=0, column=2, sticky="w")

        # OSA ([5,6],[0,1])
        self.lf_OSA = tk.LabelFrame(self, text="OSA")
        self.lf_OSA.grid(row=5, rowspan=1, columnspan=2, sticky="nesw")

        # Span ([5,6],[0,1]) -> (0,[0,1,2])
        text_span = tk.Label(self.lf_OSA, text="Plage de mesure :")
        text_span.grid(row=0, column=0, sticky="e")
        input_span = tk.Entry(self.lf_OSA, textvariable="")
        self.command.append(input_span)
        input_span.grid(row=0, column=1, sticky="nesw")
        text_span_unit = tk.Label(self.lf_OSA, text="nm\t")
        text_span_unit.grid(row=0, column=2, sticky="w")

        # VBW ([4,5],[0,1]) -> (0,[3,4,5])
        VBW_option_list = [1E1, 1E2, 1E3, 1E4, 1E5, 1E6]
        text_VBW = tk.Label(self.lf_OSA, text="Fréquence d'échantillonnage :")
        text_VBW.grid(row=0, column=3, sticky="e")
        input_VBW = tk.StringVar(self.lf_OSA)
        input_VBW.set(VBW_option_list[2])
        self.command.append(input_VBW)
        opt_VBW = tk.OptionMenu(self.lf_OSA, input_VBW, *VBW_option_list)
        opt_VBW.grid(row=0, column=4, sticky="nesw")
        text_VBW_unit = tk.Label(self.lf_OSA, text="Hz")
        text_VBW_unit.grid(row=0, column=5, sticky="w")

        # Resolution ([4,5],[0,1]) -> (1,[0,1,2])
        Resolution_option_list = [1,0.5,0.2,0.1,0.07]
        text_Resolution = tk.Label(self.lf_OSA, text="Résolution :")
        text_Resolution.grid(row=1, column=0, sticky="e")
        input_Resolution = tk.StringVar(self.lf_OSA)
        input_Resolution.set(Resolution_option_list[-1])
        self.command.append(input_Resolution)
        opt_Resolution = tk.OptionMenu(
            self.lf_OSA, input_Resolution, *Resolution_option_list
        )
        opt_Resolution.grid(row=1, column=1, sticky="nesw")
        text_Resolution_unit = tk.Label(self.lf_OSA, text="nm")
        text_Resolution_unit.grid(row=1, column=2, sticky="w")

        # Sampling Points ([4,5],[0,1]) -> (1,[3,4,5])
        Smppnt_option_list = [51,101,251,501,1001,2001,5001]
        text_Smppnt = tk.Label(self.lf_OSA, text="Nombre de points :")
        text_Smppnt.grid(row=1, column=3, sticky="e")
        input_Smppnt = tk.StringVar(self.lf_OSA)
        input_Smppnt.set(Smppnt_option_list[-2])
        self.command.append(input_Smppnt)
        opt_Smppnt = tk.OptionMenu(self.lf_OSA, input_Smppnt, *Smppnt_option_list)
        opt_Smppnt.grid(row=1, column=4, sticky="nesw")
        
        # General (0,1)
        self.lf_general = tk.LabelFrame(self, text="Général")
        self.lf_general.grid(row=0, column=1, sticky="nesw")

        # Wavelength (0,1) -> (1,[0,1,2])
        text_Wavelength = tk.Label(self.lf_general, text="Longueur d'onde :")
        text_Wavelength.grid(row=1, column=0, sticky="e")
        input_Wavelength = tk.Entry(self.lf_general, textvariable="")
        self.command.append(input_Wavelength)
        input_Wavelength.grid(row=1, column=1, sticky="nesw")
        text_Wavelength_unit = tk.Label(self.lf_general, text="nm")
        text_Wavelength_unit.grid(row=1, column=2, sticky="w")

        # Name (0,1) -> (0,[0,1,2])
        text_name = tk.Label(self.lf_general, text="Nom du fichier :")
        text_name.grid(row=0, column=0, sticky="e")
        input_name = tk.Entry(self.lf_general, textvariable="")
        self.command.append(input_name)
        input_name.grid(row=0, column=1, sticky="nesw")

        # Start (0,0) -> (1,0)
        self.button_start = tk.Button(
            self.lf_state_display,
            text="START",
            command=partial(self.UpdateState, self.command),
        )
        self.button_start.grid(row=0, column=0, sticky="nesw")

        # Exit (10,10)
        self.button_exit = tk.Button(self, text="EXIT", command=self.destroy)
        self.button_exit.grid(row=10, column=10, sticky="nesw")

    def Stop(self):
        self.button_start.config(
            text="START", command=partial(self.UpdateState, self.command)
        )
        self.destroy
        LIV.Stop()
        WAVELENGTH_SPECTRUM.Stop()

    def UpdateState(self, stringvars):
        conditions = []
        flag = 0
        for element in stringvars:
            if element.get() != "":
                conditions.append(element.get())
        if len(conditions) != len(stringvars):
            del conditions
            self.text_error.config(text="Merci de remplir toutes les cases")
            flag = 0
        else:
            self.button_start.config(text="EN COURS", command=self.destroy)
            self.text_error.config(text="")
            flag = 1
        if flag == 1:
            Write(b'a\r\n') # Bolometer in
            LIV.Data(
                str(conditions[13]),
                int(conditions[1]),
                int(conditions[2]),
                int(conditions[3]),
                float(conditions[0]),
                str(conditions[12]),
            )
            Write(b'b\r\n') # Bolometer out
            time.sleep(10)
            Write(b'y\r\n') # Sphere in
            WAVELENGTH_SPECTRUM.Data(
                str(conditions[13]),
                int(conditions[4]),
                int(conditions[5]),
                int(conditions[6]),
                float(conditions[7]),
                float(conditions[12]),
                float(conditions[8]),
                float(conditions[9]),
                float(conditions[10]),
                int(conditions[11]),
            )
            Write(b'z\r\n') # Sphere out
            self.button_start.config(text="FIN", command=self.destroy)
            self.text_error.config(text="")


class BurnInStart:
    def Start(I, T, t):
        BURN_IN.End(I, T, t)


class BurnInStop:
    def Stop(self):
        self.button_start.config(
            text="START", command=partial(self.UpdateState, self.command)
        )
        self.destroy
        BURN_IN.Stop()


class BurnIn(tk.Toplevel):

    command = []

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Vieillissement")

        # State display
        self.lf_state_display = tk.LabelFrame(self, text="Etat")
        self.lf_state_display.grid(row=0, column=0, sticky="nesw")

        # Error
        self.text_error = tk.Label(self.lf_state_display, text="")
        self.text_error.grid(row=0, column=1, sticky="nesw")

        # Burn-in conditions

        # Conditions
        self.lf_Conditions = tk.LabelFrame(self, text="Conditions")
        self.lf_Conditions.grid(row=0, column=1, sticky="nesw")

        # T
        text_temperature = tk.Label(self.lf_Conditions, text="Température :")
        text_temperature.grid(row=0, column=0, sticky="e")
        input_temperature = tk.Entry(self.lf_Conditions, textvariable="")
        self.command.append(input_temperature)
        input_temperature.grid(row=0, column=1, sticky="nesw")
        text_temperature_unit = tk.Label(self.lf_Conditions, text="°C")
        text_temperature_unit.grid(row=0, column=2, sticky="w")

        # I
        text_I = tk.Label(self.lf_Conditions, text="I :")
        text_I.grid(row=1, column=0, sticky="e")
        input_I = tk.Entry(self.lf_Conditions, textvariable="")
        self.command.append(input_I)
        input_I.grid(row=1, column=1, sticky="nesw")
        text_I_unit = tk.Label(self.lf_Conditions, text="mA")
        text_I_unit.grid(row=1, column=2, sticky="w")

        # t
        text_time = tk.Label(self.lf_Conditions, text="Temps :")
        text_time.grid(row=2, column=0, sticky="e")
        input_time = tk.Entry(self.lf_Conditions, textvariable="")
        self.command.append(input_time)
        input_time.grid(row=2, column=1, sticky="nesw")
        text_time_unit = tk.Label(self.lf_Conditions, text="s")
        text_time_unit.grid(row=2, column=2, sticky="w")

        # Start
        self.button_start = tk.Button(
            self.lf_state_display,
            text="START",
            command=partial(self.UpdateState, self.command),
        )
        self.button_start.grid(row=0, column=0, sticky="nesw")

        # Exit
        self.button_exit = tk.Button(self, text="EXIT", command=self.destroy)
        self.button_exit.grid(row=10, column=10, sticky="nesw")

    def UpdateState(self, stringvars):
        conditions = []
        flag = 0
        for element in stringvars:
            if element.get() != "":
                conditions.append(float(element.get()))
        if len(conditions) != len(stringvars):
            del conditions
            self.text_error.config(text="Merci de remplir toutes les cases")
            flag = 0
        else:
            self.button_start.config(text="EN COURS", command=self.destroy)
            self.text_error.config(text="")
            flag = 1
        if flag == 1:
            BurnInStart.Start(conditions[1], conditions[0], conditions[2])
            self.button_start.config(text="FIN", command=self.destroy)
            self.text_error.config(text="")


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("300x200")
        self.title("Interface Homme-Machine")

        ttk.Button(
            self, text="Caractérisation", command=self.OpenCharacterization
        ).pack(expand=True)
        ttk.Button(
            self, text="Vieillisement", command=self.OpenBurnIn
        ).pack(expand=True)
        ttk.Button(self, text="Fermer", command=self.destroy).pack(expand=True)

    def OpenCharacterization(self):
        window = Characterization(self)
        window.grab_set()

    def OpenBurnIn(self):
        window = BurnIn(self)
        window.grab_set()


app = App()
app.mainloop()

port.close()