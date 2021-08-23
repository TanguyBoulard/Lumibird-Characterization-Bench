# =============================================================================
# CREDITS
# =============================================================================
# Author : Tanguy BOULARD
# Date   : 28/06/2021
# Script : Graphical user interface

# =============================================================================
# MODULES
# =============================================================================

import ARDUINO
import BURN_IN
import LIV
import WAVELENGTH_SPECTRUM

import tkinter as tk
from functools import partial
from tkinter import ttk

import time

# =============================================================================
# PARAMETERS
# =============================================================================

ended = False

port = ARDUINO.OpenPort()  

# =============================================================================
# CLASS
# =============================================================================

class Characterization(tk.Toplevel):

    command = []

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Caractérisation")

        # State display
        self.lf_state_display = tk.LabelFrame(self, text="Etat")
        self.lf_state_display.grid(row=0, column=0, sticky="nesw")

        # Error
        self.text_error = tk.Label(self.lf_state_display, text="")
        self.text_error.grid(row=0, column=1, sticky="nesw")

        # Separator
        separator = tk.Label(self, text="P(I)")
        separator.grid(row=1, columnspan=10, sticky="ew")

        # Measurment conditions

            # Temperature
        self.lf_Temperature = tk.LabelFrame(self, text="Température")
        self.lf_Temperature.grid(row=2, column=1, sticky="nesw")

                # T
        text_temperature = tk.Label(self.lf_Temperature, text="Température :")
        text_temperature.grid(row=0, column=0, sticky="e")
        input_temperature = tk.Entry(self.lf_Temperature, textvariable="")
        self.command.append(input_temperature)
        input_temperature.grid(row=0, column=1, sticky="nesw")
        text_temperature_unit = tk.Label(self.lf_Temperature, text="°C")
        text_temperature_unit.grid(row=0, column=2, sticky="w")

        # Intensity
        self.lf_Intensity = tk.LabelFrame(self, text="Intensité")
        self.lf_Intensity.grid(row=2, column=0, sticky="nesw")

            # I_start
        text_I_start = tk.Label(self.lf_Intensity, text="I_début :")
        text_I_start.grid(row=0, column=0, sticky="e")
        input_I_start = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_I_start)
        input_I_start.grid(row=0, column=1, sticky="nesw")
        text_I_start_unit = tk.Label(self.lf_Intensity, text="mA")
        text_I_start_unit.grid(row=0, column=2, sticky="w")

            # I_end
        text_I_end = tk.Label(self.lf_Intensity, text="I_fin :")
        text_I_end.grid(row=1, column=0, sticky="e")
        input_I_end = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_I_end)
        input_I_end.grid(row=1, column=1, sticky="nesw")
        text_I_end_unit = tk.Label(self.lf_Intensity, text="mA")
        text_I_end_unit.grid(row=1, column=2, sticky="w")

            # Step
        text_step = tk.Label(self.lf_Intensity, text="pas :")
        text_step.grid(row=2, column=0, sticky="e")
        input_step = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_step)
        input_step.grid(row=2, column=1, sticky="nesw")
        text_step_unit = tk.Label(self.lf_Intensity, text="mA")
        text_step_unit.grid(row=2, column=2, sticky="w")

        # Separator
        separator = tk.Label(self, text="Spectre en longueur d'onde")
        separator.grid(row=3, columnspan=10, sticky="ew")

        # OSA
        self.lf_OSA = tk.LabelFrame(self, text="OSA")
        self.lf_OSA.grid(row=5, rowspan=1, columnspan=2, sticky="nesw")

            # Span
        text_span = tk.Label(self.lf_OSA, text="Plage de mesure :")
        text_span.grid(row=0, column=0, sticky="e")
        input_span = tk.Entry(self.lf_OSA, textvariable="")
        self.command.append(input_span)
        input_span.grid(row=0, column=1, sticky="nesw")
        text_span_unit = tk.Label(self.lf_OSA, text="nm\t")
        text_span_unit.grid(row=0, column=2, sticky="w")

            # VBW
        VBW_option_list = [int(1E1), int(1E2), int(1E3), int(1E4), int(1E5), int(1E6)]
        text_VBW = tk.Label(self.lf_OSA, text="Fréquence d'échantillonnage :")
        text_VBW.grid(row=0, column=3, sticky="e")
        input_VBW = tk.StringVar(self.lf_OSA)
        input_VBW.set(VBW_option_list[2])
        self.command.append(input_VBW)
        opt_VBW = tk.OptionMenu(self.lf_OSA, input_VBW, *VBW_option_list)
        opt_VBW.grid(row=0, column=4, sticky="nesw")
        text_VBW_unit = tk.Label(self.lf_OSA, text="Hz")
        text_VBW_unit.grid(row=0, column=5, sticky="w")

            # Resolution
        Resolution_option_list = [1,0.5,0.2,0.1,0.07]
        text_Resolution = tk.Label(self.lf_OSA, text="Résolution :")
        text_Resolution.grid(row=1, column=0, sticky="e")
        input_Resolution = tk.StringVar(self.lf_OSA)
        input_Resolution.set(Resolution_option_list[-1])
        self.command.append(input_Resolution)
        opt_Resolution = tk.OptionMenu(self.lf_OSA, input_Resolution, *Resolution_option_list)
        opt_Resolution.grid(row=1, column=1, sticky="nesw")
        text_Resolution_unit = tk.Label(self.lf_OSA, text="nm")
        text_Resolution_unit.grid(row=1, column=2, sticky="w")

            # Sampling Points
        Smppnt_option_list = [51,101,251,501,1001,2001,5001]
        text_Smppnt = tk.Label(self.lf_OSA, text="Nombre de points :")
        text_Smppnt.grid(row=1, column=3, sticky="e")
        input_Smppnt = tk.StringVar(self.lf_OSA)
        input_Smppnt.set(Smppnt_option_list[-2])
        self.command.append(input_Smppnt)
        opt_Smppnt = tk.OptionMenu(self.lf_OSA, input_Smppnt, *Smppnt_option_list)
        opt_Smppnt.grid(row=1, column=4, sticky="nesw")
        
        # Intensity OSA
        self.lf_IntensityOSA = tk.LabelFrame(self, text="Intensité")
        self.lf_IntensityOSA.grid(row=4, column=0, sticky="nesw")

            # I_start
        text_I_startOSA = tk.Label(self.lf_IntensityOSA, text="I_début :")
        text_I_startOSA.grid(row=0, column=0, sticky="e")
        input_I_startOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_I_startOSA)
        input_I_startOSA.grid(row=0, column=1, sticky="nesw")
        text_I_startOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_I_startOSA_unit.grid(row=0, column=2, sticky="w")

            # I_end
        text_I_endOSA = tk.Label(self.lf_IntensityOSA, text="I_fin :")
        text_I_endOSA.grid(row=1, column=0, sticky="e")
        input_I_endOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_I_endOSA)
        input_I_endOSA.grid(row=1, column=1, sticky="nesw")
        text_I_endOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_I_endOSA_unit.grid(row=1, column=2, sticky="w")

            # Step
        text_stepOSA = tk.Label(self.lf_IntensityOSA, text="pas :")
        text_stepOSA.grid(row=2, column=0, sticky="e")
        input_stepOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_stepOSA)
        input_stepOSA.grid(row=2, column=1, sticky="nesw")
        text_stepOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_stepOSA_unit.grid(row=2, column=2, sticky="w")

        # Temperature OSA
        self.lf_TemperatureOSA = tk.LabelFrame(self, text="Température")
        self.lf_TemperatureOSA.grid(row=4, column=1, sticky="nesw")

            # T OSA
        text_temperatureOSA = tk.Label(self.lf_TemperatureOSA, text="Température :")
        text_temperatureOSA.grid(row=0, column=0, sticky="e")
        input_temperatureOSA = tk.Entry(self.lf_TemperatureOSA, textvariable="")
        self.command.append(input_temperatureOSA)
        input_temperatureOSA.grid(row=0, column=1, sticky="nesw")
        text_temperatureOSA_unit = tk.Label(self.lf_TemperatureOSA, text="°C")
        text_temperatureOSA_unit.grid(row=0, column=2, sticky="w")
        
        # General
        self.lf_general = tk.LabelFrame(self, text="Général")
        self.lf_general.grid(row=0, column=1, sticky="nesw")

            # Wavelength
        text_Wavelength = tk.Label(self.lf_general, text="Longueur d'onde :")
        text_Wavelength.grid(row=1, column=0, sticky="e")
        input_Wavelength = tk.Entry(self.lf_general, textvariable="")
        self.command.append(input_Wavelength)
        input_Wavelength.grid(row=1, column=1, sticky="nesw")
        text_Wavelength_unit = tk.Label(self.lf_general, text="nm")
        text_Wavelength_unit.grid(row=1, column=2, sticky="w")

            # Name
        text_name = tk.Label(self.lf_general, text="Nom du fichier :")
        text_name.grid(row=0, column=0, sticky="e")
        input_name = tk.Entry(self.lf_general, textvariable="")
        self.command.append(input_name)
        input_name.grid(row=0, column=1, sticky="nesw")

        # Start
        self.button_start = tk.Button(self.lf_state_display, text="START", command=partial(self.UpdateState, self.command))
        self.button_start.grid(row=0, column=0, sticky="nesw")

        # Exit
        self.button_exit = tk.Button(self, text="EXIT", command=self.destroy)
        self.button_exit.grid(row=10, column=10, sticky="nesw")

    def Stop(self):
        self.button_start.config(text="START", command=partial(self.UpdateState, self.command))
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
            self.button_start.config(text="CRASH", command=self.destroy)
            self.text_error.config(text="")
            flag = 1
        if flag == 1:
            ARDUINO.Write(port, b'a\r\n') # Bolometer in
            time.sleep(5)
            # name, I_start, I_end, I_pas, T, wavelength
            LIV.Data(str(conditions[13]), int(conditions[1]), int(conditions[2]), int(conditions[3]), float(conditions[0]), str(conditions[12]))
            time.sleep(5)
            ARDUINO.Write(port, b'b\r\n') # Bolometer out
            time.sleep(5)
            ARDUINO.Write(port, b'z\r\n') # Sphere in
            time.sleep(5)
            # name, I_start, I_end, I_pas, T, wavelength, Span, VBW, res, Smppnt
            WAVELENGTH_SPECTRUM.Data(str(conditions[13]), int(conditions[8]), int(conditions[9]), int(conditions[10]), float(conditions[11]), float(conditions[12]), float(conditions[4]), int(conditions[5]), float(conditions[6]), int(conditions[7]))
            time.sleep(5)
            ARDUINO.Write(port, b'y\r\n') # Sphere out
            time.sleep(5)
            ARDUINO.Write(port, b's\r\n')
            self.button_start.config(text="FIN", command=self.destroy)
            self.text_error.config(text="")

class BurnIn(tk.Toplevel):

    command = []

    def __init__(self, parent):
        super().__init__(parent)

        self.title('Vieillissement')

        # State display
        self.lf_state_display = tk.LabelFrame(self, text='Etat')
        self.lf_state_display.grid(row=0, column=0, sticky='nesw')

        # Error
        self.text_error = tk.Label(self.lf_state_display, text='')
        self.text_error.grid(row=0, column=1, sticky='nesw')

        # Separator
        separator = tk.Label(self, text="Burn-in conditions")
        separator.grid(row=1, columnspan=10, sticky="ew")

        # Burn-in conditions

            # Conditions
        self.lf_Conditions = tk.LabelFrame(self, text='Conditions')
        self.lf_Conditions.grid(row=2, column=0, columnspan=2, sticky='nesw')

                # T
        text_temperature = tk.Label(self.lf_Conditions, text='Température :')
        text_temperature.grid(row=0, column=0, sticky='e')
        input_temperature = tk.Entry(self.lf_Conditions, textvariable='')
        self.command.append(input_temperature)
        input_temperature.grid(row=0, column=1, sticky='nesw')
        text_temperature_unit = tk.Label(self.lf_Conditions, text='°C')
        text_temperature_unit.grid(row=0, column=2, sticky='w')

                # I
        text_I = tk.Label(self.lf_Conditions, text='I :')
        text_I.grid(row=1, column=0, sticky='e')
        input_I = tk.Entry(self.lf_Conditions, textvariable='')
        self.command.append(input_I)
        input_I.grid(row=1, column=1, sticky='nesw')
        text_I_unit = tk.Label(self.lf_Conditions, text='mA')
        text_I_unit.grid(row=1, column=2, sticky='w')

                # hours
        text_time = tk.Label(self.lf_Conditions, text='Temps :')
        text_time.grid(row=2, column=0, sticky='e')
        input_time = tk.Entry(self.lf_Conditions, textvariable='')
        self.command.append(input_time)
        input_time.grid(row=2, column=1, sticky='nesw')
        text_time_unit = tk.Label(self.lf_Conditions, text='h')
        text_time_unit.grid(row=2, column=2, sticky='w')
        
                # minutes
        input_time = tk.Entry(self.lf_Conditions, textvariable='')
        self.command.append(input_time)
        input_time.grid(row=2, column=3, sticky='nesw')
        text_time_unit = tk.Label(self.lf_Conditions, text='min')
        text_time_unit.grid(row=2, column=4, sticky='w')
        
                # seconds
        input_time = tk.Entry(self.lf_Conditions, textvariable='')
        self.command.append(input_time)
        input_time.grid(row=2, column=5, sticky='nesw')
        text_time_unit = tk.Label(self.lf_Conditions, text='s')
        text_time_unit.grid(row=2, column=6, sticky='w')
        
        # Separator
        separator = tk.Label(self, text="P(I)")
        separator.grid(row=3, columnspan=10, sticky="ew")

        # Measurment conditions

            # Temperature
        self.lf_Temperature = tk.LabelFrame(self, text="Température")
        self.lf_Temperature.grid(row=4, column=1, sticky="nesw")

                # T
        text_temperature = tk.Label(self.lf_Temperature, text="Température :")
        text_temperature.grid(row=0, column=0, sticky="e")
        input_temperature = tk.Entry(self.lf_Temperature, textvariable="")
        self.command.append(input_temperature)
        input_temperature.grid(row=0, column=1, sticky="nesw")
        text_temperature_unit = tk.Label(self.lf_Temperature, text="°C")
        text_temperature_unit.grid(row=0, column=2, sticky="w")

        # Intensity
        self.lf_Intensity = tk.LabelFrame(self, text="Intensité")
        self.lf_Intensity.grid(row=4, column=0, sticky="nesw")

            # I_start
        text_I_start = tk.Label(self.lf_Intensity, text="I_début :")
        text_I_start.grid(row=0, column=0, sticky="e")
        input_I_start = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_I_start)
        input_I_start.grid(row=0, column=1, sticky="nesw")
        text_I_start_unit = tk.Label(self.lf_Intensity, text="mA")
        text_I_start_unit.grid(row=0, column=2, sticky="w")

            # I_end
        text_I_end = tk.Label(self.lf_Intensity, text="I_fin :")
        text_I_end.grid(row=1, column=0, sticky="e")
        input_I_end = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_I_end)
        input_I_end.grid(row=1, column=1, sticky="nesw")
        text_I_end_unit = tk.Label(self.lf_Intensity, text="mA")
        text_I_end_unit.grid(row=1, column=2, sticky="w")

            # Step
        text_step = tk.Label(self.lf_Intensity, text="pas :")
        text_step.grid(row=2, column=0, sticky="e")
        input_step = tk.Entry(self.lf_Intensity, textvariable="")
        self.command.append(input_step)
        input_step.grid(row=2, column=1, sticky="nesw")
        text_step_unit = tk.Label(self.lf_Intensity, text="mA")
        text_step_unit.grid(row=2, column=2, sticky="w")

        # Separator
        separator = tk.Label(self, text="Spectre en longueur d'onde")
        separator.grid(row=5, columnspan=10, sticky="ew")

        # OSA
        self.lf_OSA = tk.LabelFrame(self, text="OSA")
        self.lf_OSA.grid(row=7, rowspan=1, columnspan=2, sticky="nesw")

            # Span
        text_span = tk.Label(self.lf_OSA, text="Plage de mesure :")
        text_span.grid(row=0, column=0, sticky="e")
        input_span = tk.Entry(self.lf_OSA, textvariable="")
        self.command.append(input_span)
        input_span.grid(row=0, column=1, sticky="nesw")
        text_span_unit = tk.Label(self.lf_OSA, text="nm\t")
        text_span_unit.grid(row=0, column=2, sticky="w")

            # VBW
        VBW_option_list = [int(1E1), int(1E2), int(1E3), int(1E4), int(1E5), int(1E6)]
        text_VBW = tk.Label(self.lf_OSA, text="Fréquence d'échantillonnage :")
        text_VBW.grid(row=0, column=3, sticky="e")
        input_VBW = tk.StringVar(self.lf_OSA)
        input_VBW.set(VBW_option_list[2])
        self.command.append(input_VBW)
        opt_VBW = tk.OptionMenu(self.lf_OSA, input_VBW, *VBW_option_list)
        opt_VBW.grid(row=0, column=4, sticky="nesw")
        text_VBW_unit = tk.Label(self.lf_OSA, text="Hz")
        text_VBW_unit.grid(row=0, column=5, sticky="w")

            # Resolution
        Resolution_option_list = [1,0.5,0.2,0.1,0.07]
        text_Resolution = tk.Label(self.lf_OSA, text="Résolution :")
        text_Resolution.grid(row=1, column=0, sticky="e")
        input_Resolution = tk.StringVar(self.lf_OSA)
        input_Resolution.set(Resolution_option_list[-1])
        self.command.append(input_Resolution)
        opt_Resolution = tk.OptionMenu(self.lf_OSA, input_Resolution, *Resolution_option_list)
        opt_Resolution.grid(row=1, column=1, sticky="nesw")
        text_Resolution_unit = tk.Label(self.lf_OSA, text="nm")
        text_Resolution_unit.grid(row=1, column=2, sticky="w")

            # Sampling Points
        Smppnt_option_list = [51,101,251,501,1001,2001,5001]
        text_Smppnt = tk.Label(self.lf_OSA, text="Nombre de points :")
        text_Smppnt.grid(row=1, column=3, sticky="e")
        input_Smppnt = tk.StringVar(self.lf_OSA)
        input_Smppnt.set(Smppnt_option_list[-2])
        self.command.append(input_Smppnt)
        opt_Smppnt = tk.OptionMenu(self.lf_OSA, input_Smppnt, *Smppnt_option_list)
        opt_Smppnt.grid(row=1, column=4, sticky="nesw")
        
        # Intensity OSA
        self.lf_IntensityOSA = tk.LabelFrame(self, text="Intensité")
        self.lf_IntensityOSA.grid(row=6, column=0, sticky="nesw")

            # I_start
        text_I_startOSA = tk.Label(self.lf_IntensityOSA, text="I_début :")
        text_I_startOSA.grid(row=0, column=0, sticky="e")
        input_I_startOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_I_startOSA)
        input_I_startOSA.grid(row=0, column=1, sticky="nesw")
        text_I_startOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_I_startOSA_unit.grid(row=0, column=2, sticky="w")

            # I_end
        text_I_endOSA = tk.Label(self.lf_IntensityOSA, text="I_fin :")
        text_I_endOSA.grid(row=1, column=0, sticky="e")
        input_I_endOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_I_endOSA)
        input_I_endOSA.grid(row=1, column=1, sticky="nesw")
        text_I_endOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_I_endOSA_unit.grid(row=1, column=2, sticky="w")

            # Step
        text_stepOSA = tk.Label(self.lf_IntensityOSA, text="pas :")
        text_stepOSA.grid(row=2, column=0, sticky="e")
        input_stepOSA = tk.Entry(self.lf_IntensityOSA, textvariable="")
        self.command.append(input_stepOSA)
        input_stepOSA.grid(row=2, column=1, sticky="nesw")
        text_stepOSA_unit = tk.Label(self.lf_IntensityOSA, text="mA")
        text_stepOSA_unit.grid(row=2, column=2, sticky="w")

        # Temperature OSA
        self.lf_TemperatureOSA = tk.LabelFrame(self, text="Température")
        self.lf_TemperatureOSA.grid(row=6, column=1, sticky="nesw")

            # T OSA
        text_temperatureOSA = tk.Label(self.lf_TemperatureOSA, text="Température :")
        text_temperatureOSA.grid(row=0, column=0, sticky="e")
        input_temperatureOSA = tk.Entry(self.lf_TemperatureOSA, textvariable="")
        self.command.append(input_temperatureOSA)
        input_temperatureOSA.grid(row=0, column=1, sticky="nesw")
        text_temperatureOSA_unit = tk.Label(self.lf_TemperatureOSA, text="°C")
        text_temperatureOSA_unit.grid(row=0, column=2, sticky="w")
        
        # General
        self.lf_general = tk.LabelFrame(self, text="Général")
        self.lf_general.grid(row=0, column=1, sticky="nesw")

            # Wavelength
        text_Wavelength = tk.Label(self.lf_general, text="Longueur d'onde :")
        text_Wavelength.grid(row=1, column=0, sticky="e")
        input_Wavelength = tk.Entry(self.lf_general, textvariable="")
        self.command.append(input_Wavelength)
        input_Wavelength.grid(row=1, column=1, sticky="nesw")
        text_Wavelength_unit = tk.Label(self.lf_general, text="nm")
        text_Wavelength_unit.grid(row=1, column=2, sticky="w")

            # Name
        text_name = tk.Label(self.lf_general, text="Nom du fichier :")
        text_name.grid(row=0, column=0, sticky="e")
        input_name = tk.Entry(self.lf_general, textvariable="")
        self.command.append(input_name)
        input_name.grid(row=0, column=1, sticky="nesw")

        # Start
        self.button_start = tk.Button(self.lf_state_display, text='START', command=partial(self.UpdateState, self.command))
        self.button_start.grid(row=0, column=0, sticky='nesw')

        # Exit
        self.button_exit = tk.Button(self, text='EXIT', command=self.destroy)
        self.button_exit.grid(row=10, column=10, sticky='nesw')

    def Stop(self):
        self.button_start.config(text="START", command=partial(self.UpdateState, self.command))
        self.destroy
        BURN_IN.Stop()

    def UpdateState(self, stringvars):
        conditions = []
        flag = 0
        for element in stringvars:
            if element.get() != '':
                conditions.append(element.get())
        if len(conditions) != len(stringvars):
            del conditions
            self.text_error.config(text='Merci de remplir toutes les cases')
            flag = 0
        else:
            self.button_start.config(text='CRASH', command=self.destroy)
            self.text_error.config(text='')
            flag = 1
        if flag == 1:
            ARDUINO.Write(port, b'a\r\n') # Bolometer in
            time.sleep(5)
            # I, T, hours, mins, secs, port, wavelength, name, Span, VBW, res, Smppnt
            BURN_IN.main(int(conditions[1]), float(conditions[0]), int(conditions[2]), int(conditions[3]), int(conditions[4]), port, str(conditions[17]), str(conditions[18]), float(conditions[9]), int(conditions[10]), float(conditions[11]), int(conditions[12]))
            time.sleep(5)
            # name, I_start, I_end, I_pas, T, wavelength
            LIV.Data(str(conditions[18]), int(conditions[6]), int(conditions[7]), int(conditions[8]), float(conditions[5]), str(conditions[17]))
            time.sleep(5)
            ARDUINO.Write(port, b'b\r\n') # Bolometer out
            time.sleep(5)
            ARDUINO.Write(port, b'z\r\n') # Sphere in
            time.sleep(5)
            # name, I_start, I_end, I_pas, T, wavelength, Span, VBW, res, Smppnt
            WAVELENGTH_SPECTRUM.Data(str(conditions[18]), int(conditions[13]), int(conditions[14]), int(conditions[15]), float(conditions[16]), float(conditions[17]), float(conditions[9]), int(conditions[10]), float(conditions[11]), int(conditions[12]))
            time.sleep(5)
            ARDUINO.Write(port, b'y\r\n') # Sphere out
            time.sleep(5)
            ARDUINO.Write(port, b's\r\n')
            self.button_start.config(text="FIN", command=self.destroy)
            self.text_error.config(text='')

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("300x200")
        self.title("Interface Homme-Machine")

        ttk.Button(self, text="Caractérisation", command=self.OpenCharacterization).pack(expand=True)
        ttk.Button(self, text="Vieillisement", command=self.OpenBurnIn).pack(expand=True)
        ttk.Button(self, text="Fermer", command=self.destroy).pack(expand=True)

    def OpenCharacterization(self):
        window = Characterization(self)
        window.grab_set()

    def OpenBurnIn(self):
        # window = TIMER.Timer
        window = BurnIn(self)
        window.grab_set()

app = Main()
app.mainloop()

port.close()