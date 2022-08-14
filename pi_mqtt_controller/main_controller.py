import paho.mqtt.client as mqtt
import threading
from sanitizer_start_motion import *
from sanitizer_end_motion import *
from mask_get import *
from mask_give import *
from namaste_start_mtn import *
from namaste_end_mtn import *
from hi_start_motion import *
from hi_end_motion import *
from get_to_normal_motion import *

from gpiozero import OutputDevice

ckt_trig_relay_pin=4
ckt_trig_relay=OutputDevice(ckt_trig_relay_pin,active_high=False, initial_value=False)
ckt_trig_relay.on()


sanitizer_trig_pin=6
sanitizer_trig=OutputDevice(sanitizer_trig_pin,active_high=False, initial_value=False)

sanitizer_start_complete_s=False
sanitizer_end_complete_s=False
hi_start_complete_s=False
hi_end_complete_s=False
namaste_start_complete_s=False
namaste_end_complete_s=False
mask_get_complete_s=False
mask_give_complete_s=False
goto_normal_complete_s=False

mqtt_server=('10.42.0.1',1883,60)


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
    global sanitizer_trig, sanitizer_start_complete_s,sanitizer_end_complete_s,hi_start_complete_s,hi_end_complete_s,mask_get_complete_s,mask_give_complete_s,namaste_start_complete_s,namaste_end_complete_s,goto_normal_complete_s
    if msg.topic=='sanitizer_start_motion':
        print('Sanitizer start received')
        sanitizer_start_thr=threading.Thread(target=sanitizer_start,daemon=True)
        sanitizer_start_thr.start()
        sanitizer_start_thr.join()
        sanitizer_start_complete_s=True
        sanitizer_trig.on()

    if msg.topic=='sanitizer_end_motion':
        print('Sanitize end received')
        sanitizer_trig.off()
        sanitizer_end_thr=threading.Thread(target=sanitizer_end,daemon=True)
        sanitizer_end_thr.start()
        sanitizer_end_thr.join()
        sanitizer_end_complete_s=True

    if msg.topic=='mask_get_motion':
        print('Mask get motion received')
        mask_get_thr=threading.Thread(target=get_mask,daemon=True)
        mask_get_thr.start()
        mask_get_thr.join()
        mask_get_complete_s=True

    if msg.topic=='mask_give_motion':
        print('Massk give motion received')
        mask_give_thr=threading.Thread(target=give_mask,daemon=True)
        mask_give_thr.start()
        mask_give_thr.join()
        mask_give_complete_s=True

    if msg.topic=='hi_start_motion':
        print('hi start received')
        hi_start_thr=threading.Thread(target=hi_start,daemon=True)
        hi_start_thr.start()
        hi_start_thr.join()
        hi_start_complete_s=True

    if msg.topic=='hi_end_motion':
        print('hi end received')
        hi_end_thr=threading.Thread(target=hi_end,daemon=True)
        hi_end_thr.start()
        hi_end_thr.join()
        hi_end_complete_s=True

    if msg.topic=='namaste_start_motion':
        print('Namaste start motion received')
        namaste_start_thr=threading.Thread(target=namaste_start,daemon=True)
        namaste_start_thr.start()
        namaste_start_thr.join()
        namaste_start_complete_s=True

    if msg.topic=='namaste_end_motion':
        print('Namaste end motion received')
        namaste_end_thr=threading.Thread(target=namaste_end,daemon=True)
        namaste_end_thr.start()
        namaste_end_thr.join()
        namaste_end_complete_s=True

    if msg.topic=='goto_normal_motion':
        print('Goto normal motion received')
        goto_normal_thr=threading.Thread(target=get_to_normal,daemon=True)
        goto_normal_thr.start()
        goto_normal_thr.join()
        goto_normal_complete_s=True

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server[0],mqtt_server[1],mqtt_server[2])

mqtt_thread=threading.Thread(target=client_loop,daemon=True)
mqtt_thread.start()

while True:
    if(sanitizer_start_complete_s):
        client.publish('sanitizer_start_complete','1')
        sanitizer_start_complete_s=False

    if(sanitizer_end_complete_s):
        client.publish('sanitizer_end_complete','1')
        sanitize_complete_s=False

    if(hi_start_complete_s):
        client.publish('hi_start_complete','1')
        hi_start_complete_s=False

    if(hi_end_complete_s):
        client.publish('hi_end_complete','1')
        hi_end_complete_s=False

    if(mask_get_complete_s):
        client.publish('mask_get_complete','1')
        mask_get_complete_s=False

    if(mask_give_complete_s):
        client.publish('mask_give_complete','1')
        mask_give_complete_s=False

    if(namaste_start_complete_s):
        client.publish('namaste_start_complete','1')
        namaste_start_complete_s=False

    if(namaste_end_complete_s):
        client.publish('namaste_end_complete','1')
        namaste_end_complete_s=False

    if(goto_normal_complete_s):
        client.publish('goto_normal_complete','1')
        goto_normal_complete_s=False

    time.sleep(0.1)