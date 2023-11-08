import digitalio
import time
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keycode
from adafruit_debouncer import Debouncer
from encoder import Encoder, LightroomState

keyboard = Keyboard(usb_hid.devices)

key_pins = (board.GP9, board.GP10, board.GP15, board.GP8, board.GP11, board.GP14, board.GP7, board.GP12, board.GP13)
buttons = []
for pin in key_pins:
    tmp_pin = digitalio.DigitalInOut(pin)
    tmp_pin.pull = digitalio.Pull.UP
    buttons.append(Debouncer(tmp_pin))

#Defining keyboard key combos for each keyswitch
button_mapping = {
    buttons[0] : [Keycode.KEYPAD_ONE],
    buttons[1] : [Keycode.KEYPAD_TWO],
    buttons[2] : [Keycode.KEYPAD_THREE],
    buttons[3] : [Keycode.KEYPAD_FOUR],
    buttons[4] : [Keycode.KEYPAD_FIVE],
    buttons[5] : [Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.C],
    buttons[6] : [Keycode.LEFT_ARROW],
    buttons[7] : [Keycode.RIGHT_ARROW],
    buttons[8] : [Keycode.LEFT_CONTROL, Keycode.LEFT_SHIFT, Keycode.V],
}

#Tracks the currently active slider in Lightroom(E.G. Temperature, Tint, etc)
lightroom_state = LightroomState(0)

dial_1_pin = digitalio.DigitalInOut(board.GP1)
dial_1_pin.direction = digitalio.Direction.INPUT
dial_1_pin.pull = digitalio.Pull.UP
dial_1_button = Debouncer(dial_1_pin)

dial_2_pin = digitalio.DigitalInOut(board.GP26)
dial_2_pin.direction = digitalio.Direction.INPUT
dial_2_pin.pull = digitalio.Pull.UP
dial_2_button = Debouncer(dial_2_pin)

dial_1_encoder = Encoder(board.GP2, board.GP0, keyboard, 2)
dial_2_encoder = Encoder(board.GP21, board.GP22, keyboard, 0)


while(1):
    for button in buttons:
        button.update()
        if button.fell:
            for key in button_mapping[button]:
                keyboard.press(key)
            time.sleep(0.09)
            keyboard.release_all()
            if button == buttons[5]:
                    #Confirm copy pop-up
                    keyboard.press(Keycode.KEYPAD_ENTER)
                    time.sleep(0.09)
                    keyboard.release(Keycode.KEYPAD_ENTER)

    dial_1_button.update()
    if dial_1_button.fell:
        dial_1_encoder.advance_offset(lightroom_state)

    dial_2_button.update()
    if dial_2_button.fell:
        dial_2_encoder.advance_offset(lightroom_state)

    dial_1_encoder.read(lightroom_state)
    dial_2_encoder.read(lightroom_state)
