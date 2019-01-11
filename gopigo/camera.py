import picamera
import picamera.array
import time
import io


def camera(stop):
    """ Capture the real time image. """
    with picamera.PiCamera() as camera:
        camera.resolution = (224, 224)
        camera.framerate = 30

        # capture 30 frames per second
        streams = [io.BytesIO() for i in range(30)]

        # wait for camera to warm up
        time.sleep(2)

        while not stop.is_set():
            camera.capture_sequence(streams, format='rgb', use_video_port=True)
            bytestrings = [s.getvalue() for s in streams]
