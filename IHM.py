import tkinter as tk
from functools import partial
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo

command = []

def UpdateLabel(label, string):
    label.config(text=string)

def UpdateState(stringvars):
    conditions = []
    for element in stringvars:
        if element.get() != '':
            conditions.append(float(element.get()))
    if len(conditions) != len(stringvars):
        del(conditions)
        UpdateLabel(text_error, 'Merci de remplir toutes les cases')
    else:
        UpdateLabel(text_error, '')
        UpdateLabel(text_state, 'ON')
        # print(conditions)

def update_progress_label():
    return f"Progression: {pb['value']}%"

def ProgressLabelProgress():
    if pb['value'] < 100:
        pb['value'] += 20
        value_label['text'] = update_progress_label()
    else:
        showinfo(message='FIN !')

def ProgressLabelStop():
    pb.stop()
    value_label['text'] = update_progress_label()

    # Initialization
window = tk.Tk()
window.title('Interface Homme-Machine')

    # State display
lf_state_display = tk.LabelFrame(window, text='State Display')
lf_state_display.grid(row=0, column=0, sticky='nesw')

        #State
text_state = tk.Label(lf_state_display, text='OFF')
text_state.grid(row=1, column=1, sticky='nesw')

        #Error
text_error = tk.Label(lf_state_display, text='')
text_error.grid(row=0, column=1, sticky='nesw')

    # Measurment conditions

        # Temperature
lf_Temperature = tk.LabelFrame(window, text='Température')
lf_Temperature.grid(row=1, column=1, sticky='nesw')

            # T
text_temperature = tk.Label(lf_Temperature, text='Température :')
text_temperature.grid(row=0, column=0, sticky='e')
input_temperature = tk.Entry(lf_Temperature, textvariable='')
command.append(input_temperature)
input_temperature.grid(row=0, column=1, sticky='nesw')
text_temperature_unit = tk.Label(lf_Temperature, text='°C')
text_temperature_unit.grid(row=0, column=2, sticky='w')

        # Intensity
lf_Intensity = tk.LabelFrame(window, text='Intensité')
lf_Intensity.grid(row=1, column=0, sticky='nesw')

            # I_start
text_I_start = tk.Label(lf_Intensity, text='I_début :')
text_I_start.grid(row=0, column=0, sticky='e')
input_I_start = tk.Entry(lf_Intensity, textvariable='')
command.append(input_I_start)
input_I_start.grid(row=0, column=1, sticky='nesw')
text_I_start_unit = tk.Label(lf_Intensity, text='mA')
text_I_start_unit.grid(row=0, column=2, sticky='w')

            # I_end
text_I_end = tk.Label(lf_Intensity, text='I_fin :')
text_I_end.grid(row=1, column=0, sticky='e')
input_I_end = tk.Entry(lf_Intensity, textvariable='')
command.append(input_I_end)
input_I_end.grid(row=1, column=1, sticky='nesw')
text_I_end_unit = tk.Label(lf_Intensity, text='mA')
text_I_end_unit.grid(row=1, column=2, sticky='w')

            # step
text_step = tk.Label(lf_Intensity, text='pas :')
text_step.grid(row=2, column=0, sticky='e')
input_step = tk.Entry(lf_Intensity, textvariable='')
command.append(input_step)
input_step.grid(row=2, column=1, sticky='nesw')
text_step_unit = tk.Label(lf_Intensity, text='mA')
text_step_unit.grid(row=2, column=2, sticky='w')

        # OSA
lf_OSA = tk.LabelFrame(window, text='OSA')
lf_OSA.grid(row=2, rowspan=1, columnspan=2, sticky='nesw')

            # Span
text_span = tk.Label(lf_OSA, text='Plage de mesure :')
text_span.grid(row=0, column=0, sticky='e')
input_span = tk.Entry(lf_OSA, textvariable='')
command.append(input_span)
input_span.grid(row=0, column=1, sticky='nesw')
text_span_unit = tk.Label(lf_OSA, text='nm\t')
text_span_unit.grid(row=0, column=2, sticky='w')

            # VBW
VBW_option_list = [10, 100, 1000]
text_VBW = tk.Label(lf_OSA, text='Fréquence d\'échantillonnage :')
text_VBW.grid(row=0, column=3, sticky='e')
input_VBW = tk.StringVar(lf_OSA)
input_VBW.set(VBW_option_list[0])
command.append(input_VBW)
opt_VBW = tk.OptionMenu(lf_OSA, input_VBW, *VBW_option_list)
opt_VBW.grid(row=0, column=4, sticky='nesw')
text_VBW_unit = tk.Label(lf_OSA, text='Hz')
text_VBW_unit.grid(row=0, column=5, sticky='w')

            # Resolution
Resolution_option_list = [1, 0.07]
text_Resolution = tk.Label(lf_OSA, text='résolution :')
text_Resolution.grid(row=1, column=0, sticky='e')
input_Resolution = tk.StringVar(lf_OSA)
input_Resolution.set(Resolution_option_list[0])
command.append(input_Resolution)
opt_Resolution = tk.OptionMenu(lf_OSA, input_Resolution, *Resolution_option_list)
opt_Resolution.grid(row=1, column=1, sticky='nesw')
text_Resolution_unit = tk.Label(lf_OSA, text='nm')
text_Resolution_unit.grid(row=1, column=2, sticky='w')

            # Sampling Points
text_Smppnt = tk.Label(lf_OSA, text='Nombre de points :')
text_Smppnt.grid(row=1, column=3, sticky='e')
input_Smppnt = tk.Entry(lf_OSA, textvariable='')
command.append(input_Smppnt)
input_Smppnt.grid(row=1, column=4, sticky='nesw')

        # General
lf_general = tk.LabelFrame(window, text='Général')
lf_general.grid(row=0, column=1, sticky='nesw')

            # Wavelength
text_Wavelength = tk.Label(lf_general, text='Longueur d\'onde :')
text_Wavelength.grid(row=1, column=0, sticky='e')
input_Wavelength = tk.Entry(lf_general, textvariable='')
command.append(input_Wavelength)
input_Wavelength.grid(row=1, column=1, sticky='nesw')
text_Wavelength_unit = tk.Label(lf_general, text='nm')
text_Wavelength_unit.grid(row=1, column=2, sticky='w')

            # Name
text_name = tk.Label(lf_general, text='Nom du fichier :')
text_name.grid(row=0, column=0, sticky='e')
input_name = tk.Entry(lf_general, textvariable='')
command.append(input_name)
input_name.grid(row=0, column=1, sticky='nesw')

    # Start
button_start = tk.Button(lf_state_display, text='START', command=partial(UpdateState, command))
button_start.grid(row=1, column=0, sticky='nesw')

    # Progressbar
pb = ttk.Progressbar(window, orient='horizontal', mode='determinate', length=280)
pb.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

value_label = ttk.Label(window, text=update_progress_label())
value_label.grid(row=4, column=0, columnspan=2)

# start button
start_button = ttk.Button(window, text='Progress', command=ProgressLabelProgress)
start_button.grid(row=2, column=0, padx=10, pady=10, sticky='e')

stop_button = ttk.Button(window, text='Stop', command=ProgressLabelStop)
stop_button.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Exit
button_exit = tk.Button(window, text='EXIT', command=window.destroy)
button_exit.grid(row=10, column=10, sticky='nesw')

    # Launch
window.mainloop()

#https://www.tutorialspoint.com/python/tk_menu.htm