import paho.mqtt.client as mqtt
from smbus2 import SMBus
import threading
import time
from gpiozero import OutputDevice

ckt_trig_relay_pin=4
ckt_trig_relay=OutputDevice(ckt_trig_relay_pin,active_high=False, initial_value=False)
ckt_trig_relay.on()


bus=SMBus(1)

mot_pos_reg=1
mot_ccw_reg=2
mot_stop_reg=3

new_cmd=False
cmd=''

mqtt_server=('10.42.0.1',1883,60)
# mqtt_server=('192.168.0.109',1883,60)

def client_loop():
	global client
	while True:
		client.loop()

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe('cmd_ctl')

def on_message(client, userdata, msg):
    global cmd,new_cmd
    if msg.topic=='cmd_ctl':
        cmd=msg.payload.decode()
        print(cmd)
        new_cmd=True

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


while True:
    if(new_cmd):
        new_cmd=False
        cmd_sep=cmd.split(',')

        addr=int(cmd_sep[0])
        reg=int(cmd_sep[1])
        pos=cmd_sep[2]
        if len(pos)==1:
            pos='0'+'0'+pos
        elif len(pos)==2:
            pos='0'+pos
        pos_bytes=bytearray(pos,'ascii')
        try:
            bus.write_block_data(addr,reg,pos_bytes)
            print('Sent : ',addr,' ',reg,' ',pos )
            # request_pos(addr)

        except:
            print('Cannot send : ',addr,' ',reg,' ',pos )

    time.sleep(0.1)