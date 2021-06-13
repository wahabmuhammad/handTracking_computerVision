import cv2
import time
import math
import numpy as np
import handtracking_module as htm
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1280, 720 #lebar dan tinggi tampilan webcam
cam = cv2.VideoCapture(0) #input video from webcam
cam.set(3,wCam) #mengatur lebar webcam
cam.set(4,hCam) #mengatur tinggi webcam

pTime = 0 #input time untuk FPS
# cTime = 0 

detector = htm.handDetector(detectionCon=0.7) #import module hand tracking untuk mendeteksi tangan
devices = AudioUtilities.GetSpeakers() #input speaker perangkat
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None) #mengaktivasi speaker
volume = cast(interface, POINTER(IAudioEndpointVolume)) #Variabel volume 
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange() #volRange jarak index volume

minVol = volRange[0] #volume minimal
maxVol  = volRange[1] #volume maximal
vol = 0
volBar = 400
volPer = 0

print("Selamat datang di Volume Control Visual")
var1 = input("Anda ingin menjalankan program ini? ")

while True:
    if var1 == 'iya':
        source, img = cam.read() #membaca sumber dari webcam
        img = cv2.flip(img, 1,1) #mirorring tampilan webcam
        img = detector.findHands(img) #detector tangan
        lmlist = detector.findPosition(img, draw=False) #untuk menemukan daftar landmark dari tangan
        if len(lmlist) != 0:
            # print(lmlist[4], lmlist[20])

            x1, y1 = lmlist[4][1],lmlist[4][2] #landmark 4 adalah jempol dan index 1 atau 2 adalah jari kanan dan kiri
            x2, y2 = lmlist[8][1],lmlist[8][2] #landmark 8 adalah telunjuk dan index 1 atau 2 adalah jari kanan dan kiri
            cx, cy = (x1+x2)//2, (y1+y2)//2 

            cv2.circle(img, (x1, y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img, (x2, y2),15,(255,0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),4)
            cv2.circle(img, (cx, cy),15,(255,0,255),cv2.FILLED)

            length = math.hypot(x2-x1,y2-y1)
            # print(length)
            
            # Hand Range 50-300
            # Volume Range -65-0

            vol = np.interp(length,[50,300],[minVol,maxVol])
            volBar = np.interp(length,[50,300],[400,150])
            volPer = np.interp(length,[50,300],[0,100])
            # print(int(length), vol)
            volume.SetMasterVolumeLevel(vol,None)

            if length <50:
                cv2.circle(img, (x2, y2),15,(0,255,0),cv2.FILLED)

        cv2.rectangle(img, (50,150),(85,400),(0,255,255),3)
        cv2.rectangle(img, (50, int(volBar)),(85,400),(0,255,255),cv2.FILLED)
        cv2.putText(img, "Vol: " +str(int(volPer)) + "%", (40,450), cv2.FONT_HERSHEY_PLAIN,2 ,(0,255,255),2)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, "FPS: " +str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3 ,(0,255,255),3)

        cv2.imshow('Volume Control', img)
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):
            break
            cam.release()
            cv2.destroyAllWindows()
    else:
        break



    