from camera import camera
from threading import Thread, Event
import sys, termios, tty, os, time
from easygopigo3 import EasyGoPiGo3
from multiprocessing import Queue


def key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def robot(stop):
    while not stop.is_set():
        signal = control_queue.get()
        if signal == 'w':
            gpg3.forward()
        elif signal == 's':
            gpg3.backward()
        elif signal == 'a':
            gpg3.left()
        elif signal == 'd':
            gpg3.right()
        time.sleep(0.1)
        if control_queue.qsize() <= 0:
            gpg3.stop()
        

def main():
    # start the camera
    stop_camera = Event()
    camera_thread = Thread(target=camera, args=(stop_camera,))
    camera_thread.start()
    
    global gpg3, control_queue
    gpg3 = EasyGoPiGo3()
    gpg3.set_speed(180)
    control_queue = Queue()

    stop_robot = Event()
    robot_thread = Thread(target=robot, args=(stop_robot,))
    robot_thread.start()
    prev_signal = ' '
    
    while True:
        signal = key()

        if signal == 'q':
            break
        elif control_queue.qsize() <= 0 or prev_signal != signal:
            prev_signal = signal
            control_queue.put(signal)

    # stop everything
    stop_camera.set()
    stop_robot.set()
    exit()

if __name__ == '__main__':
    main()
