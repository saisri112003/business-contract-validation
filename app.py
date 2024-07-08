import streamlit as st
import pandas as pd
from io import StringIO
import os
from extract_pdf import extract_text_from_pdf
from fine_tune import predict
from spac import extract_details

classes = {
    0: "Services Provided", 
    1: "Payment", 
    2: "Term", 
    3: "Confidentiality", 
    4: "Termination", 
    5: "Governing Law", 
    6: "Signatures"
}

def save_uploaded_file(uploaded_file, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path,"wb") as f:
        f.write(uploaded_file.read())
    return file_path

# Title 
st.title("File Upload Example")

# File uploader
upload_file = st.file_uploader("Choose the file")

if upload_file is not None:
    st.markdown("## Extracted Content")
    uploaded_file_path = save_uploaded_file(upload_file, "uploaded_file")
    text = extract_text_from_pdf(uploaded_file_path)
    all_entities = extract_details(text)
    # print (all_entities)
    # Add border to the extracted content
    st.markdown("""
        <div style="border:2px solid black; padding: 10px;">
            <b>Extracted Text:</b>
            <p>{}</p>
        </div>
    """.format(text.replace("\n", "<br>")), unsafe_allow_html=True)
    
    st.markdown("## Predicted Clause")
    
    # Initialize an HTML string with a border
    html_content = '<div style="border:2px solid black; padding: 10px;"><b>Predicted Clauses:</b><br>'
    
    for line in text.splitlines():
        label_idx = predict(line)
        if label_idx != 6:
            html_content += f"{line} <b>[{classes[label_idx]}]</b><br>"
        else:
            html_content += f"{line}<br>"
    
    # Close the HTML string
    html_content += '</div>'
    
    # Display the content with border
    st.markdown(html_content, unsafe_allow_html=True)


    









