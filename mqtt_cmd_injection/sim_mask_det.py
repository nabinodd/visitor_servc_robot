import paho.mqtt.client as mqtt
import threading
import random
import time


mqtt_server=('localhost',1883,60)

p_streaming_sts=False
np_streaming_sts=False
person=False

def client_loop():
	global client
	while True:
		client.loop()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('person_enter')
    client.subscribe('person_exit')


def on_message(client, userdata, msg):

    global p_streaming_sts,np_streaming_sts,person

    if msg.topic=='person_enter':
        print('[INF]Person entered in the frame')
        person=True
        p_streaming_sts=True


    if msg.topic=='person_exit':
        print('[INF]Person exited from the frame')
        person=False
        np_streaming_sts=True

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server[0],mqtt_server[1],mqtt_server[2])

mqtt_thread=threading.Thread(target=client_loop,daemon=True)
mqtt_thread.start()

while True:
    if(p_streaming_sts):
        client.publish('streaming','1')
        print('[INF]Stream start published\n')
        time.sleep(2)

        tmpr=str(random.randint(35,41))
        mask_sts=random.choice(['0','1'])

        client.publish('mask_result_tmpr',mask_sts+','+tmpr)
        print('[INF]Mask result & temperature published\n')

        p_streaming_sts=False

    if(np_streaming_sts and not person):
        client.publish('streaming','0')
        print('[INF]Streram Stop\n')
        np_streaming_sts=False

    else:
        time.sleep(0.1)