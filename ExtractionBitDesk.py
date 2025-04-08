import os
import cv2
import numpy as np
from descripteurs import bitdesc  


def extraction_caracteristiques_bitdesc(chemin):
    liste_carac = []

    for root, dirs, files in os.walk(chemin):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.bmp', '.jpeg')):
                path_relative = os.path.relpath(os.path.join(root, file), chemin)
                path = os.path.join(root, file)
                
                
                carac = bitdesc(path)
                print(carac)  
                
                
                class_name = os.path.dirname(path_relative)
                
            
                liste_carac.append(carac + [class_name, path_relative])
    

    Signatures = np.array(liste_carac)
    
    
    np.save('SignatureBitdesc.npy', Signatures)

def main():
    extraction_caracteristiques_bitdesc('./animalsCbir/')  

if __name__ == '__main__':
    main()