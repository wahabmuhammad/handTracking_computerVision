import cv2
import time
import mediapipe as mp

cam = cv2.VideoCapture(0)
cam.set(4, 1080)
cam.set(3, 1920)

mpHands = mp.solutions.hands
hands = mpHands.Hands(False)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    source, img = cam.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handlns in results.multi_hand_landmarks:
            for id, ln in enumerate(handlns.landmark):
                h,w,c = img.shape
                cx,cy = int(ln.x*w), int(ln.y*h)
                # if id == 4:
                cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handlns, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3 ,(255,0,255),3)


    cv2.imshow('image', img)
    key = cv2.waitKey(10)
    if key == 27 or key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()