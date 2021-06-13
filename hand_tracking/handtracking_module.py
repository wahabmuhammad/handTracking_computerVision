import cv2
import time
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands = 4, detectionCon =0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handlns in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlns, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0,draw=True):

        lmlist = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
                # if id == 4:
                if draw:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
        return lmlist

def main():
    pTime = 0
    cTime = 0
    cam = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        source, img = cam.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        # if len(lmlist) != 0:
        #     print(lmlist[4])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3 ,(255,0,255),3)

        cv2.imshow('image', img)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()