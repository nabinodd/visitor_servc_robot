import paho.mqtt.client as mqtt
from smbus2 import SMBus
import threading
import pigpio
import time
from gpiozero import OutputDevice

ckt_trig_relay_pin=4

bus=SMBus(1)
pi=pigpio.pi()


right_wrist_pin=10
left_wrist_pin=9
head_servo_pin=27
initial_wrist_pos=1500
initial_head_servo_pos=1500

pi.set_servo_pulsewidth(right_wrist_pin,initial_wrist_pos)
pi.set_servo_pulsewidth(left_wrist_pin,initial_wrist_pos)
pi.set_servo_pulsewidth(head_servo_pin,initial_head_servo_pos)

ckt_trig_relay=OutputDevice(ckt_trig_relay_pin,active_high=False, initial_value=False)
ckt_trig_relay.on()

mot_cw_reg=1
mot_ccw_reg=2
mot_stop_reg=3

new_cmd=False
cmd=''

mqtt_server=('10.42.0.1',1883,60)

def client_loop():
	global client
	while True:
		client.loop()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('joys_ctl')
    client.subscribe('joys_ctl/right_wrist')
    client.subscribe('joys_ctl/left_wrist')
    client.subscribe('joys_ctl/head_servo')

def on_message(client, userdata, msg):
    global cmd,new_cmd,pi
    if msg.topic=='joys_ctl':
        cmd=msg.payload.decode()
        print(cmd)
        new_cmd=True
    elif msg.topic=='joys_ctl/right_wrist':
        r_pos=msg.payload.decode()
        r_pos_val=map(float(r_pos))
        pi.set_servo_pulsewidth(right_wrist_pin,r_pos_val)
        print('Pos : ',r_pos_val)

    elif msg.topic=='joys_ctl/left_wrist':
        l_pos=msg.payload.decode()
        l_pos_val=map(float(l_pos))
        pi.set_servo_pulsewidth(left_wrist_pin,l_pos_val)
        print('Pos : ',l_pos_val)

    elif msg.topic=='joys_ctl/head_servo':
        head_servo_pos=msg.payload.decode()
        head_servo_val=map(float(head_servo_pos))
        pi.set_servo_pulsewidth(head_servo_pin,head_servo_val)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server[0],mqtt_server[1],mqtt_server[2])

mqtt_thread=threading.Thread(target=client_loop,daemon=True)
mqtt_thread.start()

def request_pos(addr):
    try:
        data=bus.read_i2c_block_data(addr,4,4)
        print('Received data : ',data)
    except:
        print('Cannot query data')

def map(v, in_min=-1, in_max=1, out_min=500, out_max=2500):
	if v < in_min:
		v = in_min
	if v > in_max:
		v = in_max
	return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    if(new_cmd):
        new_cmd=False
        cmd_sep=cmd.split(',')

        addr=int(cmd_sep[0])
        reg=int(cmd_sep[1])
        speed=cmd_sep[2]
        if len(speed)==1:
            speed='0'+'0'+speed
        elif len(speed)==2:
            speed='0'+speed
        speed=bytearray(speed,'ascii')

        try:
            bus.write_block_data(addr,reg,speed)
            print('Sent : ',addr, reg,speed)
            # request_pos(addr)

        except:
            print('Cannot send')

    time.sleep(0.1)