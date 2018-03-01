import picamera
import picamera.array
import time
from threading import Thread, Lock


def main():
    global camera, stream
    camera = picamera.PiCamera()
    camera.resolution = (224, 224)
    camera.framerate = 30
    time.sleep(2)
    stream = picamera.array.PiRGBArray(camera)
    Thread(target=capture).start()


def capture():
    for _ in camera.capture_continuous(stream, 'bgr'):
        Thread(target=image).start()


def image():
    output = stream.array
    print output.shape
    stream.truncate(0)


if __name__ == '__main__':
    main()
