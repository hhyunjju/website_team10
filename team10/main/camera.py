from imutils.video import VideoStream
import imutils
import cv2
import os
import urllib.request
import numpy as np
from django.conf import settings





class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()


    #This function is used in views
    def get_frame(self):

        success, image = self.video.read()
        frame_flip = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()



class IPWebCam(object):
    def __init__(self):
        self.url = "http://192.168.1.178:8080/shot.jpg"
        
        # self.output_folder = "captured_images"  # Specify the folder where you want to save the images

        # # Create the output folder if it doesn't exist
        # if not os.path.exists(self.output_folder):
        #     os.makedirs(self.output_folder)


    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        img =cv2.resize(img, (640, 480))
        frame_flip = cv2.flip(img, 1)
        
        # # Save the image to the output folder
        # 이미지 이름 변경 필요? 중복되지 않게?
        # image_filename = os.path.join(self.output_folder, "captured_image.jpg")
        # cv2.imwrite(image_filename, frame_flip)
        
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()