import cv2 as cv
import numpy as np
import mediapipe as mp
import math
import dlib

from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import datetime
from pymongo import MongoClient
import certifi
ca=certifi.where()
# creation of MongoClient
client=MongoClient()
  
# Connect with the portnumber and host
client = MongoClient('mongodb://root:root@ac-ggutrlf-shard-00-00.ltueshq.mongodb.net:27017,ac-ggutrlf-shard-00-01.ltueshq.mongodb.net:27017,ac-ggutrlf-shard-00-02.ltueshq.mongodb.net:27017/?ssl=true&replicaSet=atlas-osry5t-shard-0&authSource=admin&retryWrites=true&w=majority',tls=True, tlsAllowInvalidCertificates=True)
db=client.eye
data=db.log
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)


mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398 ]
RIGHT_EYE = [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246 ]
RIGHT_IRIS = [474, 475, 476, 477]
LEFT_IRIS = [469, 470, 471, 472]
L_H_LEFT = [33] # RIGHT EYE RIGHT MOST LANDMARK
L_H_RIGHT = [133] #RIGHT EYE LEFT MOST LANDMARK
R_H_LEFT = [362] #LEFT EYE RIGHT MOST LANDMARK
R_H_RIGHT = [263] #LEFT EYE LEFT MOST LANDMARK

def euclidean_distance(point1,point2):
    x1,y1 = point1.ravel()
    x2,y2 = point2.ravel()
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance


def iris_position(iris_center, right_point, left_point):
    center_to_right_dist = euclidean_distance(iris_center,right_point)
    total_distance = euclidean_distance(right_point,left_point)
    ratio = center_to_right_dist/total_distance
    iris_position =""
    if ratio <= 0.42:
        iris_position ="Right"
    elif ratio > 0.42 and ratio <= 0.57:
        iris_position = "Center"
    else:
        iris_position = "Left"
    return iris_position, ratio

#cap = cv.VideoCapture(1)

detector = dlib.get_frontal_face_detector()

with mp_face_mesh.FaceMesh(
    max_num_faces=10,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:
    while True:
        
            #ret, frame = cap.read()
            #if not ret:
                #break            
            #frame = cv.flip(frame,1)
           # _, frame = cap.read()
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            timestamp = datetime.datetime.now()
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            cv.putText(frame, ts, (10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
            
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = detector(gray)
            i=0
            c=0
            average = 0
            people_count_prev = 0
            weight = 0.99
            if len(faces) == 0:
               c = 0
               now=datetime.datetime.now()
               curr_time=now.strftime("%S")
               if int(curr_time)%5==0:
                    di={"average":0,"time":now.strftime("%H:%M:%S")}
                    data.insert_one(di)
                    print("success")
               print('total number of faces is zero!')
            for face in faces:
                x,y=face.left(),face.top()
                height,width=face.right(),face.bottom()
                cv.rectangle(frame,(x,y),(height,width),(0,0,255),2)
                i=i+1
                c=i
                average = weight*c + (1-weight)*people_count_prev
                print("Total number of faces = ",average)
                people_count_prev = average
               
                cv.putText(frame,'face'+str(i),(x-12,y-12),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
                now=datetime.datetime.now()
                curr_time=now.strftime("%S")
                
                if int(curr_time)%5==0:
                    di={"average":average,"time":now.strftime("%H:%M:%S")}
                    data.insert_one(di)
                    print("success")
                
                              
                                  
            
            rgb_frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            img_h,img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            if results.multi_face_landmarks:
                #print(results.multi_face_landmarks[0].landmark)
                mesh_points = np.array([np.multiply([p.x, p.y],[img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
                #print(mesh_points.shape)
                #cv.polylines(frame, [mesh_points[LEFT_EYE]],True, (0,255,0),1,cv.LINE_AA)
                #cv.polylines(frame, [mesh_points[RIGHT_EYE]],True, (0,255,0),1,cv.LINE_AA)
                (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype= np.int32)
                center_right = np.array([r_cx, r_cy], dtype= np.int32)
                cv.circle(frame, center_left, int(l_radius), (255,0,255), 1, cv.LINE_AA)
                cv.circle(frame, center_right, int(r_radius), (255,0,255), 1, cv.LINE_AA)
                cv.circle(frame,mesh_points[R_H_RIGHT][0], 3,(255, 255, 255), -1, cv.LINE_AA)
                cv.circle(frame,mesh_points[R_H_LEFT][0], 3,(0, 255, 255), -1, cv.LINE_AA)
                
                iris_pos,ratio = iris_position(
                    center_right, mesh_points[R_H_RIGHT], mesh_points[R_H_LEFT][0]
                    )
                #print(iris_pos)
                cv.putText(frame,
                           f"Iris pos: {iris_pos} {ratio: .2f}",
                           (30,30),
                           cv.FONT_HERSHEY_PLAIN,
                           1.2,
                           (0,255,0),
                           1,
                           cv.LINE_AA,)
    
            #cv.imshow('img',frame)
            key = cv.waitKey(1)
            if key == ord('q'):
                break


cap.release()
cv.destroyAllWindows()
vs.stop()
