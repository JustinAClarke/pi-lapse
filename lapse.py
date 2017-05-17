#!/usr/bin/env python3

import time
from picamera import PiCamera

import configparser
import random
import os,sys

class piCameraLapse:
    def __init__(self):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read('config.ini')
        self.camera = False
        self.width = 1280
        self.height = 720
        self.location = "/tmp/images"
        self.delay = 8 #in seconds
        #time set in UTC
        self.startHour = 10
        self.startMinute = 0
        self.endHour = 11
        self.endMinute = 60
        
        self.debug = True
        self.getConfig()

    def getConfig(self):
        self.width = self.config['Camera'].getint('width',1280)
        self.height = self.config['Camera'].getint('height',720)

        self.startHour = self.config['Times'].getint('SHour',0)
        self.endHour = self.config['Times'].getint('EHour',0)

        self.startMinute = self.config['Times'].getint('SMinute',0)
        self.endMinute = self.config['Times'].getint('EMinute',0)

        self.delay = self.config['Times'].getint('Delay',0)

        self.location = self.config['General'].get('Location',0)
        pass

    def setConfig(self):
        with open('config.ini', 'w') as configfile:
           self.config.write(configfile)
        pass

    def printDebug(self,line):
        if(self.debug):
            print(line)
            
    def cameraon(self):
        if self.getCameraStatus() == False:
            self.printDebug("Camera On")
            #self.camera = PiCamera()
            #self.camera.led = False
            self.camera = "On"

    def cameraoff(self):
        if self.getCameraStatus():
            self.printDebug("Camera Off")
            #self.camera.close()
            self.camera = False

    def getCameraStatus(self):
        if self.camera == False:
            return False
        else:
            return True
        
    def capture(self):
        if(self.getCameraStatus()):
            if not os.path.exists(self.location):
                os.makedirs(self.location, mode=0o777)
            self.printDebug("Capture")
            #self.camera.resolution(self.width,self.height)
            time.sleep(2)
            file= "{}{}.jpg".format(self.location,time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()))
            self.printDebug("saveLoc {}".format(file))
            #camera.capture(file)
            
    def isTime(self):
        self.printDebug("istime")
        hour = int(time.strftime("%H",time.gmtime()))
        minute = int(time.strftime("%M",time.gmtime()))
        
        self.printDebug("Hour current:{} start:{} end:{}".format(hour,self.startHour,self.endHour))
        self.printDebug("Minute current:{} start:{} end:{}".format(minute,self.startMinute,self.endMinute))
    
        #sys.exit()
        if(
            self.startHour == 0 and
            self.endHour == 0 and
            self.startMinute == 0 and
            self.endMinute == 0
            ):
            return True
        if(
            hour >= self.startHour and
            hour <= self.endHour and
            minute >= self.startMinute and
            minute <= self.endMinute
            ):
            return True
        else:
            return False
        
#    def setConfig(self,config):
#        self.delay = config.delay
#        self.width = config.width
#        self.height = config.height
        
        
#        pass
    
    def loop(self):
        self.printDebug("Loop")
        while True:
            if(self.isTime()):
                self.printDebug("Loop Capture")
                self.printDebug("Sleep {} Seconds".format(self.delay))
                time.sleep(self.delay)
                self.cameraon()
                self.capture()
                self.cameraoff()
        
if __name__ == '__main__':
    app = piCameraLapse()
    app.setConfig()
    app.loop()
    pass
