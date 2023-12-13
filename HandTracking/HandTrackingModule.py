import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self,mode = False, maxHands = 2, detectionCon=0.5,trackCon = 0.5) -> None:
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Hand Tracking Module
        self.mpHands = mp.solutions.hands

        # Hands object
        self.hands = self.mpHands.Hands(static_image_mode=False,
               max_num_hands=self.maxHands,
               min_detection_confidence=self.detectionCon,
               min_tracking_confidence=self.trackCon)

        # Draw the hand landmarks
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the image
        self.results = self.hands.process(imgRGB)

        # Check if there are any hand landmarks
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img


    def findPosition(self,img,handNo=0,draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 9, (255, 0, 255), cv2.FILLED)
        return lmList
    
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0

    detector = HandDetector()

    while True:
        success, img = cap.read()

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cv2.putText(img=img, text=f"FPS: {int(fps)}", org=(10, 70),fontFace= cv2.FONT_HERSHEY_PLAIN,fontScale=3, color=(255, 0, 255), thickness=3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()