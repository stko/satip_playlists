from gpiozero import Button
from subprocess import check_call
from signal import pause


def reboot():
    check_call(["sudo", "reboot"])


reboot_btn = Button(3, hold_time=2)
reboot_btn.when_held = reboot

pause()
