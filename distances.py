import numpy as np
from scipy.spatial import distance

def manhattan(v1,v2):
    v1=np.array(v1).astype('float')
    v2=np.array(v2).astype('float')
    dist=np.sum(np.abs(v1-v2))
    return dist
    
def enclidienne(v1,v2):
    v1=np.array(v1).astype('float')
    v2=np.array(v2).astype('float')
    dist=np.sqrt(np.sum(v1-v2)**2)
    return dist

def chebyshev(v1,v2):
    v1=np.array(v1).astype('float')
    v2=np.array(v2).astype('float')
    dist=np.max(np.abs(v1-v2))
    return dist

def canberra(v1,v2):
    return distance.canberra(v1,v2)


def recherche_image(bdd_signature,img_requete,distance,K):
    img_similaire=[]
    for instance in bdd_signature:
        cara,label,img_chemin=instance[:-2],instance[-2],instance[-1]
        if distance=='euclidienne':
            dist=enclidienne(img_requete,cara)
        if distance=='manhatan':
            dist=manhattan(img_requete,cara)
        if distance=='chebyshev':
            dist=chebyshev(img_requete,cara)
        if distance=='canberra':
            dist=canberra(img_requete,cara)
        img_similaire.append((img_chemin,dist,label))
        img_similaire.sort(key=lambda x:x[1])
    return img_similaire[:K]



