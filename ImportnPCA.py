import os
from numpy import *
from PIL import Image
import PCAtools
import matplotlib.pyplot as plt
import ExportTools

#Gets current path and goes into Images folder.
path= os.getcwd()+"/Images"


#Creates an array of the images names
imageNameList=[name for name in os.listdir(path)if name !=".DS_Store"]

#Creates an array of the images names corresponding integers
imageNumList=[int(name.split(".")[0]) for name in imageNameList]

#Sorts name list according to number list
imageNameList=[x[1] for x in sorted(zip(imageNumList,imageNameList))]
n=len(imageNameList)

#Thumbnail Width
width=32
height=32

#Initiate image container
imList=[]

#Loop to crop and scale pictures
j=1
for name in imageNameList:
    absname=path+"/"+name
    thumb=PCAtools.cropScale(width,height,absname)
    message="Processing image %d of %d" %(j,len(imageNameList))
    print(message)
    j+=1
    imList.append(thumb)

#Get X
X=PCAtools.unrollStack(imList)

#Perform renormalization
norm=PCAtools.featureNormalize(X)
X_norm=norm[0]

#Perform PCA
decomp=PCAtools.pca(X)
U=decomp[0]
S=decomp[1]

#Create reduced U-matrix
k=3
Ureduce= empty(shape=[k, U.shape[1]])
counter=0
for ind in Uinds:
    newrow=U[ind:ind+1,:]
    Ureduce[c,:] =newrow
    counter+=1

#Calculate total variance
Uinds=range(0,k,1)
Svals=[S[i]for i in Uinds]
var=1-(sum(Svals)/sum(S))

#Create Z vector, or picures in feature space
Z=matmul(Ureduce,X.transpose())

#Create approximation
Xapprox=matmul(Z.transpose(),Ureduce)

#Show approximation
#PCAtools.showreconstruction(Xapprox,width,height)

#Write to json if coordinate system
if k==3:
    export_name="Zmat"
    ExportTools.exporttoJSON(Z.transpose(),export_name)
