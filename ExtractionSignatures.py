import os
from descripteurs import glcm,glcm_haralik_bit
import numpy as np

def extraction_caracteristiques(chemin):
    liste_carac=[]
    # Parcourir tous les fichier et dossier
    for root,dirs,files in os.walk(chemin):
        for file in files:
            if file.lower().endswith(('.png','jpg','.bmp','jpeg')):
                path_relative=os.path.relpath(os.path.join(root,file),chemin)
                
                path=os.path.join(root,file)
                carac=glcm_haralik_bit(path)
                print(carac)
                class_name=os.path.dirname(path_relative)
                liste_carac.append(carac+[class_name,path_relative])
    Signatures=np.array(liste_carac)
    np.save('SignatureConcat.npy',Signatures)

def main():
    extraction_caracteristiques('./animalsCbir/')

if __name__=='__main__':
    main()