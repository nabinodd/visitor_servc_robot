import paho.mqtt.client as mqtt
import pygame
import time

pygame.init()

nos_joy=pygame.joystick.get_count()

if nos_joy==0:
    print('[ERR] No Joystick found')
else:
    print('Joysticks : ',pygame.joystick.get_count())

    r_controller=pygame.joystick.Joystick(0)
    l_controller=pygame.joystick.Joystick(1)

    l_controller.init()
    r_controller.init()

    print('[INF] Controller initalized')

broker='192.168.0.109'
client=mqtt.Client('2joys_pub')


def on_log(client,userdata,level,buf):
    print('log: '+buf)

def on_connect(client,userdata,flags,rc):
    if rc==0:
        print('Connected OK')
    else:
        print('Not connected : ',rc)


client.on_connect=on_connect
# client.on_log=on_log

print('Connecting to broker : ',broker)
client.will_set('botst/conn','0')
client.connect(broker)
client.loop_start()

def map(v, in_min=0, in_max=1.0, out_min=0, out_max=255):
	if v < in_min:
		v = in_min
	if v > in_max:
		v = in_max
	return int((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

addr_dict={'neck':11,'r_chest':12,'r_shoulder':13,'r_arm':14,'r_elbow':15,'r_forearm':16}

addl_dict={'l_chest':22,'l_shoulder':23,'l_arm':24,'l_elbow':25,'l_forearm':26}

dirn={'cw':1,'ccw':2,'stp':3}

addrs=None
addls=None

def send_cmd(addr,dirnn,speed,side):
    if side=='right':
        cmd=str(addr_dict[addr])+','+str(dirn[dirnn])+','+str(speed)
        client.publish('joys_ctl',cmd)
        print('Command : ',cmd)


    elif side=='left':
        cmd=str(addl_dict[addr])+','+str(dirn[dirnn])+','+str(speed)
        client.publish('joys_ctl',cmd)
        print('Command : ',cmd)


while True:
    time.sleep(0.1)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True

    if nos_joy!=0:
        # left_x=l_controller.get_axis(0)
        left_y=l_controller.get_axis(2)
        right_y=r_controller.get_axis(2)

        right_btn_ul=r_controller.get_button(4)
        right_btn_ur=r_controller.get_button(5)
        right_btn_dl=r_controller.get_button(2)
        right_btn_dr=r_controller.get_button(3)
        right_thmb=r_controller.get_button(1)
        right_trig_btn=r_controller.get_button(0)


        left_btn_ul=l_controller.get_button(4)
        left_btn_ur=l_controller.get_button(5)
        left_btn_dl=l_controller.get_button(2)
        left_btn_dr=l_controller.get_button(3)
        left_thmb=l_controller.get_button(1)
        left_trig_btn=l_controller.get_button(0)


        right_hat_up=r_controller.get_hat(0)
        right_hat_r=r_controller.get_hat(0)



        # print(right_btn_ul,right_btn_ur,right_btn_dl,right_btn_dr,right_thmb,right_trig_btn)


        if right_y<0:
            r_speed_val=-right_y
            r_direction='cw'

        elif right_y>0:
            r_speed_val=right_y
            r_direction='ccw'

        elif right_y==0:
            r_speed_val=0
            r_direction='stp'

        # print('Left X: ',left_x,' Left Y: ',left_y,' Right Y: ',right_y)
        if right_btn_dl==1:
            addrs='r_arm'
            print('R Arm')

        elif right_btn_dr==1:
            addrs='r_shoulder'
            print('R Shoulder')

        elif right_btn_ul==1:
            addrs='r_forearm'
            print('R Forearm')

        elif right_btn_ur==1:
            addrs='r_elbow'
            print('R Elbow')

        elif right_thmb==1:
            addrs='r_chest'
            print('R Chest')

        elif right_trig_btn==1:
            addls=None
            print('Right wrist')
            client.publish('joys_ctl/right_wrist',str(right_y))

        elif right_hat_up[1]==1:
            addrs='neck'
            print('Neck')


        if left_y<0:
            l_speed_val=-left_y
            l_direction='cw'

        elif left_y>0:
            l_speed_val=left_y
            l_direction='ccw'

        elif right_y==0:
            l_speed_val=0
            l_direction='stp'

        # print('Left X: ',left_x,' Left Y: ',left_y,' Right Y: ',right_y)
        if left_btn_dl==1:
            addls='l_arm'
            print('L Arm')

        elif left_btn_dr==1:
            addls='l_shoulder'
            print('L Shoulder')

        elif left_btn_ul==1:
            addls='l_forearm'
            print('L Forearm')

        elif left_btn_ur==1:
            addls='l_elbow'
            print('L Elbow')

        elif left_thmb==1:
            addls='l_chest'
            print('L Chest')

        elif right_hat_r[1]==-1:
            print('Head servo')
            client.publish('joys_ctl/head_servo',str(right_y))

        elif left_trig_btn==1:
            addls=None
            addrs=None
            print('Left Wrist')
            client.publish('joys_ctl/left_wrist',str(left_y))

        if(addls !=None):
            send_cmd(addls,l_direction,map(l_speed_val),'left')
            addls=None
            addrs=None

        if(addrs !=None):
            send_cmd(addrs,r_direction,map(r_speed_val),'right')
            addrs=None
            addls=None
        # else:
        #     stop_all()