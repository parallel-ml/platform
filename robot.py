import picamera
import picamera.array
import time
from threading import Thread, Lock
import io
import numpy as np


def main():
    camera = picamera.PiCamera()
    camera.resolution = (224, 224)
    camera.framerate=30
    streams = [io.BytesIO() for i in range(30)]
    time.sleep(2)
    start = time.time()
    camera.capture_sequence(streams, format='rgb', use_video_port=True)
    streams = [s.getvalue() for s in streams]
    print (time.time() - start)

    for bytestring in streams:
        image = np.frombuffer(bytestring, dtype=np.uint8)
        print image.shape


if __name__ == '__main__':
    main()
