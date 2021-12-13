import time
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# Allow the camera to warmup
time.sleep(0.1)

# Grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# Display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)
