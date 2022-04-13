import os
from cv2 import cv2


def convert_to_peat(address_in):
    # PEAT ONLY WORKS WITH UNCOMPRESSED 1024x768 30FPS AVI VIDEOS
    address_out = os.path.splitext(address_in)[0]+'.avi'
    writer = cv2.VideoWriter(address_out, 0, 30, (1024, 768))
    capture = cv2.VideoCapture(address_in)
    while True:
        check, frame = capture.read()
        if not check:
            break
        frame2 = cv2.resize(frame, (1024, 768))
        writer.write(frame2)
    writer.release()
