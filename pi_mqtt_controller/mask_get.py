from gpiozero import DigitalInputDevice
from motor_class import MotorNode
import pigpio
import time

pi=pigpio.pi()

initial_wrist_pos=1500
right_wrist_pin=10
pi.set_servo_pulsewidth(right_wrist_pin,initial_wrist_pos)


def get_mask():
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


    right_shoulder.rotate_to_pos(3,blocking=True)
    right_chest.send_init()
    time.sleep(1)
    right_chest.check_init(blocking=True)
    time.sleep(1)
    right_arm.send_init()
    right_arm.check_init(blocking=True)
    right_elbow.rotate_to_pos(100,blocking=True)
    right_forearm.rotate_to_pos(50,blocking=True)
    pi.set_servo_pulsewidth(right_wrist_pin,1850)
    print('Getting mask.............')


