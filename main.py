import cv2
import numpy as np

frameWidth = 1000
frameHeight = 1000

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

myColors = [[42,85,59,87,255,255],
            [0,122,114,9,255,255],
            [23,110,141,62,255,255]]
myColorValues = [[84,146,1],          ## BGR
                 [3,0,233],
                 [1,200,255]]
points=[]


def findColor(img, myColors, myColorValues):
    imgHsv= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        
        lower=np.array(color[0:3])
        upper=np.array(color[3:6])
        mask= cv2.inRange(imgHsv,lower,upper)
        x,y= getContours(mask)
        
        cv2.circle(imgRes,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        # cv2.imshow(str(color[0]),mask)
    
    return newPoints

def getContours(img):
    contours, hierarchy= cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area= cv2.contourArea(cnt)
        print(area)
        
        # cv2.drawContours(imgRes, cnt, -1,(255,0,0),3)    
        peri=cv2.arcLength(cnt,True)
        approx=cv2.approxPolyDP(cnt,0.06*peri,True)
        x,y,w,h= cv2.boundingRect(approx)
            
    return x+w//2, y
            
def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgRes, (point[0], point[1]),12, myColorValues[point[2]], cv2.FILLED)       

while True:
    success, img = cap.read()
    imgRes= img.copy()
    newPoints= findColor(img,myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            points.append(newP)
    if len(points)!=0:
        drawOnCanvas(points,myColorValues)
    cv2.imshow("Result", imgRes)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
