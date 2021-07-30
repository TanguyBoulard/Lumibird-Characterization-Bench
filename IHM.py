import tkinter as tk
from functools import partial

command = []
conditions = []

def UpdateLabel(label, string):
    label.config(text=string)

def UpdateState(command, conditions, stringvars):
    for element in stringvars:
        if element.get() == '':
            UpdateLabel(text_error, 'Merci de remplir toutes les cases')
        else:
            UpdateLabel(text_error, '')
            UpdateLabel(text_state, 'ON')
            conditions.append(float(element.get()))


    # Initialization
window = tk.Tk()

    # Introduction text
lf_introduction = tk.LabelFrame(window, text='')
lf_introduction.grid(row=0, column=0)

text_IHM = tk.Label(window, text='Interface Homme-Machine', foreground='white', background='black')
text_IHM.grid(row=0, column=0)

    # State display
lf_state_display = tk.LabelFrame(window, text='State Display')
lf_state_display.grid(row=1, column=0)

        #State
text_state = tk.Label(lf_state_display, text='OFF')
text_state.grid(row=1, column=1)

        #Error
text_error = tk.Label(lf_state_display, text='')
text_error.grid(row=0, column=1)

    # Measurment conditions

        # Temperature
lf_Temperature = tk.LabelFrame(window, text='Température')
lf_Temperature.grid(row=2, column=0)

            #Temperature
text_temperature = tk.Label(lf_Temperature, text='Température :')
text_temperature.grid(row=0, column=0, sticky='e')
input_temperature = tk.Entry(lf_Temperature, textvariable='')
command.append(input_temperature)
input_temperature.grid(row=0, column=1)
text_temperature_unit = tk.Label(lf_Temperature, text='°C')
text_temperature_unit.grid(row=0, column=2, sticky='w')

        # Intensity
lf_Intensity = tk.LabelFrame(window, text='Intensité')
lf_Intensity.grid(row=3, column=0)

            #I_start
text_I_start = tk.Label(lf_Intensity, text='I_début :')
text_I_start.grid(row=0, column=0, sticky='e')
input_I_start = tk.Entry(lf_Intensity, textvariable='')
command.append(input_I_start)
input_I_start.grid(row=0, column=1)
text_I_start_unit = tk.Label(lf_Intensity, text='mA')
text_I_start_unit.grid(row=0, column=2, sticky='w')

            #I_end
text_I_end = tk.Label(lf_Intensity, text='I_fin :')
text_I_end.grid(row=1, column=0, sticky='e')
input_I_end = tk.Entry(lf_Intensity, textvariable='')
command.append(input_I_end)
input_I_end.grid(row=1, column=1)
text_I_end_unit = tk.Label(lf_Intensity, text='mA')
text_I_end_unit.grid(row=1, column=2, sticky='w')

            #step
text_step = tk.Label(lf_Intensity, text='pas :')
text_step.grid(row=2, column=0, sticky='e')
input_step = tk.Entry(lf_Intensity, textvariable='')
command.append(input_step)
input_step.grid(row=2, column=1)
text_step_unit = tk.Label(lf_Intensity, text='mA')
text_step_unit.grid(row=2, column=2, sticky='w')

    # Start
button_start = tk.Button(lf_state_display, text='START', command=partial(UpdateState, command, conditions, command))
button_start.grid(row=1, column=0)

    # Exit
button_exit = tk.Button(window, text='EXIT', command=window.destroy)
button_exit.grid(row=10, column=10)

    # Launch
window.mainloop()

print(conditions)