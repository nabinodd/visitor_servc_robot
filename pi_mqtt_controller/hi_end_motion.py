from gpiozero import DigitalInputDevice
from motor_class import MotorNode


def hi_end():
    right_shoulder_pin=DigitalInputDevice(12,pull_up=None,active_state=False)
    right_shoulder=MotorNode(13,right_shoulder_pin,'right_shoulder')


    right_arm_pin=DigitalInputDevice(16,pull_up=None,active_state=False)
    right_arm=MotorNode(14,right_arm_pin,'right_arm')

    right_elbow_pin=DigitalInputDevice(20,pull_up=None,active_state=False)
    right_elbow=MotorNode(15,right_elbow_pin,'right_elbow')

    right_elbow.rotate_to_pos(230,blocking=True)
    right_elbow.rotate_to_pos(180,blocking=True)
    right_elbow.rotate_to_pos(230,blocking=True)

    right_elbow.send_init()
    right_elbow.check_init(blocking=True)

    right_shoulder.send_init()
    right_shoulder.check_init(blocking=True)
    right_arm.send_init()
    right_arm.check_init(blocking=True)
    right_arm.rotate_to_pos(200,blocking=True)
