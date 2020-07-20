# Motion-Dection-with-built-in-GUI

It is a Python Script for Motion Detection utilizing OpenCV-python package with built-in GUI that offers various functions to user. If a motion is large enough to be detected (adjustable) the user is notified both with a popup window showing the motion and with a sound effect.

# Aditional Information

The main idea is to detect state change of some pixels between the current and previous frame when capturing video from a webcam. For this purpose, the absolute value of the difference between these two frames is calculated, then a threshold function is applied (to find pixels that have changed) and finally a square contour of the moving object is drawn. User has the ability to choose how to be notified when motion is detected. In gui one can find the options of video alert, audio alert, both video and audio alert, streaming video and mute. It is possible to modify the sensitivity, the video playing time during motion detection as well as the personalization of GUI environment by changing the background image.

# Dependencies

- Python 3
- Install opencv-python 4.3.0 (pip install opencv-python)
- Webcamera

# Run Motion Detector with GUI

Clone the repository and run the command python motion.py or pythonw motion.py in the project directory.

# Developers

Menelaos M. 
Emmanouil K.
