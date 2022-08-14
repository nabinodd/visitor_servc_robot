from gpiozero import DigitalInputDevice
from motor_class import MotorNode
from gpiozero import OutputDevice
import time


def sanitizer_end():

    # sanitizer_trig_pin=6
    # sanitizer_trig=OutputDevice(sanitizer_trig_pin,active_high=False, initial_value=False)

    left_chest_pin=DigitalInputDevice(15,pull_up=None,active_state=False)
    left_chest=MotorNode(22,left_chest_pin,'left_chest')

    left_shoulder_pin=DigitalInputDevice(18,pull_up=None,active_state=False)
    left_shoulder=MotorNode(23,left_shoulder_pin,'left_shoulder')

    # sanitizer_trig.off()

    left_chest.send_init()
    # left_chest.send_data_to_i2c(4)
    left_chest.check_init(blocking=True)
    left_chest.rotate_to_pos(9,blocking=True)
    time.sleep(1)

    left_shoulder.send_init()
    # left_shoulder.send_data_to_i2c(4)
    left_shoulder.check_init(blocking=True)
