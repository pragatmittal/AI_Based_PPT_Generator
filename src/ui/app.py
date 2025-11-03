import streamlit as st
import requests

# Define FastAPI backend URL
API_URL = "https://ai-based-ppt-generator-1.onrender.com"

st.set_page_config(page_title="AI-Based PowerPoint Generator", layout="centered")
st.title("AI-Based PowerPoint Generator")
st.write("Upload your documents, and let AI create PowerPoint presentations for you!")

# File uploader
uploaded_file = st.file_uploader("Upload Documents (Text, PDF, etc.)", type=["pdf", "docx", "txt", "csv", "xlsx"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' selected!")
    
    # Upload file to FastAPI backend
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    upload_response = requests.post(f"{API_URL}/upload", files=files)
    
    if upload_response.status_code == 200:
        st.success("File uploaded successfully!")
        
        # Generate presentation
        generate_response = requests.post(f"{API_URL}/generate/", files=files)
        
        if generate_response.status_code == 200:
            st.success("Presentation generated successfully!")
            
            # Get download URL
            download_url = f"{API_URL}/download/?filename=output/generated_presentation.pptx"
            st.markdown(f"[Download Presentation]({download_url})", unsafe_allow_html=True)
        else:
            st.error("Error generating presentation. Please try again.")
    else:
        st.error("Error uploading file. Please try again.")
