import cv2
import time
import mediapipe as mp
import handtracking_module as htm

wCam = 1920
hCam = 1080

pTime = 0
cTime = 0

cam = cv2.VideoCapture(0)
cam.set(3,wCam)
cam.set(4,hCam)
detector = htm.handDetector(detectionCon=0.7)
    
while True:
    source, img = cam.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    # if len(lmlist) != 0:
    #     print(lmlist[4])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, "FPS: "+ str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3 ,(255,0,255),3)

    cv2.imshow('image', img)
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()