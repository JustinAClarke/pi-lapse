#!/usr/bin/env python3

import time, os
from picamera import PiCamera
from datetime import datetime

from pathlib import Path


basepath = '/home/justinc/lapse_photos/'


if __name__ == '__main__':
    img_path = Path("{}/{}/".format(basepath,time.time()))
    img_path.mkdir(parents=True, exist_ok=True)
    while True:
        camera = PiCamera()
        camera.resolution='3280x2464'
        #take photo
        time.sleep(2)
        captureDate = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        camera.capture("{}/{}.jpg".format(img_path,captureDate))
        time.sleep(2)
        os.unlink("/home/justinc/latest.jpg")
        os.symlink("{}/{}.jpg".format(img_path,captureDate),  "/home/justinc/latest.jpg")
        camera.close()
        time.sleep(10)

