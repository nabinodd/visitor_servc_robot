import paho.mqtt.client as mqtt
import threading
import time


sanitizer_start_complete_s=False
sanitizer_end_complete_s=False
hi_start_complete_s=False
hi_end_complete_s=False
namaste_start_complete_s=False
namaste_end_complete_s=False
mask_get_complete_s=False
mask_give_complete_s=False
goto_normal_complete_s=False

mqtt_server=('localhost',1883,60)


def client_loop():
	global client
	while True:
		client.loop()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('sanitizer_start_motion')
    client.subscribe('sanitizer_end_motion')
    client.subscribe('mask_get_motion')
    client.subscribe('mask_give_motion')
    client.subscribe('hi_start_motion')
    client.subscribe('hi_end_motion')
    client.subscribe('namaste_start_motion')
    client.subscribe('namaste_end_motion')
    client.subscribe('goto_normal_motion')

def on_message(client, userdata, msg):
    global  sanitizer_start_complete_s,sanitizer_end_complete_s,hi_start_complete_s,hi_end_complete_s,mask_get_complete_s,mask_give_complete_s,namaste_start_complete_s,namaste_end_complete_s,goto_normal_complete_s
    if msg.topic=='sanitizer_start_motion':
        print('[CMD]Sanitizer start received')
        time.sleep(3)
        sanitizer_start_complete_s=True

    if msg.topic=='sanitizer_end_motion':
        print('[CMD]Sanitize end received')
        time.sleep(3)
        sanitizer_end_complete_s=True


    if msg.topic=='mask_get_motion':
        print('[CMD]Mask get motion received')
        time.sleep(5)
        mask_get_complete_s=True

    if msg.topic=='mask_give_motion':
        print('[CMD]Mask give motion received')
        time.sleep(5)
        mask_give_complete_s=True

    if msg.topic=='hi_start_motion':
        print('[CMD]Hi start received')
        time.sleep(5)
        hi_start_complete_s=True

    if msg.topic=='hi_end_motion':
        print('[CMD]Hi end received')
        time.sleep(5)
        hi_end_complete_s=True

    if msg.topic=='namaste_start_motion':
        print('[CMD]Namaste start motion received')
        time.sleep(8)
        namaste_start_complete_s=True


    if msg.topic=='namaste_end_motion':
        print('[CMD]Namaste end motion received')
        time.sleep(5)
        namaste_end_complete_s=True

    if msg.topic=='goto_normal_motion':
        print('[CMD]Goto normal motion received')
        time.sleep(10)
        goto_normal_complete_s=True

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server[0],mqtt_server[1],mqtt_server[2])

mqtt_thread=threading.Thread(target=client_loop,daemon=True)
mqtt_thread.start()

while True:
    if(sanitizer_start_complete_s):
        print('[OK]Sanitizer start complete\n')
        client.publish('sanitizer_start_complete','1')
        sanitizer_start_complete_s=False

    if(sanitizer_end_complete_s):
        print('[OK]Sanitizer end complete\n')
        client.publish('sanitizer_end_complete','1')
        sanitizer_end_complete_s=False

    if(hi_start_complete_s):
        print('[OK]Hi start complete\n')
        client.publish('hi_start_complete','1')
        hi_start_complete_s=False

    if(hi_end_complete_s):
        print('[OK]Hi end complete\n')
        client.publish('hi_end_complete','1')
        hi_end_complete_s=False

    if(mask_get_complete_s):
        print('[OK]Mask get motion complete\n')
        client.publish('mask_get_complete','1')
        mask_get_complete_s=False

    if(mask_give_complete_s):
        print('[OK]Mask give motion complete\n')
        client.publish('mask_give_complete','1')
        mask_give_complete_s=False

    if(namaste_start_complete_s):
        print('[OK]Namaste start motion complete\n')
        client.publish('namaste_start_complete','1')
        namaste_start_complete_s=False

    if(namaste_end_complete_s):
        print('[OK]Namaste end motion complete\n')
        client.publish('namaste_end_complete','1')
        namaste_end_complete_s=False

    if(goto_normal_complete_s):
        print('[OK]Goto normal motion complete\n')
        client.publish('goto_normal_complete','1')
        goto_normal_complete_s=False

    time.sleep(0.1)