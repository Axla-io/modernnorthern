import json
import os

def exporttoJSON(X,filename):
    X_list=X.tolist()
    name="%s.json"%(filename)
    filename=os.getcwd()+"/"+name
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(X_list, f, ensure_ascii=False, indent=4)
