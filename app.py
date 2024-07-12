import streamlit as st
import os
from extract_pdf import extract_text_from_pdf
from fine_tune import predict
from NER import extract_entities
import re

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
    
    # Add border to the extracted content
    st.markdown("""
        <div style="border:2px solid black; padding: 10px;">
            <b>Extracted Text:</b>
            <p>{}</p>
        </div>
    """.format(text.replace("\n", "<br>")), unsafe_allow_html=True)
    
    st.markdown("## Predicted Clause")
    
    # Initialize an HTML string with a border for predicted clauses
    html_content = '<div style="border:2px solid black; padding: 10px;"><b>Predicted Clauses:</b><br>'
    # all_entities = []
    # for line in text.splitlines():
    #     label_idx = predict(line)
    #     if label_idx != 6:
    #         html_content += f"{line} <b>[{classes[label_idx]}]</b><br>"
    #     else:
    #         html_content += f"{line}<br>"
    #     entities = extract_entities(line)
    #     all_entities.extend(entities)
    
    all_entities = []
    for line in text.splitlines():
        predicted_class = predict(text=line)
        if predicted_class == 6 or re.search(r"\d\s*\.\s*([\w\s]+)\s*:", line):
            html_content += f"{line}<br>"
            entities = []
        else:
            html_content += f"{line} <b>[{classes[predicted_class]}]</b><br>"
            entities = extract_entities(text=line)
        all_entities.extend(entities)
    # Close the HTML string for predicted clauses
    html_content += '</div>'
    
    # Display the predicted clauses content with border
    st.markdown(html_content, unsafe_allow_html=True)
    
    st.markdown("## Extracted Entities")
    
    # Initialize an HTML string with a border for extracted entities
    entities_html_content = '<div style="border:2px solid black; padding: 10px;"><b>Extracted Entities:</b><br>'
    stack = []
    for entity in all_entities:
        if entity[1] == 'CARDINAL':
            continue
        elif entity[0] in stack:
            continue
        entities_html_content += f"{entity[0]} <b>{entity[1]}</b><br>"
        stack.append(entity[0])
    
    # Close the HTML string for extracted entities
    entities_html_content += '</div>'
    
    # Display the extracted entities content with border
    st.markdown(entities_html_content, unsafe_allow_html=True)

    st.markdown("## Summary")
    

    details = {}
    for entity in all_entities:
       details[entity[1]] = entity[0]
    print(details)

    summary_content = f"""
        <div style="border:2px solid black; padding: 10px;">
            <b>Summary:</b><br>
            {details["PARTY_A"]} agrees to provide services to {details["PARTY_B"]}, as {details["PARTY_B"]} agrees to pay {details["MONEY"]} to {details["PARTY_A"]} for the described services provided for {details["NOTICE_DAYS"]}. This contract will commence on {details["START_DATE"]} and continue till {details["END_DATE"]}. Both the parties agrees to maintain the {details["CONFIDENTIALITY"]}  of any proprietary or confidentials ] .<br>
            
        </div>
        """
    

    
    st.markdown(summary_content, unsafe_allow_html=True)

