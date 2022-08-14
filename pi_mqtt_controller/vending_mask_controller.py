import paho.mqtt.client as mqtt
from smbus2 import SMBus
import threading
import time

bus=SMBus(1)

new_cmd=False
cmd=''

vending_init=False

mqtt_server=('10.42.0.1',1883,60)

class  VendMotor(SMBus):
    def __init__(self,_reg):
        self.reg=_reg

    def drop(self):

        try:
            bus.write_block_data(44,self.reg,b'\x00')
            print('Sent drop command')

        except:
            print('Cannot send')

mot1=VendMotor(1)
mot2=VendMotor(2)
mot3=VendMotor(3)
mot4=VendMotor(4)
mot5=VendMotor(5)

nums_left={mot1:0,mot2:0,mot3:0,mot4:0,mot5:0}


def client_loop():
	global client
	while True:
		client.loop()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('vending_drop')
    client.subscribe('resp_vending')

def on_message(client, userdata, msg):
    global nums_left,vending_init
    if msg.topic=='vending_drop':
        drop_mask()

    if msg.topic=='resp_vending':
        print('Got msg')
        nums=msg.payload.decode()
        print(nums)
        nums_sep=nums.split(',')
        nums_left={mot1:int(nums_sep[0]),mot2:int(nums_sep[1]),mot3:int(nums_sep[2]),mot4:int(nums_sep[3]),mot5:int(nums_sep[4])}
        vending_init=True


def on_log(client,userdata,level,buf):
    print('log: '+buf)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server[0],mqtt_server[1],mqtt_server[2])
mqtt_thread=threading.Thread(target=client_loop,daemon=True)
mqtt_thread.start()



def check_empty():
    global nums_left
    empty=True
    for key in nums_left:
        if nums_left[key]==0:
            empty=True
        elif nums_left[key]!=0:
            empty=False
    return empty


def drop_mask():
    global nums_left
    l=[]
    s=''
    if(not check_empty()):
        for key in nums_left:
            if nums_left[key]!=0:
                key.drop()
                nums_left[key]=nums_left[key]-1

                for key in  nums_left:
                    l.append(nums_left[key])

                for n in l:
                    s=s+str(n)+','
                s=s[:-1]
                print(s)
                client.publish('set_vending',s)
                break

    elif (check_empty()):
        print('All slots empty!!!!')

client.publish('get_vending','1')

while not vending_init:
    time.sleep(1)

mqtt_thread.join()