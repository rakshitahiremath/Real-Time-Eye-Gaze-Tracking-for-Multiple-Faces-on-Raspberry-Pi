# Real-Time-Eye-Gaze-Tracking-for-Multiple-Faces-on-Raspberry-Pi
This project is entirely set up on Raspberry Pi-3 model
## Requirements:
* Raspberry Pi 3 model B
* USB webcam


## Installations:
* Numpy
* cv2
* pymongo
* Mediapipe (Using Mediapipe, I was able to detect multifaces in the frame in real time.)
* Dlib( Click [here](https://youtu.be/uF4aDdxBm_M) to know how I installed Dlib on Raspberry Pi )
* imutils

### Set-up : 
1. Go to [MongoDB](https://cloud.mongodb.com/) and configure a MongoDB Atlas cluter running, Setup the MongoDB cluster and copy the URI. ([Procedure](https://www.mongodb.com/docs/atlas/getting-started/))
2. create **var.py**  file in the root folder and create variable DB and paste your MongoDB URI


```javascript
 DB = YOUR_URI_WITH_QUOTES
```


### Mediapipe gives 468 facial landmarks. To locate iris posistion,it is required to note down the eye landmarks.

![image](https://user-images.githubusercontent.com/59859182/178719145-e697ab6a-0538-4f7a-9c3f-733059c036df.png)
<sub>[Image from Mediapipe](https://google.github.io/mediapipe/solutions/iris)</sub>

On running the python file given in this repositry on Raspberry Pi with USB Webcam connected,I was able to 
detect the face and eye landmarks. Also detects the Iris position (tells whether the person is looking at center,right or left).
Along with this, it also determines the number of people in the frame.


The number of faces in the frame will be logged on to the database every 5 seconds.
#### Image 1- since there is no faces detected in the frame, the total number of faces is zero.
<img src="https://user-images.githubusercontent.com/59859182/178708001-00b021f8-5034-441c-8e80-35cce4dd24df.jpg" width="800" height="400"/>

#### Image 2- Below is the output in a scenario where there is only one face detected in the frame.
<img src="https://user-images.githubusercontent.com/59859182/178714480-1a30efd1-d725-4835-a78a-d145f30fa4a5.jpg" width="800" height="400"/>




Referneces:
[Extracted code snippet from here](https://github.com/Asadullah-Dal17/iris-Segmentation-mediapipe-python)
[Ai Phile](https://aiphile.blogspot.com/)
