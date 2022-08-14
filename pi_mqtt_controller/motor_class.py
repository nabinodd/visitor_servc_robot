from gpiozero import DigitalInputDevice
from smbus2 import SMBus
import threading
import time

class MotorNode(SMBus):

    def __init__(self,addr,pin_o,name):
        self.addr=int(addr)
        self.name=name
        self.sent=False
        self.gpin=pin_o
        self.pin_st=0
        self.data=[]
        self.bus=SMBus(1)


    def send_data_to_i2c(self,reg,pos='000'):
        if len(pos)==1:
            pos='0'+'0'+pos
        elif len(pos)==2:
            pos='0'+pos
        pos_bytes=bytearray(pos,'ascii')
        try:
            self.bus.write_block_data(self.addr,reg,pos_bytes)
            time.sleep(0.5)
            print('Sent : ',self.addr,' ',reg,' ',pos )
            self.sent=True
        except:
            print('Cannot send to : ',self.addr)
            self.sent=False
        return self.sent

    def request_data_from_i2c(self,lenn=4):
        self.data=[]
        try:
            self.data=self.bus.read_i2c_block_data(self.addr,22,4)
            time.sleep(0.1)
        except:
            print('Cannot query data from : ',self.addr)

        if len(self.data)>0:
            return self.data
        else:
            return None

    def get_ack(self,data):
        if(data==None):
            return None

        reg=data[0]
        pos=[]
        for i in range(1,3):
            if(data[i])!=0:
                pos.append(data[i])

        # pos = [data[1],data[2]]

        position=''.join(map(chr,pos))

        if reg==11:
            return ('pos,'+str(position))

        elif reg==44:
            return 'init,0'

        elif reg==77:
            return('err,'+str(position))

        elif reg==33:
            return('enc,'+str(position))

        else:
            print('Received data : ',data)
            return None

    def check_init(self,blocking=False):    #checks whether the motor is init or not, returns bool
        while(blocking and self.gpin.value==0):
            print('Waiting for init')
            time.sleep(0.5)
        if(self.gpin.value==1):
            self.request_data_from_i2c()
            ack=self.get_ack(self.data)
            if ack!=None:
                ack_sep=ack.split(',')
                if ack_sep[0]=='init':
                    time.sleep(0.1)
                    return True
                else:
                    time.sleep(0.1)
                    return False
        else:
            return False

    def check_pos_ack(self,blocking=False):  #checks pos, returns pos or None
        while(blocking and self.gpin.value==0):
            print('Waiting for pos ack')
            time.sleep(0.5)  #here 1----------------------
        if(self.gpin.value==1):
            if self.request_data_from_i2c()!=None:
                ack=self.get_ack(self.data)
                if ack!=None:
                    ack_sep=ack.split(',')
                    if ack_sep[0]=='pos':
                        time.sleep(0.1)
                        return ack_sep[1]
                    else:
                        time.sleep(0.1)
                        return None
        else:
            time.sleep(0.1)
            return None

    def rotate_to_pos(self,pos,blocking=False):  #rotates to target pos, returns bool
        if self.check_ack_pin():
            self.send_data_to_i2c(1,str(pos))
            time.sleep(0.5)
            r=self.check_pos_ack(blocking=blocking)
            if r!=None:
                response=int(r)
                if(response>pos-1 and response<pos+1):
                    return True
                else:
                    return False
            else:
                return False
        else:
            print(self.name,' busy, cannot release ack line')
            return False

    def check_ack_pin(self):
        c=0
        if self.gpin.value==1:
            while True:
                self.send_data_to_i2c(55)
                c=c+1
                time.sleep(0.5)
                if self.gpin.value==0:
                    return True
                if c>5:
                    print('Cannot release ack pin of : ',self.name)
                    return False

        elif self.gpin.value==0:
            return True


    def send_init(self):
        if self.check_ack_pin():
            self.send_data_to_i2c(4)
            time.sleep(0.5)
            return True
        else:
            print(self.name,' busy, cannot send init')
            return False
