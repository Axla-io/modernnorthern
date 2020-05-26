from numpy import *
from PIL import Image
import matplotlib.pyplot as plt

def cropScale(new_width,new_height,image):
    im = Image.open(image)
    width, height = im.size

    new_aspect=new_width/new_height
    old_aspect=width/height
    left=0
    right=width
    bottom=height
    top=0


    if old_aspect<new_aspect: #tall case
        changed_height=height*old_aspect/new_aspect
        top = (height - changed_height)/2
        bottom = (height + changed_height)/2

    elif old_aspect>new_aspect: #wide case
        changed_width=width*new_aspect/old_aspect
        right = (width + changed_width)/2
        left = (width - changed_width)/2


    # Crop the center of the image
    im = im.crop((left, top, right, bottom))
    size=(new_width,new_height)

    thumb=im.resize(size)
    return thumb

def unrollStack(imList):
    m=len(imList)
    image=imList[0]
    data = asarray(image)
    n=len(data[:][:][0].ravel()))
    X=empty(shape=(m,n,3))
    print(X.shape)
    for i in range(len(imList)):
        image=imList[i]
        data = asarray(image)
        if len(data.shape)<3:
            data=array([data,data,data])
        data=array([data[0][:][:].ravel(),data[1][:][:].ravel(),data[2][:][0].ravel()])
        X[i][:][:]=data.transpose()
    return asarray(X)

def featureNormalize(X):
    mu = X.mean(axis=0)
    X_norm = X-mu


    sigma=std(X_norm)
    X_norm = X_norm/sigma;

    return [X_norm, mu, sigma]


def pca(X):
    m = X.shape[0]
    Sigma=matmul(X.transpose(),X)/m;
    U,S,V=linalg.svd(Sigma)
    return [U,S]

def findbiggestindex(X,k):
    return X.argsort()[-k:][::-1]

def showreconstruction(X,width,height):
    m,n= X.shape
    for i in range(m):
        row=X[i,:]
        rec_arr=reshape(row,(width, height,3))
        im=Image.fromarray(uint8(rec_arr))
        plt.imshow(im)
        plt.show()
