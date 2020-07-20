"""
OpenCV Motion Detection with GUI
@authors: Menelaos M.(menmad00) and Emmanouil K.

Description: It is a Python Script for Motion Detection utilizing OpenCV-python package with built-in GUI that offers various functions to user.
If a motion is large enough to be detected (adjustable) the user is notified both with a popup window showing the motion and with a sound effect.
"""
# importing OpenCV, time, winsound and threading library 
import cv2
import time
import winsound
import threading


def alertBySound():
    winsound.Beep(5000,1000)
    #winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    #winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    return

# Parameters
background = cv2.imread("background.jpg")
window_name = 'MDC'
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
color = (255, 0, 0) 
thickness = 1
sensitivityUpper = 10
sensitivityBottom = 1
sensitivityStart = 2
CONTOUR_AREA = 10000

# Controller
soundC = False
videoC = False
muteC = False
forceShowC = False
showFor = 1
sensitivity = sensitivityStart

# Capturing video 
video = cv2.VideoCapture(0) 

static_back = None
motionDetected = False
startTime = 0
elapsedTime = time.time()

# Infinite while loop to treat stack of image as video 
while True: 
    # Reading frame(image) from video 
    check, frame = video.read()
    frameExcMotion = frame.copy()
    
    # Controller
    image = background.copy()

    y = 20
    increase = 23

    org = (10, y)
    if(not muteC):
        image = cv2.putText(image, 'Mute (Off): Space', org, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        image = cv2.putText(image, 'Mute (On): Space', org, font, fontScale, color, thickness, cv2.LINE_AA)

    y = y + increase
    org = (10, y)
    if(not forceShowC):
        image = cv2.putText(image, 'Stream (Off): F', org, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        image = cv2.putText(image, 'Stream (On): F', org, font, fontScale, color, thickness, cv2.LINE_AA)

    y = y + increase
    org = (10, y) 
    if(not soundC):
        image = cv2.putText(image, 'Sound (Off): S', org, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        image = cv2.putText(image, 'Sound (On): S', org, font, fontScale, color, thickness, cv2.LINE_AA)

    y = y + increase
    org = (10, y) 
    if(not videoC):
        image = cv2.putText(image, 'Video (Off): V', org, font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        image = cv2.putText(image, 'Video (On): V', org, font, fontScale, color, thickness, cv2.LINE_AA)

    y = y + increase
    org = (10, y) 
    image = cv2.putText(image, 'Show for ' + str(showFor) + 's : [1-10]', org, font, fontScale, color, thickness, cv2.LINE_AA)

    y = y + increase
    org = (10, y)
    image = cv2.putText(image, 'Sensitivity ' + str(int(sensitivity*10)) + ': +/-', org, font, fontScale, color, thickness, cv2.LINE_AA)

    y = y + increase
    org = (10, y)
    image = cv2.putText(image, 'Exit: Q', org, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow(window_name, image)
    # End Of Controller
    
    # Converting color image to gray_scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Converting gray scale image to GaussianBlur 
    # so that change can be find easily 
    gray = cv2.GaussianBlur(gray, (21, 21), 0)     
    
    if static_back is None: 
        static_back = gray
        continue
    # Difference between static background 
    # and current frame(which is GaussianBlur) 
    diff_frame = cv2.absdiff(static_back, gray) 
    

    # If change in between static background and 
    # current frame is greater than 30 it will show white color(255) 
    thresh_frame = cv2.threshold(diff_frame, sensitivity, 255, cv2.THRESH_BINARY)[1] 
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) 

    # Finding contour of moving object 
    (cnts, _) = cv2.findContours(thresh_frame.copy(), 
					cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
    for contour in cnts:
        if cv2.contourArea(contour) < CONTOUR_AREA: 
            continue
        if( not motionDetected):
            motionDetected = True
            startTime = time.time()
        else:
            startTime = time.time()
        (x, y, w, h) = cv2.boundingRect(contour) 
		# making green rectangle arround the moving object 
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    if muteC:
        motionDetected = False
   
    if motionDetected:
        if(videoC):
            cv2.imshow("Motion", frame)
        if(soundC):
            thread = threading.Thread(target=alertBySound)
            thread.start()
        elapsedTime = time.time()
        if(elapsedTime - startTime > showFor):
            motionDetected = False

    if forceShowC and not muteC:
        cv2.imshow("Stream", frameExcMotion)
    else:
        cv2.destroyWindow("Stream")


    if not motionDetected or not videoC:
        cv2.destroyWindow("Motion")
        
    key = cv2.waitKey(1)
    if key == ord(' '):
        muteC = not muteC
    if key == ord('f'):
        forceShowC = not forceShowC
    if key == ord('s'):
        soundC = not soundC
    if key == ord('v'):
        videoC = not videoC
    if key in range(ord('0'), ord('9')+1):
        showFor = key-ord('0')
        if showFor==0:
            showFor = 10
    if key == ord('+'):
        sensitivity = sensitivity + 0.1
        if sensitivity > sensitivityUpper:
            sensitivity = sensitivityUpper
    if key == ord('-'):
        sensitivity = sensitivity - 0.1
        if sensitivity < sensitivityBottom:
            sensitivity = sensitivityBottom
    if key == ord('q'):
        exit()
    static_back = gray
    

video.release() 

# Destroying all the windows 
cv2.destroyAllWindows() 
