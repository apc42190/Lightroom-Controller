import digitalio
import time
from adafruit_hid.keyboard import Keycode

#Tracks the slider that is currently selected inside lightroom classic
class LightroomState:
    def __init__(self, offset):
        self.state = offset

    def increment(self):
        self.state = (self.state + 1) % 13

    def decrement(self):
        self.state = (self.state - 1) % 13

#Manages rotary encoder logic
class Encoder:
    def __init__(self, clk_pin, dt_pin, keyboard, offset):
        self.clk = digitalio.DigitalInOut(clk_pin)
        self.clk.direction = digitalio.Direction.INPUT
        self.dt = digitalio.DigitalInOut(dt_pin)
        self.dt.direction = digitalio.Direction.INPUT
        self.last = None
        self.count = 0
        self.offset = offset
        self.keyboard = keyboard

    #Update lightroom selected slider until it matches the slider that is selected by the updated rotary encoder
    def equalizeState(self, state):
        if self.offset - state.state <= 0:
            while state.state != self.offset:
                self.keyboard.press(Keycode.COMMA)
                self.keyboard.release(Keycode.COMMA)
                state.decrement()
        else:
            while state.state != self.offset:
                self.keyboard.press(Keycode.PERIOD)
                self.keyboard.release(Keycode.PERIOD)
                state.increment()

    #If encoder moved clockwise, increase the value of selected slider
    def up(self, state):
        self.equalizeState(state)
        self.keyboard.press(Keycode.KEYPAD_PLUS)
        time.sleep(0.09)
        self.keyboard.release(Keycode.KEYPAD_PLUS)

    #If encoder moved counter-clockwise, decrease the value of selected slider
    def down(self, state):
        self.equalizeState(state)
        self.keyboard.press(Keycode.KEYPAD_MINUS)
        time.sleep(0.09)
        self.keyboard.release(Keycode.KEYPAD_MINUS)

    #Advances slider selection for this encoder and lightroom by 1
    def advance_offset(self, state):
        self.equalizeState(state)
        self.offset = (self.offset + 1) % 13
        self.keyboard.press(Keycode.PERIOD)
        self.keyboard.release(Keycode.PERIOD)
        state.increment()

    #Checks encoder for increase or decrease
    def read(self, state):
        #Encoder state has changed
        if self.last != self.clk.value:
            #The encoders used in this project trigger twice for every detent. Ignores half inputs.
            if self.count % 2 == 0:
                #Encoder rotated clockwise
                if self.clk.value != self.dt.value and self.last is not None:
                    self.up(state)
                    time.sleep(0.005)
                #Encoder rotated counter-clockwise
                elif self.clk.value == self.dt.value and self.last is not None:
                    self.down(state)
                    time.sleep(0.005)
            self.count += 1
            self.last = self.clk.value

