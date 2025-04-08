from distances import recherche_image
import numpy as np
import streamlit as st
import os
from descripteurs import glcm, haralik_feat, bitdesc, glcm_haralik_bit  

os.makedirs("temp_images", exist_ok=True)


def load_signature(extraction_method):
    """Load the precomputed signature based on the extraction method selected."""
    if extraction_method == "GLCM":
        return np.load('SignatureGLCM.npy')
    elif extraction_method == "Haralick":
        return np.load('SignatureHaralik.npy')
    elif extraction_method == "Bitdesc":
        return np.load('SignatureBitdesc.npy')
    elif extraction_method == "GLCM + Haralick + Bitdesc":
        return np.load('SignatureConcat.npy')


def process_uploaded_image(uploaded_file, extraction_method):
    """Process the uploaded image and extract features based on the selected method."""
    file_path = os.path.join("temp_images", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    
    if extraction_method == "GLCM":
        img_features = glcm(file_path)
    elif extraction_method == "Haralick":
        img_features = haralik_feat(file_path)
    elif extraction_method == "Bitdesc":
        img_features = bitdesc(file_path)
    elif extraction_method == "GLCM + Haralick + Bitdesc":
        img_features = glcm_haralik_bit(file_path)

    return img_features


def main():
    st.title("Content-Based Image Retrieval (CBIR)")

    
    extraction_method = st.selectbox("Select Feature Extraction Method", 
                                     ("GLCM", "Haralick", "Bitdesc", "GLCM + Haralick + Bitdesc"))
    
    
    signature = load_signature(extraction_method)

    uploaded_image = st.file_uploader("Upload an image to find similar images", type=["jpg", "png", "jpeg", "bmp"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="🖼 Uploaded Image", use_container_width=True)

       
        img_features = process_uploaded_image(uploaded_image, extraction_method)

      
        distance_metric = st.selectbox("Select Distance Metric", ("euclidienne", "manhatan", "chebyshev", "canberra"))

       
        num_results = st.slider("Number of similar images to display", min_value=1, max_value=20, value=5)

       
               
        SIMILARITY_THRESHOLD = 1000

      
        results = recherche_image(signature, img_features, distance=distance_metric, K=num_results)

        
        filtered_results = []

        
        for img_path, dist, label in results:
            if dist < SIMILARITY_THRESHOLD: 
                filtered_results.append((img_path, dist, label))

       
        if filtered_results:
            st.write(f"Found {len(filtered_results)} similar images:")

            
            for img_path, dist, label in filtered_results:
                image_full_path = os.path.join("animalsCbir", img_path)
                st.image(image_full_path, caption=f" Similarity: {dist:.4f} | Label: {label}", use_container_width=True)
        else:
            st.warning(f"No similar images found with a similarity below {SIMILARITY_THRESHOLD}.")
    else:
        st.warning(" Please upload an image to start the search.")


if __name__ == "__main__":
    main()
