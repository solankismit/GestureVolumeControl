import HandTracking.HandTrackingModule as htm
import cv2
import time
import numpy as np
import math
import pyautogui
import pycaw

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0

    detector = htm.HandDetector()

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


        cv2.putText(img=img, text=f"FPS: {int(fps)}", org=(10, 70),fontFace= cv2.FONT_HERSHEY_PLAIN,fontScale=3, color=(255, 0, 255), thickness=3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()