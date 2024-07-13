import streamlit as st
import os
from extract_pdf import extract_text_from_pdf
from fine_tune import predict
from NER import extract_entities
import re
from streamlit_option_menu import option_menu

classes = {
    0: "Services Provided", 
    1: "Payment", 
    2: "Term", 
    3: "Confidentiality", 
    4: "Termination", 
    5: "Governing Law", 
    6: "Signatures"
}

selected = option_menu(
    menu_title = None,
    options = ["Extracted content", "Predicted Clause", "Extracted Entities", "Summary"],
    menu_icon= "cast",
    orientation = "horizontal",

)


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
    if selected == "Extracted content": st.markdown("## Extracted Content")
    uploaded_file_path = save_uploaded_file(upload_file, "uploaded_file")
    text = extract_text_from_pdf(uploaded_file_path)
    
    # Add border to the extracted content
    if selected == "Extracted content":  st.markdown("""
        <div style="border:2px solid black; padding: 10px;  background-color: #f0f0f5;">
            <Extracted Text>
            <p>{}</p>
        </div>
    """.format(text.replace("\n", "<br>")), unsafe_allow_html=True)
    
    if selected == "Predicted Clause":st.markdown("## Predicted Clause")
    
    # Initialize an HTML string with a border for predicted clauses
    html_content = '<div style="border:2px solid black; padding: 10px;  background-color: #f0f0f5;"><Predicted Clauses>'
    
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
    if selected == "Predicted Clause":st.markdown(html_content, unsafe_allow_html=True)
    
    if selected == "Extracted Entities": st.markdown("## Extracted Entities")
    
    # Initialize an HTML string with a border for extracted entities
    entities_html_content = '<div style="border:2px solid black; padding: 10px;  background-color: #f0f0f5;"><Extracted Entities>'
    stack = []
    for entity in all_entities:
        if entity[1] == 'CARDINAL':
            continue
        elif entity[0] in stack:
            continue
        entities_html_content += f"<b>{entity[1]} :</b> {entity[0]}<br>"
        stack.append(entity[0])
    
    # Close the HTML string for extracted entities
    entities_html_content += '</div>'
    
    # Display the extracted entities content with border
    if selected == "Extracted Entities": st.markdown(entities_html_content, unsafe_allow_html=True)

    if selected == "Summary": st.markdown("## Summary")
    

    details = {}
    for entity in all_entities:
       details[entity[1]] = entity[0]
    # print(details)

    summary_content = f"""
        <div style="border:2px solid black; padding: 10px;  background-color: #f0f0f5;">
            <b> {details["PARTY_A"]} </b> agrees to provide services to <b> {details["PARTY_B"]} </b>, 
            as <b> {details["PARTY_B"]} </b> agrees to pay <b> ${details["MONEY"]} </b> to <b> {details["PARTY_A"]} </b> for the described services provided
              for  <b> {details["NOTICE_DAYS"]} days </b>. This contract will commence on <b> {details["START_DATE"]} </b> and continue till <b> {details["END_DATE"]} </b>.
             Both the parties agrees to maintain the <b> {details["CONFIDENTIALITY"]} </b> of any proprietary
               or confidential information disclosed during theterm of this contract. This obligation will continue beyond the 
               termination of this contract. This contract shall be governed by and construed in accordance
                 with the laws of the State of <b> {details["STATE"]} </b> . .<br>
            
        </div>
        """
    

    
    if selected == "Summary":st.markdown(summary_content, unsafe_allow_html=True)

