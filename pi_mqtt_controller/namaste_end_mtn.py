from gpiozero import DigitalInputDevice
from motor_class import MotorNode
import pigpio
import time

pi=pigpio.pi()

initial_neck_pos=1500
neck_servo_pin=27
pi.set_servo_pulsewidth(neck_servo_pin,initial_neck_pos)


def namaste_end():

    right_chest_pin=DigitalInputDevice(8,pull_up=None,active_state=False)
    right_chest=MotorNode(12,right_chest_pin,'right_chest')

    right_shoulder_pin=DigitalInputDevice(12,pull_up=None,active_state=False)
    right_shoulder=MotorNode(13,right_shoulder_pin,'right_shoulder')

    right_arm_pin=DigitalInputDevice(16,pull_up=None,active_state=False)
    right_arm=MotorNode(14,right_arm_pin,'right_arm')

    right_elbow_pin=DigitalInputDevice(20,pull_up=None,active_state=False)
    right_elbow=MotorNode(15,right_elbow_pin,'right_elbow')


    left_chest_pin=DigitalInputDevice(15,pull_up=None,active_state=False)
    left_chest=MotorNode(22,left_chest_pin,'left_chest')

    left_shoulder_pin=DigitalInputDevice(18,pull_up=None,active_state=False)
    left_shoulder=MotorNode(23,left_shoulder_pin,'left_shoulder')

    left_arm_pin=DigitalInputDevice(23,pull_up=None,active_state=False)
    left_arm=MotorNode(24,left_arm_pin,'left_arm')

    left_elbow_pin=DigitalInputDevice(24,pull_up=None,active_state=False)
    left_elbow=MotorNode(25,left_elbow_pin,'left_elbow')


    for i in range(1500,1100,-50):
        pi.set_servo_pulsewidth(neck_servo_pin,i)

    print('Namaste done')
    time.sleep(1)

    for i in range(1100,1500,50):
        pi.set_servo_pulsewidth(neck_servo_pin,i)

    right_elbow.send_init()
    left_elbow.send_init()
    time.sleep(1)

    right_elbow.check_init(blocking=True)
    left_elbow.check_init(blocking=True)

    right_chest.send_init()
    left_chest.send_init()

    right_arm.send_init()
    left_arm.send_init()

    time.sleep(1)
    right_chest.check_init(blocking=True)
    left_chest.check_init(blocking=True)

    right_arm.check_init(blocking=True)
    left_arm.check_init(blocking=True)

    right_chest.rotate_to_pos(9,blocking=True)
    left_chest.rotate_to_pos(9,blocking=True)
    time.sleep(1)

    right_shoulder.send_init()
    left_shoulder.send_init()
    time.sleep(1)

    right_shoulder.check_init(blocking=True)
    left_shoulder.check_init(blocking=True)

    right_arm.rotate_to_pos(200,blocking=True)
    left_arm.rotate_to_pos(200,blocking=True)
    print('Set to normal')


