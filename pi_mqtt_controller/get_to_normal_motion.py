from gpiozero import DigitalInputDevice
from motor_class import MotorNode
import pigpio
import time


pi=pigpio.pi()

initial_wrist_pos=1500
right_wrist_pin=10
left_wrist_pin=9

# pi.set_servo_pulsewidth(right_wrist_pin,initial_wrist_pos)


def get_to_normal():
    right_chest_pin=DigitalInputDevice(8,pull_up=None,active_state=False)
    right_chest=MotorNode(12,right_chest_pin,'right_chest')

    right_shoulder_pin=DigitalInputDevice(12,pull_up=None,active_state=False)
    right_shoulder=MotorNode(13,right_shoulder_pin,'right_shoulder')

    right_arm_pin=DigitalInputDevice(16,pull_up=None,active_state=False)
    right_arm=MotorNode(14,right_arm_pin,'right_arm')

    right_elbow_pin=DigitalInputDevice(20,pull_up=None,active_state=False)
    right_elbow=MotorNode(15,right_elbow_pin,'right_elbow')

    right_forearm_pin=DigitalInputDevice(21,pull_up=None,active_state=False)
    right_forearm=MotorNode(16,right_forearm_pin,'right_forearm')

    left_chest_pin=DigitalInputDevice(15,pull_up=None,active_state=False)
    left_chest=MotorNode(22,left_chest_pin,'left_chest')

    left_shoulder_pin=DigitalInputDevice(18,pull_up=None,active_state=False)
    left_shoulder=MotorNode(23,left_shoulder_pin,'left_shoulder')

    left_arm_pin=DigitalInputDevice(23,pull_up=None,active_state=False)
    left_arm=MotorNode(24,left_arm_pin,'left_arm')

    left_elbow_pin=DigitalInputDevice(24,pull_up=None,active_state=False)
    left_elbow=MotorNode(25,left_elbow_pin,'left_elbow')

    left_forearm_pin=DigitalInputDevice(19,pull_up=None,active_state=False)
    left_forearm=MotorNode(26,left_forearm_pin,'left_forearm')


    right_shoulder.rotate_to_pos(15,blocking=True)
    left_shoulder.rotate_to_pos(15,blocking=True)

    right_chest.send_init()
    left_chest.send_init()

    right_chest.check_init(blocking=True)
    left_chest.check_init(blocking=True)

    right_chest.rotate_to_pos(10,blocking=True)
    left_chest.rotate_to_pos(10,blocking=True)

    right_elbow.send_init()
    left_elbow.send_init()
    right_elbow.check_init(blocking=True)
    left_elbow.check_init(blocking=True)

    right_forearm.send_init()
    left_forearm.send_init()

    right_arm.send_init()
    left_arm.send_init()

    # right_forearm.rotate_to_pos(100,blocking=True)
    # left_forearm.rotate_to_pos(120,blocking=True)

    # right_arm.rotate_to_pos(200,blocking=True)
    # left_arm.rotate_to_pos(200,blocking=True)

    right_forearm.check_init(blocking=True)
    left_forearm.check_init(blocking=True)

    right_forearm.rotate_to_pos(100)
    left_forearm.rotate_to_pos(120)

    right_arm.check_init(blocking=True)
    left_arm.check_init(blocking=True)

    right_arm.rotate_to_pos(200)
    left_arm.rotate_to_pos(200)

    right_shoulder.send_init()
    left_shoulder.send_init()
    right_shoulder.check_init(blocking=True)
    left_shoulder.check_init(blocking=True)

    pi.set_servo_pulsewidth(right_wrist_pin,initial_wrist_pos)
    pi.set_servo_pulsewidth(left_wrist_pin,initial_wrist_pos)


# get_to_normal()