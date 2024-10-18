import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#
cap = cv2.VideoCapture(1)
pTime = 0

detector = htm.handDetector(detectionCon=0.8)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]


while True:
    success, img = cap.read()
    
    img = detector.findHands(img, draw= False)
    lmList = detector.findPosition(img, points_to_draw=[4, 8])
    
    if lmList != None:
        tumbx, tumby = lmList[4][1], lmList[4][2]
        indx, indy = lmList[8][1], lmList[8][2]
        centrex, centrey = (tumbx + indx) // 2, (tumby + indy) // 2
        
        cv2.line(img, (tumbx, tumby), (indx, indy), (0, 0, 0), 3)
        cv2.circle(img, (centrex, centrey), 10, (0,0,0),  cv2.FILLED)
        line_length = math.hypot(indx - tumbx, indy - tumby)

        vol = np.interp(line_length, [10, 200], [min_vol, max_vol])
        volume.SetMasterVolumeLevel(vol, None)
        
        if line_length < 25:
            cv2.circle(img, (centrex, centrey), 10, (0,0,255),  cv2.FILLED)
        
        
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                1, (255, 255, 255), 1)
    cv2.imshow("Img", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()