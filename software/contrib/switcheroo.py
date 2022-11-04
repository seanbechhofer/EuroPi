from europi import *
import machine
from europi_script import EuroPiScript
from time import ticks_diff, ticks_ms
from random import randint

"""
Switcheroo
author: Sean Bechhofer (github.com/seanbechhofer)
date: 2022-10-31
labels: switch

Sequential switch that allows an input to be piped to different
outputs. The selected output changes on each clock pulse.  The results
can then be used to, e.g. create arpeggios.  

Knob 2 adds an offset to the input signal, allowing the app to be used
as a clocked source of triggers without any input.

digital_in: clock in
analog_in: signal in

knob_1: unused
knob_2: signal offset

button_1: Short Press: decrease outputs. Long Press: cycle mode
button_2: Short Press: increase outputs. Long Press: unused
output_n: Mirrored input+offset or zero depending on selection

The reading of the input signal is not particularly sophisticated. As
a results this is not intended for use with audio input. But it might
be fun to try it.  
"""

# Version number

VERSION = "1.0"

# Offset range.

OFFSET = 5


class Direction:
    FWD = 0
    REV = 1
    RND = 2
    PND = 3
    count = 4


class Switcheroo(EuroPiScript):
    def __init__(self):
        # Overclock the Pico for improved performance.
        machine.freq(250_000_000)
        self.dirty = True
        self.direction = Direction.FWD
        self.selected = 0
        self.outputs = 3
        # State of the pendulum mode. True means ascending, false descending. 
        self.pendulum_forward = True
        # Zero everything
        [cv.off() for cv in cvs]

        # Triggered when din goes HIGH.
        @din.handler
        def dinTrigger():
            # Set selected output to 0 cvs[self.selected].off() Set
            # all outputs to 0. This could probably be done better.
            [cv.off() for cv in cvs]

            # Calculate which output to use.
            if self.direction == Direction.FWD:
                self.selected = (self.selected + 1) % self.outputs
            elif self.direction == Direction.REV:
                self.selected = (self.selected - 1) % self.outputs
            elif self.direction == Direction.RND:
                self.selected = randint(0, self.outputs - 1)
            elif self.direction == Direction.PND:
                # If outputs is == 1 then we don't want to do anything as the output will not change. 
                if self.outputs > 1:
                    if self.pendulum_forward:
                        # Forwards
                        # Are we at the end? 
                        if self.selected == (self.outputs - 1):
                            # Turn around
                            self.pendulum_forward = False
                            self.selected = self.selected - 1
                        else:
                            self.selected = self.selected + 1
                    else:
                        # Backwards
                        # Are we at the beginning?
                        if self.selected == 0:
                            # Turn around
                            self.pendulum_forward = True
                            self.selected = self.selected + 1
                        else:
                            self.selected = self.selected - 1
            # Do we need to now set the value? Or can we rely on update picking this up?

        @din.handler_falling
        def dinTriggerEnd():
            # Don't do anything
            pass

        # Triggered when button 1 is released
        # Short press: add output
        # Long press: cycle direction
        @b1.handler_falling
        def b1Pressed():
            if ticks_diff(ticks_ms(), b1.last_pressed()) > 300:
                # increment direction
                self.direction = (self.direction + 1) % Direction.count
            else:
                # decrement outputs
                self.outputs = max(self.outputs - 1, 1)
            self.dirty = True

        # Triggered when button 2 is released
        # Short press: remove output
        # Long press: unused
        @b2.handler_falling
        def b2Pressed():
            if ticks_diff(ticks_ms(), b2.last_pressed()) > 300:
                pass
            else:
                # increment outputs
                self.outputs = min(self.outputs + 1, 6)
            self.dirty = True

    def update(self):
        # Sample input
        sample = ain.read_voltage()

        # Get offset
        offset = k2.read_position()

        # Pass sample to active output
        cvs[self.selected].voltage(sample + (OFFSET * offset) / 100)

    def main(self):
        while True:
            self.update()
            if self.dirty:
                self.update_screen()
                self.dirty = False

    def update_screen(self):
        oled.fill(0)
        oled.text(f"Switcheroo v{VERSION}", 0, 0, 1)
        oled.text("outs:" + str(int(self.outputs)), 0, 8, 1)
        mode = "---"
        if self.direction == Direction.FWD:
            mode = "fwd"
        elif self.direction == Direction.REV:
            mode = "rev"
        elif self.direction == Direction.RND:
            mode = "rnd"
        elif self.direction == Direction.PND:
            mode = "pnd"
        oled.text("mode:" + mode, 0, 16, 1)
        # Show info about selection
        oled.show()


if __name__ == "__main__":
    Switcheroo().main()
