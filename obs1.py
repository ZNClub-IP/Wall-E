#####       TEST 2   VER 1.0
####        TO Find start and end points as (R,C)
###     
##
#

import numpy as np
import cv2

img=cv2.imread('test_image5.png')

h,w,c=img.shape
#hi=float(h)/10      #height grid by 10
#wj=float(w)/10      #width grid by 10
#print h,w,c,hi,wj

#cv2.imshow('img',img)


#masking

l2=np.array([76,72,34])
u2=np.array([204,177,63])

mask=cv2.inRange(img,l2,u2)
andd=cv2.bitwise_and(img,img,mask=mask)

gray = cv2.cvtColor(andd,cv2.COLOR_BGR2GRAY)        #GRAY

ret,thresh = cv2.threshold(gray,80,255,0)          #THRESH
#cv2.imshow('thresh',thresh)


contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    #CONTOUR
cv2.drawContours(andd,contours,-1,(0,0,255),1)        #DRAW CONTOUR red

        #BEGIN TO FIND (R,C)

cnt=contours        #rename contours to cnt
dim=40              #scaling factor
                    #row point list = [ end , start ]
ro=list()
                    #col point list = [ end , start ]
co=list()



    #for all contours find (R,C)        
for i in range(0,len(cnt)):
    x,y,wr,hr = cv2.boundingRect(contours[i])       #get top left point

    print x,y,wr,hr
    #print i
    #print int(x/dim)        #col
    #print int(y/dim)        #row
    ro.append(int(y/dim)+1)
    co.append(int(x/dim)+1)
    #im3 = cv2.rectangle(andd,(x,y),(x+wr,y+hr),(0,0,0),2)  #show rectangle
print ro
print co

        


#cv2.imshow('andd',andd)

#cv2.imshow('mask',mask)

#################### END ########################

if cv2.waitKey(0)==27:
    cv2.destroyAllWindows()
            
