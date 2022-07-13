# Real-Time-Eye-Gaze-Tracking-for-Multiple-Faces-on-Raspberry-Pi
This project is entirely set up on Raspberry Pi-3 model
## Requirements:
* Raspberry Pi 3 model B
* USB webcam

## Installations:
* Numpy
* cv2
* Mediapipe (Using Mediapipe, I was able to detect multifaces in the frame in real time.)
* Dlib( Click [here](https://youtu.be/uF4aDdxBm_M) to know how I installed Dlib on Raspberry Pi )
* imutils

On running the python file given in this repositry on Raspberry Pi with USB Webcam connected,I was able to 
detect the face and eye landmarks. Also detects the Iris position (tells whether the person is looking at center,right or left).
Along with this, it also determines the number of people in the frame.


The number of faces in the frame will be logged on to the database every 5 seconds.
#### Image 1- since there is no faces detected in the frame, the total number of faces is zero.
<img src="https://user-images.githubusercontent.com/59859182/178708001-00b021f8-5034-441c-8e80-35cce4dd24df.jpg" width="800" height="400"/>

#### Image 2- Below is the output in a scenario where there is only one face detected in the frame.
<img src="https://user-images.githubusercontent.com/59859182/178712465-451bd7e7-2d1b-466c-b819-b9b99a1ac725.jpg" width="800" height="400"/>




Referneces:
[Ai Phile](https://aiphile.blogspot.com/)
