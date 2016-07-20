#####       TEST 2 - PATH FINDING   VER 4.0    
####        TO Find start and end points as (R,C) + points of all walls
###         + apply FOREST FIRE ALGO from start point to end point
##          + track back PATH from end point to end point
#

import numpy as np
import cv2
import time

#start
t1=time.time()

img=cv2.imread('test_image2.png')

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

def check(r,c,rp,cp):  #CHECK conditions      
    if r in range(1,11) and c in range(1,11):        

        a=(matt[r][c]==0 and matt[r][c]!=-1)

        #e=r in range(ro[1]-2,ro[1]+gr) and c in range(co[1]-2,co[1]+gc)

        return a# and e

def fill(r,c,rp,cp):    #fill cell current(r,c) and parent(rp,cp)
    
    if check(r,c,rp,cp): 
        
        matt[r][c] = 1 + matt[rp][cp]   #current=1+parent
        
        fill(r+1,c,r,c)                 #
        fill(r,c+1,r,c)
        fill(r,c-1,r,c)
        #fill(r-1,c,r,c)

fill(ro[1]+1,co[1],ro[1],co[1]) #RANDOM call
#fill(ro[1],co[1]+1,ro[1],ro[1])
print "\n\n"

print matt


    ## track path

tailr=list()    #row
tailc=list()    #col

def track(r,c):
    
    if r in range(ro[0]-gr-2,ro[0]+2) and c in range(co[0]-gc-2,co[0]+2):

        #print r,c
        
        e=(matt[r][c]==10)      #start
        #print r

        a=(matt[r][c-1]==-1 or matt[r][c-1]==0)    #left  a wall and 0
        #print x
        
        b=(matt[r-1][c]==-1 or matt[r-1][c]==0)    #top  a wall and 0
        #print y

        g=(matt[r][c+1]==-1 or matt[r][c+1]==0)    #right  a wall and 0
    
        #print a,b,g

        ## following elif ladder is combination of 3 conditions :
        ## TOP , LEFT , RIGHT cells
        ## The combo for Valid and candidate cell is :
        ## 1. all 3 valid
        ## 2. any 2
        ## 3. any 1
        
        if a and not b and not g: # left is a wall , go for top n right
            #print "101"
            if matt[r-1][c]<matt[r][c+1]:   #top < right
                tailr.append(r-1)
                tailc.append(c)
                track(r-1,c)
                
            else:
                tailr.append(r)
                tailc.append(c+1)
                track(r,c+1)
        elif b and not a and not g:# top is a wall , go for left n right
            #print "011"
            if matt[r][c-1]<matt[r][c+1]:   #left < right
                tailr.append(r)
                tailc.append(c-1)
                track(r,c-1)
            else:
                tailr.append(r)
                tailc.append(c+1)
                track(r,c+1)
        elif g and not a and not b:# right is a wall , go for top n left

            #print "110" #
            if matt[r][c-1]<matt[r-1][c]:   #left < top
                tailr.append(r)
                tailc.append(c-1)
                track(r,c-1)
            else:
                tailr.append(r-1)
                tailc.append(c)
                track(r-1,c)
        elif b and a and not g:# go for right
                #print "001"
                tailr.append(r)
                tailc.append(c+1)
                track(r,c+1)
        elif b and g and not a:# go for left
                #print "100"
                tailr.append(r)
                tailc.append(c-1)
                track(r,c-1)
        elif g and a and not b:# go for top
                #print "010"
                tailr.append(r-1)
                tailc.append(c)
                track(r-1,c)
        elif not a and not g and not b: # check all 3
#            print "111"
            if matt[r-1][c]<matt[r][c-1]:
                if matt[r-1][c]<matt[r][c+1]:
                    
                    tailr.append(r-1)
                    tailc.append(c)
                    track(r-1,c)

                else:
                    tailr.append(r)
                    tailc.append(c+1)
                    track(r,c+1)
            else:
                if matt[r][c-1]<matt[r][c+1]:
                    
                    tailr.append(r)
                    tailc.append(c-1)
                    track(r,c-1)

                else:
                    tailr.append(r)
                    tailc.append(c+1)
                    track(r,c+1)
                
track(ro[0],co[0])

print tailr
print tailc

    ##detect CELLs in image as BOTTOM-RIGHT point represents the CELL 

for i in range(0,len(tailr)):
#    for j in range(0,len(tailc)):
        cv2.circle(img,(tailc[i]*40,tailr[i]*40),3,(0,0,255),-1)

cv2.imshow('img',img)          #original

#end
print(time.time()-t1)

#################### END ############################
if cv2.waitKey(0)==27:
    cv2.destroyAllWindows()
