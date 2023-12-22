from django.shortcuts import render

from .models import *

# Create your views here.
def get_policySvcMain(request):
    return render(request,'policySvcMain.html')

def get_privateMain(request):
    return render(request,'privateMain.html')

def get_MainTest(request):
    return render(request,'main.html')


def test(request):
    if request.method == 'POST':
        image = request.FILES.get('camera-image')
        CameraImage.objects.create(image=image)
    images = CameraImage.objects.all()
    context = {
        'images':images
    }
    return render(request, 'main.html', context)

def indexcss(request):
    return render(request, 'index.html')


from django.http import StreamingHttpResponse
from .camera import *

#Display the 2 videos
def index(request):
    return render(request, 'cvtest.html')

#Every time you call the phone and laptop camera method gets frame
#More info found in camera.py
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#Method for laptop camera
def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
                    #video type
					content_type='multipart/x-mixed-replace; boundary=frame')

#Method for phone camera
def webcam_feed(request):
	return StreamingHttpResponse(gen(IPWebCam()),
                    #video type
					content_type='multipart/x-mixed-replace; boundary=frame')

