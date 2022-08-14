from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from flask import Flask, render_template, Response
from tensorflow.keras.models import load_model
import paho.mqtt.client as mqtt
import thermal_cam as tc
from cv2 import cv2
import numpy as np
import threading
import time
import math
import os

app = Flask( __name__ )
temperature=0
##########################################################################################################
username='admin'
password='ingnepal123'
ip='192.168.10.222'
resource='/Streaming/channels/101/httppreview'

# cam_url='http://admin:ingnepal123@192.168.10.222/Streaming/channels/101/httppreview'
cam_url='http://'+username+':'+password+'@'+ip+resource

# cam_url='rtsp://admin:ingnepal123@192.168.10.222/Streaming/channels/101/'

broker='localhost'
client=mqtt.Client('client1')
client.will_set('conn/disconnected','1')
##########################################################################################################
vs=cv2.VideoCapture()
#for rtsp
# valH=100
# valW=400
#for http
valH=100
valW=200

##########################################################################################################
cam_conn_sts=False
run=True
reading=False
frame_rd=None

##########################################################################################################
stream=True
stream_frame=None
stream_frame_encoded=None
##########################################################################################################

prototxt_path = os.path.sep.join(['models', 'deploy.prototxt'])
face_model_path = os.path.sep.join(['models','res10_300x300_ssd_iter_140000.caffemodel'])
mask_model_path=os.path.sep.join(['models','my.model'])

face_net=cv2.dnn.readNetFromCaffe(prototxt_path,face_model_path)
mask_net = load_model(mask_model_path)

tick_icon=os.path.sep.join((['assets','tick.png']))
cross_icon=os.path.sep.join((['assets','cross.png']))
tick=cv2.imread(tick_icon)
cross=cv2.imread(cross_icon)

# tick=cv2.resize(tick,(100,100))
# cross=cv2.resize(cross,(100,100))
tick_cross_sq_size=50

tick=cv2.resize(tick,(tick_cross_sq_size,tick_cross_sq_size))
cross=cv2.resize(cross,(tick_cross_sq_size,tick_cross_sq_size))
##########################################################################################################
conf=0.5
diag=220
scan_time=1

predecting=False
mask_result=None
mask_pred=None
##########################################################################################################
while not cam_conn_sts:
    try:
        cam_conn_sts=vs.open(cam_url,cv2.CAP_FFMPEG)
    except:
        print('Error checking conn sts')
        cam_conn_sts=False
    print('Connection status : ',cam_conn_sts)
    time.sleep(0.5)


get_frame_shape=False
while(not get_frame_shape):
    ret,fr=vs.read()
    if ret:
        h,w=(fr.shape[0],fr.shape[1])
        fstartY=valH
        fendY=h-valH
        fstartX=valW
        fendX=w-valW
        get_frame_shape=True
    else:
        print('Waiting to get frame  shape')
        time.sleep(1)

##########################################################################################################
def gen():
    while True:
        global stream_frame_encoded
        if stream_frame_encoded is not None:
            try:
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream_frame_encoded + b'\r\n\r\n')
            except:
                yield(print('Error streaming'))


@app.route('/')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def init_stream_server():
    global app
    app.run( host = '0.0.0.0', port = '5000' )

stream_server = threading.Thread( target = init_stream_server, daemon = True )
stream_server.start()

def encode_frame():
    global stream_frame_encoded
    while run:
        if stream_frame is not None:
            ret, jpeg = cv2.imencode('.jpg', stream_frame)
            stream_frame_encoded=jpeg.tobytes()
        else:
            time.sleep(1)

encoding_thr=threading.Thread(target=encode_frame,daemon=True)
encoding_thr.start()
##########################################################################################################

def get_tempr():

    global temperature
    for t in tc.connect():
        temperature=int(t)

tempr_thr=threading.Thread(target=get_tempr,daemon=True)
tempr_thr.start()
##########################################################################################################
mq_mask_result_tmpr='mask_result_tmpr'
mq_stream_ctl='streaming'

def on_log(client,userdata,level,buf):
    print('log: '+buf)

def on_connect(client,userdata,flags,rc):
    print("Connected with result code "+str(rc))
    client.subscribe('cmd/exit')


def on_message(client, userdata, msg):
    global run
    if msg.topic=='cmd/exit':
        run=False

def stream_controller():
    global stream
    c=0
    d=0
    while run:
        if stream:
            if(c<5):
                client.publish(mq_stream_ctl,'1')
                c=c+1
                d=0
        else:
            if(d<5):
                client.publish(mq_stream_ctl,'0')
                d=d+1
                c=0
        time.sleep(0.1)

stream_ctlr_thr=threading.Thread(target=stream_controller,daemon=True)
stream_ctlr_thr.start()


def client_loop():
	global client
	while run:
		client.loop()

cl_loop_thr=threading.Thread(target=client_loop,daemon=True)
cl_loop_thr.start()


client.on_connect=on_connect
client.on_log=on_log
client.on_message = on_message
client.connect(broker)

##########################################################################################################

def no_prediction():
    global predecting,mask_pred,mask_result
    predecting=False
    mask_result=None
    mask_pred=None

def read_feed():
    global frame_rd,reading
    while run:
        try:
            ret,frame_r=vs.read()
            if(ret):
                frame_rd=frame_r[fstartY:fendY,fstartX:fendX]
                reading=True
            else:
                reading=False
        except:
            print('Unable to get feed')
read_feed_thr=threading.Thread(target=read_feed,daemon=True)
read_feed_thr.start()

def detect_face(frame):
    chk_locs=[]
    nchk_locs=[]
    h,w= frame.shape[:2]
    # blob=cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)),1.0,(300,300),(104.0,177.0,123.0)) #preprocessing Image
    blob=cv2.dnn.blobFromImage(frame,1.0,(300,300),(104.0,177.0,123.0)) #preprocessing Image
    face_net.setInput(blob)
    detections=face_net.forward()
    num_face=0
    for i in range(0,detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf:
            num_face=num_face+1
            box=detections[0,0,i,3:7]*np.array([w,h,w,h])
            (startX,startY,endX,endY)=box.astype('int')

            startX=startX-20
            startY=startY-30
            endX=endX+20
            endY=endY+40

            startX=1 if startX<0 else startX
            startX=w if startX>w else startX

            startY=1 if startY<0 else startY
            startY=h if startY>h else startY

            endX=1 if endX<0 else endX
            endX=w if endX>w else endX

            endY=1 if endY<0 else endY
            endY=h if endY>h else endY


            diag_len=int(math.sqrt((endX-startX)**2+(endY-startY)**2))
            if diag_len>=diag:
                chk_locs.append((i,confidence,startX,startY,endX,endY))
            else:
                nchk_locs.append((i,confidence,startX,startY,endX,endY))
    return (chk_locs,nchk_locs)

def predict_mask(frame,chk_locs):
    i,confidence,startX,startY,endX,endY=chk_locs[0]
    face = frame[startY:endY,startX:endX]
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = img_to_array(face)
    face = preprocess_input(face)
    face = np.expand_dims(face, axis=0)
    preds=mask_net.predict(face)
    return preds

def draw_rects(frame,locs,color=None):
    global mask_result,tick,cross,temperature,stream_frame,stream
    frame=frame.copy()
    for box in locs:
        i,confidence,startX,startY,endX,endY=box
        if mask_result==True:       #wearing mask
            color=(0,255,0)
            frame[endY-tick_cross_sq_size:endY,endX-tick_cross_sq_size:endX,:]=tick[:,:,:]
            client.publish(mq_mask_result_tmpr,'1'+','+str(temperature))

        elif mask_result==False:       #Not wearing mask
            color=(0,0,255)
            frame[endY-tick_cross_sq_size:endY,endX-tick_cross_sq_size:endX,:]=cross[:,:,:]
            client.publish(mq_mask_result_tmpr,'0'+','+str(temperature))
            
        elif mask_result==None and color==None:     #Scanning
            color=(0,255,255)
            if predecting==True and mask_result==None:
                pass
        cv2.rectangle(frame,(startX,startY),(endX,endY),color,2)
        cv2.imshow('Detections',frame)
        stream=True
        stream_frame=frame
    return True


def watcher():
    global run,predecting,mask_result,mask_pred,scan_time
    while run:
        if predecting:
            mrt=0
            mrf=0
            start_time=time.perf_counter()
            while run and predecting:
                if mask_pred:
                    mrt=mrt+1
                else:
                    mrf=mrf+1
                if time.perf_counter()>start_time+scan_time:
                    mask_result=True if mrt>mrf else False
                    if mask_result:
                        print('The person is wearing mask : ',temperature)
                    elif not mask_result:
                        print('The person is not wearing mask : ',temperature)

                    while run and predecting:
                        mask_result=mask_pred
                        time.sleep(0.1)
                    break
                else:
                    time.sleep(0.1)
        else:
            time.sleep(0.1)

watcher_thr=threading.Thread(target=watcher,daemon=True)
watcher_thr.start()

while run:
    if reading:
        frame=frame_rd
        chk_locs,nchk_locs=detect_face(frame)
        if len(chk_locs)+len(nchk_locs)>0:
            # stream=True
            if len(nchk_locs)>0:    #Drawing the faces outide the range
                no_prediction()
                stream=False
                # draw_rects(frame,nchk_locs,color=(145,50,170))

            if len(chk_locs)==1:    #Predicting whenever there is only one face within the range
                predecting=True
                preds=predict_mask(frame,chk_locs)
                mask,without_mask=preds[0]
                mask_pred = True if mask > without_mask else False
                draw_rects(frame,chk_locs)

            elif len(chk_locs)>1:   #Drawing if multiple faces within the range
                no_prediction()
                stream=False
                # cv2.putText(frame,'Multiple faces or too close',(100,100),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,255),2)
                # cv2.imshow('Detections',frame)
                print('Multiple faces inside the range. Num. of faces = ',len(chk_locs))
        else:
            stream=False
            no_prediction()
            cv2.imshow('Detections',frame)
            time.sleep(0.1)

        if cv2.waitKey(1) & 0XFF==ord('q'):
            run=False
            break
    else:
        time.sleep(1)
        print('Waiting')

read_feed_thr.join()
vs.release()
cv2.destroyAllWindows()