# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 09:46:46 2016

Sample for tisgrabber to OpenCV Sample 2

Open a camera by name
Set a video format hard coded (not recommended, but some peoples insist on this)
Set properties exposure, gain, whitebalance
"""
import sys
import os

PACKAGE_PARENT = '.'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
DB_DIR = SCRIPT_DIR
indentLevel = 1
for i in range(indentLevel):
    DB_DIR = os.path.split(DB_DIR)[0]
sys.path.append(os.path.normpath(os.path.join(PACKAGE_PARENT,SCRIPT_DIR)))
sys.path.append(os.path.normpath(DB_DIR))
print(sys.path)

import ctypes as C
import tisgrabber as IC
import cv2
import numpy as np

lWidth=C.c_long()
lHeight= C.c_long()
iBitsPerPixel=C.c_int()
COLORFORMAT=C.c_int()

class ImageSourceCam:
    def __init__(self):
        self.cam = IC.TIS_CAM()
    
    def open(self):
        # List availabe devices as uniqe names. This is a combination of camera name and serial number
        Devices = self.cam.GetDevices()
        cam = None
        for dev in Devices:
            cam = dev.decode('utf-8')
            break
        self.cam.open(cam)
    
    def config(self):
        if self.cam.IsDevValid() == 1:
            #cv2.namedWindow('Window', cv2.cv.CV_WINDOW_NORMAL)
            print( 'Press ctrl-c to stop' )

            # Set a video format
            self.cam.SetVideoFormat("RGB32 (4000x3000)")
            
            #Set a frame rate of 30 frames per second
            self.cam.SetFrameRate( 30.0 )   

            # Set some properties
            # Exposure time

            ExposureAuto=[1]
            
            self.cam.GetPropertySwitch("Exposure","Auto",ExposureAuto)
            print("Exposure auto : ", ExposureAuto[0])

            
            # In order to set a fixed exposure time, the Exposure Automatic must be disabled first.
            # Using the IC Imaging Control VCD Property Inspector, we know, the item is "Exposure", the
            # element is "Auto" and the interface is "Switch". Therefore we use for disabling:
            self.cam.SetPropertySwitch("Exposure","Auto",0)
            # "0" is off, "1" is on.

            ExposureTime=[0]
            self.cam.GetPropertyAbsoluteValue("Exposure","Value",ExposureTime)
            print("Exposure time abs: ", ExposureTime[0])

            
            # Set an absolute exposure time, given in fractions of seconds. 0.0303 is 1/30 second:
            self.cam.SetPropertyAbsoluteValue("Exposure","Value",0.0303)

            # Proceed with Gain, since we have gain automatic, disable first. Then set values.
            Gainauto=[0]
            self.cam.GetPropertySwitch("Gain","Auto",Gainauto)
            print("Gain auto : ", Gainauto[0])
            
            self.cam.SetPropertySwitch("Gain","Auto",0)
            self.cam.SetPropertyValue("Gain","Value",10)

            WhiteBalanceAuto=[0]
            # Same goes with white balance. We make a complete red image:
            self.cam.SetPropertySwitch("WhiteBalance","Auto",1)
            self.cam.GetPropertySwitch("WhiteBalance","Auto",WhiteBalanceAuto)
            print("WB auto : ", WhiteBalanceAuto[0])

            self.cam.SetPropertySwitch("WhiteBalance","Auto",0)
            self.cam.GetPropertySwitch("WhiteBalance","Auto",WhiteBalanceAuto)
            print("WB auto : ", WhiteBalanceAuto[0])
            
            self.cam.SetPropertyValue("WhiteBalance","White Balance Red",64)
            self.cam.SetPropertyValue("WhiteBalance","White Balance Green",64)
            self.cam.SetPropertyValue("WhiteBalance","White Balance Blue",64)

    def start(self):
        # Start the live video stream, but show no own live video window. We will use OpenCV for this.
        self.cam.StartLive(0) 

    def snap(self):
        # Snap an image
        self.cam.SnapImage()
        # Get the image
        image = self.cam.GetImage()
        # Apply some OpenCV function on this image
        image = cv2.flip(image,0)
        image = cv2.erode(image,np.ones((11, 11)))
        return image
    
    def close(self):
        self.cam.StopLive()
    
    
 
  