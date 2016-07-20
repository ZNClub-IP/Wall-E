#####       TEST 2   VER 2.0
####        TO Find start and end points as (R,C) + points of all walls
###         
##
#

import numpy as np
import cv2
import time

#start
t1=time.time()

img=cv2.imread('test_image5.png')

h,w,c=img.shape
#hi=float(h)/10      #height grid by 10
#wj=float(w)/10      #width grid by 10
#print h,w,c,hi,wj

#cv2.imshow('img',img)          #original


            #masking START and END pts

l2=np.array([76,72,34])         #green
u2=np.array([204,177,63])       #blue

mask=cv2.inRange(img,l2,u2)
andd=cv2.bitwise_and(img,img,mask=mask)

gray = cv2.cvtColor(andd,cv2.COLOR_BGR2GRAY)        #GRAY

ret,thresh = cv2.threshold(gray,80,255,0)            #THRESH
#cv2.imshow('thresh',thresh)    #thresh

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    #CONTOUR
cv2.drawContours(andd,contours,-1,(0,0,255),1)        #DRAW CONTOUR

        #BEGIN TO FIND (R,C)

cnt=contours        #rename contours to cnt
dim=40              #scaling factor
grid=10
                    #row point list = [ end , start ]
ro=list()
                    #col point list = [ end , start ]
co=list()



    #for all contours find (R,C)        
for i in range(0,len(cnt)):
    x,y,wr,hr = cv2.boundingRect(contours[i])       #get top left point

    #print x,y,wr,hr
    #print i
    #print int(x/dim)        #col
    #print int(y/dim)        #row
    ro.append(int(y/dim)+1)
    co.append(int(x/dim)+1)
    #im3 = cv2.rectangle(andd,(x,y),(x+wr,y+hr),(0,0,0),2)  #show rectangle
#print ro
#print co
        
#cv2.imshow('andd',andd)

#cv2.imshow('mask',mask)
    
    #find BLACK WALLs

i=20
while i in range(0,400):
    j=20
    while j in range(0,400):
        if img[i][j][0]==0 and img[i][j][1]==0 and img[i][j][2]==0:
            #print i,j,(i/dim)+1,(j/dim)+1
            ro.append(int(i/dim)+1)
            co.append(int(j/dim)+1)
            
        j+=40
    i+=40
##    
##print ro
##print co


    ## mapping image to matrix

matt=np.zeros(shape=(grid+1,grid+1),dtype=int)
#print matt
#print matt.shape

#for i in range(0,2):

matt[ro[0]][co[0]]=100      #end
#print matt[ro[0]][co[0]]

matt[ro[1]][co[1]]=10       #start
#print matt[ro[1]][co[1]]

#print max(ro)
#print max(co)

gr=abs(ro[1]-ro[0])+1       #grid of end n start
gc=abs(co[1]-co[0])+1
#print gr,gc

for i in range(2,len(ro)):  #walls
    matt[ro[i]][co[i]]=-1

print matt

        ##apply algo
#end
print(time.time()-t1)

#################### END ############################
if cv2.waitKey(0)==27:
    cv2.destroyAllWindows()
            
