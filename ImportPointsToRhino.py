import json
import rhinoscriptsyntax as rs
from System.Drawing import Color
import os

filename=os.getcwd()+"/Zmat.json"
with open(filename, 'r') as f:
    loaded_json = json.load(f)

LayerName="ImportPoints"

if not rs.IsLayer(LayerName):
    rs.AddLayer(LayerName,Color.Red)

counter=1
for pt in loaded_json:
    point=rs.AddPoint(pt)
    rs.ObjectName(point,str(counter))
    rs.ObjectLayer(point,LayerName)
    counter+=1
