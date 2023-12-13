
# Write a program that can start and stop a media player (e.g. VLC) using hand gestures.
#
# The program should be able to detect the following hand gestures:
# - A "stop" gesture, which is a hand with all fingers extended and the palm facing the camera.
# - A "start" gesture, which is a hand with all fingers extended and the palm facing away from the camera.
#
# Code Starts Here
import HandTracking.HandTrackingModule as htm
import cv2
import time
import numpy as np
import math
import pyautogui
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def main():

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volMin, volMax = volume.GetVolumeRange()[:2]
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = htm.HandDetector()

    min_hand_size = 40
    max_hand_size = 225
    min_distance = 10
    max_distance = 100
    while True:
        success, img = cap.read()

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        img = detector.findHands(img)
        lmList = detector.findPosition(img,draw=False)
        if len(lmList) != 0:
            # Draw line between thumb and index finger
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Draw circles on the tips of the fingers
            # cv2.circle(img, (x1, y1), 9, (255, 0, 255), cv2.FILLED)
            # cv2.circle(img, (x2, y2), 9, (255, 0, 255), cv2.FILLED)

            # Draw line between the tips of the fingers
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Calculate the length of the line between the tips of the fingers
            length = math.hypot(x2 - x1, y2 - y1)
            print(length)

            # Calculate the distance between the palm and the finger endpoint
            x1, y1 = lmList[0][1], lmList[0][2]
            x2, y2 = lmList[5][1], lmList[5][2]
            hand_size = math.hypot(x2 - x1, y2 - y1)
            print(f"HAND SIZE :: {hand_size}")
            # Use the size of the hand in the image as a proxy for distance from the camera
            distance_from_camera = np.interp(hand_size, [min_hand_size, max_hand_size], [max_distance, min_distance])
            
            # Adjust the volume based on the distance from the camera and the distance between the thumb and index finger
            vol = np.interp(length, [15, 220], [volMin, volMax])
            vol *= distance_from_camera / max_distance
            # vol = np.interp(length, [15, 220], [volMin, volMax])
            print(vol, length)
            volume.SetMasterVolumeLevel(vol, None)  
            
            
            
            # Draw a circle on the center of the line between the tips of the fingers
            cv2.circle(img, (cx, cy), 9, (255, 0, 255), cv2.FILLED)




        cv2.putText(img=img, text=f"FPS: {int(fps)}", org=(10, 70),fontFace= cv2.FONT_HERSHEY_PLAIN,fontScale=3, color=(255, 0, 255), thickness=3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()