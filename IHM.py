import BURN_IN
import LIV
import WAVELENGTH_SPECTRUM

import tkinter as tk
from functools import partial
from tkinter import ttk

class Characterization(tk.Toplevel):
    
    command = []
    
    def __init__(self, parent):
        super().__init__(parent)

        self.title('Caractérisation')
        
        # State display
        self.lf_state_display = tk.LabelFrame(self, text='State Display')
        self.lf_state_display.grid(row=0, column=0, sticky='nesw')

            #State
        self.text_state = tk.Label(self.lf_state_display, text='OFF')
        self.text_state.grid(row=1, column=1, sticky='nesw')

            #Error
        self.text_error = tk.Label(self.lf_state_display, text='')
        self.text_error.grid(row=0, column=1, sticky='nesw')

        # Measurment conditions

            # Temperature
        self.lf_Temperature = tk.LabelFrame(self, text='Température')
        self.lf_Temperature.grid(row=1, column=1, sticky='nesw')

                # T
        text_temperature = tk.Label(self.lf_Temperature, text='Température :')
        text_temperature.grid(row=0, column=0, sticky='e')
        input_temperature = tk.Entry(self.lf_Temperature, textvariable='')
        self.command.append(input_temperature)
        input_temperature.grid(row=0, column=1, sticky='nesw')
        text_temperature_unit = tk.Label(self.lf_Temperature, text='°C')
        text_temperature_unit.grid(row=0, column=2, sticky='w')

            # Intensity
        self.lf_Intensity = tk.LabelFrame(self, text='Intensité')
        self.lf_Intensity.grid(row=1, column=0, sticky='nesw')

                # I_start
        text_I_start = tk.Label(self.lf_Intensity, text='I_début :')
        text_I_start.grid(row=0, column=0, sticky='e')
        input_I_start = tk.Entry(self.lf_Intensity, textvariable='')
        self.command.append(input_I_start)
        input_I_start.grid(row=0, column=1, sticky='nesw')
        text_I_start_unit = tk.Label(self.lf_Intensity, text='mA')
        text_I_start_unit.grid(row=0, column=2, sticky='w')

                # I_end
        text_I_end = tk.Label(self.lf_Intensity, text='I_fin :')
        text_I_end.grid(row=1, column=0, sticky='e')
        input_I_end = tk.Entry(self.lf_Intensity, textvariable='')
        self.command.append(input_I_end)
        input_I_end.grid(row=1, column=1, sticky='nesw')
        text_I_end_unit = tk.Label(self.lf_Intensity, text='mA')
        text_I_end_unit.grid(row=1, column=2, sticky='w')

                # Step
        text_step = tk.Label(self.lf_Intensity, text='pas :')
        text_step.grid(row=2, column=0, sticky='e')
        input_step = tk.Entry(self.lf_Intensity, textvariable='')
        self.command.append(input_step)
        input_step.grid(row=2, column=1, sticky='nesw')
        text_step_unit = tk.Label(self.lf_Intensity, text='mA')
        text_step_unit.grid(row=2, column=2, sticky='w')

        # OSA
        self.lf_OSA = tk.LabelFrame(self, text='OSA')
        self.lf_OSA.grid(row=2, rowspan=1, columnspan=2, sticky='nesw')

            # Span
        text_span = tk.Label(self.lf_OSA, text='Plage de mesure :')
        text_span.grid(row=0, column=0, sticky='e')
        input_span = tk.Entry(self.lf_OSA, textvariable='')
        self.command.append(input_span)
        input_span.grid(row=0, column=1, sticky='nesw')
        text_span_unit = tk.Label(self.lf_OSA, text='nm\t')
        text_span_unit.grid(row=0, column=2, sticky='w')

            # VBW
        VBW_option_list = [10, 100, 1000]
        text_VBW = tk.Label(self.lf_OSA, text='Fréquence d\'échantillonnage :')
        text_VBW.grid(row=0, column=3, sticky='e')
        input_VBW = tk.StringVar(self.lf_OSA)
        input_VBW.set(VBW_option_list[0])
        self.command.append(input_VBW)
        opt_VBW = tk.OptionMenu(self.lf_OSA, input_VBW, *VBW_option_list)
        opt_VBW.grid(row=0, column=4, sticky='nesw')
        text_VBW_unit = tk.Label(self.lf_OSA, text='Hz')
        text_VBW_unit.grid(row=0, column=5, sticky='w')

            # Resolution
        Resolution_option_list = [1, 0.07]
        text_Resolution = tk.Label(self.lf_OSA, text='résolution :')
        text_Resolution.grid(row=1, column=0, sticky='e')
        input_Resolution = tk.StringVar(self.lf_OSA)
        input_Resolution.set(Resolution_option_list[0])
        self.command.append(input_Resolution)
        opt_Resolution = tk.OptionMenu(self.lf_OSA, input_Resolution, *Resolution_option_list)
        opt_Resolution.grid(row=1, column=1, sticky='nesw')
        text_Resolution_unit = tk.Label(self.lf_OSA, text='nm')
        text_Resolution_unit.grid(row=1, column=2, sticky='w')

            # Sampling Points
        text_Smppnt = tk.Label(self.lf_OSA, text='Nombre de points :')
        text_Smppnt.grid(row=1, column=3, sticky='e')
        input_Smppnt = tk.Entry(self.lf_OSA, textvariable='')
        self.command.append(input_Smppnt)
        input_Smppnt.grid(row=1, column=4, sticky='nesw')

        # General
        self.lf_general = tk.LabelFrame(self, text='Général')
        self.lf_general.grid(row=0, column=1, sticky='nesw')

            # Wavelength
        text_Wavelength = tk.Label(self.lf_general, text='Longueur d\'onde :')
        text_Wavelength.grid(row=1, column=0, sticky='e')
        input_Wavelength = tk.Entry(self.lf_general, textvariable='')
        self.command.append(input_Wavelength)
        input_Wavelength.grid(row=1, column=1, sticky='nesw')
        text_Wavelength_unit = tk.Label(self.lf_general, text='nm')
        text_Wavelength_unit.grid(row=1, column=2, sticky='w')

            # Name
        text_name = tk.Label(self.lf_general, text='Nom du fichier :')
        text_name.grid(row=0, column=0, sticky='e')
        input_name = tk.Entry(self.lf_general, textvariable='')
        self.command.append(input_name)
        input_name.grid(row=0, column=1, sticky='nesw')

        # Start
        self.button_start = tk.Button(self.lf_state_display, text='START', command=partial(self.UpdateState, self.command))
        self.button_start.grid(row=1, column=0, sticky='nesw')

        # Exit
        self.button_exit = tk.Button(self, text='EXIT', command=self.destroy)
        self.button_exit.grid(row=10, column=10, sticky='nesw')

    def Stop(self):
        LIV.Stop()
        WAVELENGTH_SPECTRUM.Stop()
        self.button_start.config(text='START', command=partial(self.UpdateState, self.command))
        self.text_state.config(text='OFF')
        
    def UpdateState(self, stringvars):
        conditions = []
        for element in stringvars:
            if element.get() != '':
                conditions.append(float(element.get()))
        if len(conditions) != len(stringvars):
            del(conditions)
            self.text_error.config(text='Merci de remplir toutes les cases')
        else:
            self.button_start.config(text='STOP', command=partial(self.Stop))
            self.text_error.config(text='')
            self.text_state.config(text='ON')
            LIV.Data(conditions[9], conditions[1], conditions[2], conditions[3], conditions[0], conditions[8])
            WAVELENGTH_SPECTRUM.Data(conditions[9], conditions[1], conditions[2], conditions[3], conditions[0], conditions[8], conditions[4], conditions[5], conditions[6], conditions[7])

class BurnIn(tk.Toplevel):
    
    command = []
    
    def __init__(self, parent):
        super().__init__(parent)

        self.title('Vieillissement')
        
        # State display
        self.lf_state_display = tk.LabelFrame(self, text='State Display')
        self.lf_state_display.grid(row=0, column=0, sticky='nesw')

            #State
        self.text_state = tk.Label(self.lf_state_display, text='OFF')
        self.text_state.grid(row=1, column=1, sticky='nesw')

            #Error
        self.text_error = tk.Label(self.lf_state_display, text='')
        self.text_error.grid(row=0, column=1, sticky='nesw')

        # Burn-in conditions

            # Conditions
        self.lf_Conditions = tk.LabelFrame(self, text='Conditions')
        self.lf_Conditions.grid(row=0, column=1, sticky='nesw')

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
        
                # t
        text_time = tk.Label(self.lf_Conditions, text='Temps :')
        text_time.grid(row=2, column=0, sticky='e')
        input_time = tk.Entry(self.lf_Conditions, textvariable='')
        self.command.append(input_time)
        input_time.grid(row=2, column=1, sticky='nesw')
        text_time_unit = tk.Label(self.lf_Conditions, text='s')
        text_time_unit.grid(row=2, column=2, sticky='w')

        # Start
        self.button_start = tk.Button(self.lf_state_display, text='START', command=partial(self.UpdateState, self.command))
        self.button_start.grid(row=1, column=0, sticky='nesw')

        # Exit
        self.button_exit = tk.Button(self, text='EXIT', command=self.destroy)
        self.button_exit.grid(row=10, column=10, sticky='nesw')

    def Stop(self):
        BURN_IN.Stop()
        self.button_start.config(text='START', command=partial(self.UpdateState, self.command))
        self.text_state.config(text='OFF')

    def UpdateState(self, stringvars):
        conditions = []
        for element in stringvars:
            if element.get() != '':
                conditions.append(float(element.get()))
        if len(conditions) != len(stringvars):
            del(conditions)
            self.text_error.config(text='Merci de remplir toutes les cases')
        else:
            self.button_start.config(text='STOP', command=partial(self.Stop))
            self.text_error.config(text='')
            self.text_state.config(text='ON')
            print(conditions)
            BURN_IN.End(conditions[1], conditions[0], conditions[2])

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('300x200')
        self.title('Interface Homme-Machine')

        ttk.Button(self, text='Caractérisation', command=self.OpenCharacterization).pack(expand=True)
        ttk.Button(self, text='Vieillissement', command=self.OpenBurnIn).pack(expand=True)
        ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)

    def OpenCharacterization(self):
        window = Characterization(self)
        window.grab_set()
        
    def OpenBurnIn(self):
        window = BurnIn(self)
        window.grab_set()

app = App()
app.mainloop()