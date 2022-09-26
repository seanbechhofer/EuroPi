# EuroPi Switcheroo - Sequential Switch

author: Sean Bechhofer (github.com/seanbechhofer)

date: 2022-09026

labels: switch, clock, randomness

**The old Switcheroo!**

Switcheroo is an app that allows an input to be piped to different outputs. The selected output changes on each clock pulse. 
The results can then be used to, e.g. create arpeggios. 

Demo video: XXX

Credits:
- The Europi hardware and firmware was designed by Allen Synthesis:
https://github.com/Allen-Synthesis/EuroPi

# Controls

- digital_in: Clock in
- analog_in: Signal in

- knob_1: unused
- knob_2: Signal offset

- button_1: Short Press: Select operating mode
- button_2: Short Press: Cycle through numbers of outputs

- output_n: Mirrored input or zero depending on selection

# Operation

The app reads a signal from the analog input and then pipes the resulting value to the selected output. 
Value at unselected outputs is zero. 
The value from knob 2 is also added to the output, allowing for operation without an input value -- for example providing a constant value for triggers/gates. 

## Basic Usage
1. Connect a clock input to the Digital input
2. Connect an input to the Analog output
3. Dial in required offset
4. Select mode using button 1
5. Select number of outputs using button 2
6. Start your clock - when a clock pulse is received, the active output channel will switch. Inactive channels are zeroed. 

## Modes

The examples below assume 4 outputs are active. 
1. Forward. Outputs change in order e.g. *1, 2, 3, 4, 1, 2, 3, 4, ...*
2. Reverse. Outputs change in reverse order e.g. *4, 3, 2, 1, 4, 3, 2, 1, ...*
3. Pendulum. Outputs change back and forth e.g. *1, 2, 3, 4, 3, 2, 1, 2, 3, ...*
4. Random. Random output selected. 

# Known bugs / Interesting features

Probably. 
