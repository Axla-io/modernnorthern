"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "AXLRSN"

import rhinoscriptsyntax as rs
import Rhino
import Rhino.Geometry as rg
import random
import ghpythonlib.treehelpers as th

"""Perform K-means clustering and group together everything

inputs:
    pts, that are to be clustered nx1
    K layers of clustering that we want

outputs:
    Points per K, the first row corresponds to the input, then each new row corresponds to the different means generated in the previous round.
    Groups per K, a matrix nxk. each row represents a layer of clustering
    C_matrix is the connectivity matrix for the flattened version of PPK"""


def k_means_random_centroids_init(pts,K,step=1):
    #Creates a random point inside bounding box
    #Coerce point3dlist
    pts=Rhino.Collections.Point3dList(pts)
    bounds=pts.BoundingBox#Gets bounding box
    maxPt=bounds.Max
    minPt=bounds.Min
    xrange=[maxPt.X, minPt.X] # sets them at least a mm apart
    yrange=[maxPt.Y, minPt.Y]
    zrange=[maxPt.Z, minPt.Z]

    centroids=[] #Create container list
    for i in range(K):
        x=random.uniform(xrange[1],xrange[0])
        y=random.uniform(yrange[1],yrange[0])
        z=random.uniform(zrange[1],zrange[0])
        centroids.append(rg.Point3d(x,y,z))
    return centroids

def findClosestCentroids(pts,centroids,tol=Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance):
    idx=[]
    for i in range(len(pts)):
        pt=pts[i]
        dist_vec=[rg.Point3d.Subtract(pt,c).Length for c in centroids if c not in pts]
        dist_vec=[x for x in dist_vec if x>tol]
        if dist_vec:
            idx.append(dist_vec.index(min(dist_vec)))
        else: #This is a dirty hack to avoid problems when clusters alternate
            idx.append(0)
    return idx


def computeCentroids(pts,idx,K):
    centroids=[]
    for k in range(K):
        id_list = [i for i, x in enumerate(idx) if x == k]
        x=[pts[x] for x in id_list]
        centroid=rg.Point3d(0,0,0)
        for pt in x:
            centroid=rg.Point3d.Add(pt,centroid)
        centroid=rg.Point3d.Divide(centroid,len(x))
        centroids.append(centroid)
    return centroids

def movementCheck(centroids,old_centroids):
    dist_vec= []
    for i in range(len(centroids)):
        c=centroids[i]
        oc=old_centroids[i]
        dist_vec.append(rg.Point3d.Subtract(c,oc).Length)
    tot_vec=0
    for l in dist_vec: tot_vec +=l
    return tot_vec


def kMeans(pts,K, iter=1000,tol=Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance):
    centroids=k_means_random_centroids_init(pts,K)
    old_centroids=[]
    for i in range(iter):
        old_centroids=centroids
        idx = findClosestCentroids(pts, centroids)
        centroids = computeCentroids(pts, idx, K)
        tot_vec=movementCheck(centroids,old_centroids)
        if tot_vec< tol:
            break
    return pts, idx, centroids

def createCmatrix(GPK):
    #Creates the connectivity matrix for the cluster from the GroupsPerK data tree.
    G_flat = [item for sublist in GPK for item in sublist]
    G_flat.append(0)
    C_empty= [0 for x in G_flat]
    C=[list(C_empty) for x in G_flat]
    Layer_count=0
    grave=0
    c=0
    t_c=0 #temporary c
    for i in range(len(G_flat)):
        if Layer_count>= len(GPK):
            break
        Current_Layer=GPK[Layer_count]
        n=len(Current_Layer) #Length of current layer
        group=G_flat[c] #The different values we encounter in the current layer
        #print(group)
        id_list=[]
        if ConnectGroup==True:
            id_list = [i for i, x in enumerate(Current_Layer) if x == group]
            id_list=[x+grave for x in id_list]
        if grave+n+group<=len(G_flat)-1:
            id_list.append(grave+n+group)

        for id in id_list:
            C[c][id]=1
        c+=1
        t_c+=1
        if t_c==n:
            Layer_count+=1
            t_c=0
            grave+=n
            if grave>=len(G_flat):
                break

    return C






pts=pts_init
K=k_init
tol=Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance




"""Procedure:
Main K-means loop, for decreasing K:
    1. set bounds of current set of points
    2. do random initialization within bounds and with k points
    3. perform k-means with current set of points and k
    4. output vector of current points, resulting groups for current points, and new means,
    if means are same, destroy one. If one is destroyed, perform extra decrease on k.
    5. decrease K and set generated means as current points for next iteration

"""
PPK=[] #List of list of points in each iteration of the clustering per iteration
GPK=[]  #The group of which of the point in PPK belongs to, as name of the future centroid in next iteration

for i in range(K+1,0,-1):
    if len(pts)==1:
        PPK.append(pts)
        break
    elif K<1:
        cent_final=rg.Point3d(0,0,0)
        for pt in pts:
            cent_final=rg.Point3d.Add(pt,cent_final)
        cent_final=rg.Point3d.Divide(cent_final,len(pts))
        PPK.append(cent_final)
        break
    pts, idx, centroids=kMeans(pts,K)

    PPK.append(pts)




    centhelp= [cnt for cnt in centroids if cnt.IsValid==True]
    idxhelp=[centhelp.index(centroids[id]) for id in idx]
    GPK.append(idxhelp)

    centroids=centhelp
    K=K-1
    pts=centroids
    if len(pts)<K:
        K=len(pts)

C = createCmatrix(GPK)
C_matrix=th.list_to_tree(C, source=[0,0])
Points=th.list_to_tree(PPK, source=[0,0])
GroupsPerK=th.list_to_tree(GPK, source=[0,0])
