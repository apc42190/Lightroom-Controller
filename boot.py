import digitalio
import storage
import board

pin = digitalio.DigitalInOut(board.GP9)
pin.pull = digitalio.Pull.UP

#Hold top-left key to enable usb drive
if pin.value:
    print("Button not held. Disable drive")
    storage.disable_usb_drive()
else:
    print("Button held. Enable drive")
    storage.enable_usb_drive()
