#pip install scikit-image
#pip install mahotas
from skimage.feature import graycomatrix,graycoprops
from mahotas.features import haralick
from BiT import bio_taxo

import cv2
import numpy as np

# Extraction des caractéristiques

def glcm(chemin):
    data=cv2.imread(chemin,0)
    co_matrice=graycomatrix(data,[1],[0,np.pi/2],None,symmetric=True,normed=False)
    dissimilarity=graycoprops(co_matrice,'dissimilarity')[0,0]
    contrast=graycoprops(co_matrice,'contrast')[0,0]
    correlation=graycoprops(co_matrice,'correlation')[0,0]
    energy=graycoprops(co_matrice,'energy')[0,0]
    homogeneity=graycoprops(co_matrice,'homogeneity')[0,0]
    ASM=graycoprops(co_matrice,'ASM')[0,0]
    features=[dissimilarity,contrast,correlation,energy,homogeneity,ASM]
    features=[float(x) for x in features]
    return features

# Les carateristiques d'Haralik
def haralik_feat(chemin):
    data=cv2.imread(chemin,0)
    features=haralick(data).mean(0).tolist()
    features=[float(x) for x in features]
    return features

def bitdesc(chemin):
    data=cv2.imread(chemin,0)
    bit_features=bio_taxo(data)
    bit_features=[float(x) for x in bit_features]
    return bit_features


def glcm_haralik_bit(chemin):
    return glcm(chemin)+haralik_feat(chemin)+bitdesc(chemin)