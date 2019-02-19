import cv2,numpy as np,time

img=cv2.imread('/Users/jerry/Downloads/IMG_0257.JPG')
start=time.time()
#img=cv2.imread('/Users/jerry/Downloads/IMG_0258.JPG')
imgR=cv2.resize(img,(1080,720))
img=cv2.GaussianBlur(imgR,(3,3),0)
img=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
_,img=cv2.threshold(img,192,255,cv2.THRESH_BINARY)

img,contours,hierarchy=cv2.findContours(img, 1, 2)


c=max(contours,key=lambda c:sum(cv2.minAreaRect(c)[1]))
rect = cv2.minAreaRect(c)
b = np.int0(cv2.boxPoints(rect))
cv2.drawContours(imgR, [b], -1, (0, 0, 255), 2)

cv2.putText(imgR,str(round(rect[2],2))+'deg',(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2,cv2.LINE_AA)
print(time.time()-start)

cv2.imshow('',imgR)
cv2.waitKey(0)
