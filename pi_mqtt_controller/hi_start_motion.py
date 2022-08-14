from gpiozero import DigitalInputDevice
from motor_class import MotorNode

def hi_start():
    right_shoulder_pin=DigitalInputDevice(12,pull_up=None,active_state=False)
    right_shoulder=MotorNode(13,right_shoulder_pin,'right_shoulder')


    right_arm_pin=DigitalInputDevice(16,pull_up=None,active_state=False)
    right_arm=MotorNode(14,right_arm_pin,'right_arm')

    right_shoulder.rotate_to_pos(20,blocking=True)
    right_arm.rotate_to_pos(446,blocking=True)