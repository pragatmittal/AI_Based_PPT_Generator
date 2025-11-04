import streamlit as st
import requests
import time

# Define FastAPI backend URL - Update this with your actual Render backend URL
API_URL = "https://ai-based-ppt-generator-1.onrender.com"  # Replace with actual backend URL

st.set_page_config(page_title="AI-Based PowerPoint Generator", layout="centered")
st.title("AI-Based PowerPoint Generator")
st.write("Upload your documents, and let AI create PowerPoint presentations for you!")

# File uploader
uploaded_file = st.file_uploader("Upload Documents (Text, PDF, etc.)", type=["pdf", "docx", "txt", "csv", "xlsx"])

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' selected!")
    
    try:
        # Upload file to FastAPI backend
        st.info("Uploading file...")
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        upload_response = requests.post(f"{API_URL}/upload", files=files, timeout=30)
        
        if upload_response.status_code == 200:
            st.success("File uploaded successfully!")
            
            # Generate presentation
            st.info("Generating presentation...")
            generate_response = requests.post(f"{API_URL}/generate/", files=files, timeout=60)
            
            if generate_response.status_code == 200:
                st.success("Presentation generated successfully!")
                
                # Get download URL
                response_data = generate_response.json()
                download_url = f"{API_URL}/download/?filename=output/generated_presentation.pptx"
                st.markdown(f"[📥 Download Presentation]({download_url})", unsafe_allow_html=True)
            else:
                st.error(f"Error generating presentation: {generate_response.text}")
        else:
            st.error(f"Error uploading file: {upload_response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Please check if the API is running.")
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")