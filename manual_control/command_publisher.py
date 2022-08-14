import paho.mqtt.client as mqtt
import time

broker='192.168.2.35'
client=mqtt.Client('sim_publishzer')


def on_log(client,userdata,level,buf):
    print('log: '+buf)

def on_connect(client,userdata,flags,rc):
    if rc==0:
        pass
        # print('Connected OK')
    else:
        print('Not connected : ',rc)


client.on_connect=on_connect
# client.on_log=on_log

print('Connecting to broker : ',broker)
client.will_set('sim_publisher/connection','disconnected')
client.connect(broker)
client.loop_start()

# cmd='11,0,0,180,105'

def validate_cmd(addr,pos):

    if addr==0:
        print('Wrong Address : ',addr)
        return False
    else:
        return True

while True:
    time.sleep(1)
    # client.publish('robot_ctl/right/arm',cmd)
    addr=input('Addr : ')

    reg=input('Reg : ')
    if(reg=='1'):
        pos=input('Pos  : ')
    else:
        pos='000'

    if validate_cmd(int(addr),int (pos)):
        cmd=str(addr+','+reg+','+pos)
        client.publish('cmd_ctl',cmd)
        print('Command sent : ',cmd)