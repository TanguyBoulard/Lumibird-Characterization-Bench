# LUMIBIRD OPHELLIA

  - [Characterization-Bench](#characterization-bench)
  - [HEXAPOD](#hexapod)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Characterization-Bench

## *Lumbird* project from **Tanguy Boulard** as engineer intern to improve the characterization bench in the active clean room.

  - [Equipment](#Equipment)
  - [Installation](#installation)
  - [Credits](#credits)
  - [Roadmap](#roadmap)

## Equipment

1. COS (Chip On Submont) electrical connectivity
	- Four-terminal sensing: in order to measure Intensity injected on the chip plus the output Voltage
	- Communication cable which allow a control from the alimentation to the COS
2. Measuring instrument
	- PRO8000 for COS alimentation plus TEC control
	- KEYSIGHT for output Voltage read
	- GENTEC-EO P-LINK for optical power read
	- OSA for wavelength spectrum analysis
3. Communicationcable which allow connectivity from PC to measuring instrument
	- PC/PRO8000 -> RS232C
	- PC/KEYSIGHT -> USB
	- PC/OSA -> GPIB
	- PC/P-LINK -> USB
	- PC/ARDUINO -> USB
4. ARDUINO alimentation
	- ARDUINO is alimented by PC
	- SHIELD need alimentation (12V, 3A) thanks to adaptator

## Installation

  * Connect all the device to PC.  
  * Carefully place the COS on the bench.  
  * Check if stepper motors are well connected on the shield thanks to the scheme below,  and then verify plugging onto the Arduino.  
  * Execute 'Interface Homme-Machine.exe'.
  * You are then good to go! You can now start characterization. 
  * In addition, datas are saved on a desktop menu.

## Created by

BOULARD Tanguy 

## Roadmap

  - [x] Instrumentation with measuring instrument.
  - [x] Program a first version on Python.
  - [x] Create the interface which displays and saves the datas measured.
  - [ ] Automatization with Arduino.
  - [ ] Program a first version on Python.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# HEXAPOD
