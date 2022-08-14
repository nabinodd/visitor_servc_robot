from gpiozero import DigitalInputDevice
from motor_class import MotorNode
from gpiozero import OutputDevice
import time


def sanitizer_start():

    # sanitizer_trig_pin=6
    # sanitizer_trig=OutputDevice(sanitizer_trig_pin,active_high=False, initial_value=False)

    left_chest_pin=DigitalInputDevice(15,pull_up=None,active_state=False)
    left_chest=MotorNode(22,left_chest_pin,'left_chest')

    left_shoulder_pin=DigitalInputDevice(18,pull_up=None,active_state=False)
    left_shoulder=MotorNode(23,left_shoulder_pin,'left_shoulder')

    left_shoulder.rotate_to_pos(7,blocking=True)

    left_chest.send_init()
    time.sleep(1)
    left_chest.check_init(blocking=True)

    left_chest.rotate_to_pos(32,blocking=True)
    print('Rotation complete to 32')
    # sanitizer_trig.on()
    print('Giving sanitizer...........')