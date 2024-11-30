import streamlit as st
from pdf_utils import extract_text_from_pdf
from nlp_utils import extract_key_details, summarize_text
from ppt_generator import generate_pptx

st.title("RFP to PowerPoint Generator")
st.write("Upload an RFP PDF, extract key sections, and generate a professional PowerPoint.")

uploaded_file = st.file_uploader("Upload an RFP PDF", type=["pdf"])
#esse tá certo
if uploaded_file:
    rfp_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted RFP Text", value=rfp_text, height=300)

    st.write("**Extracted Key Details Using NLP:**")
    key_details = extract_key_details(rfp_text)
    for section, content in key_details.items():
        st.write(f"**{section}:** {content}")

    if st.button("Generate PowerPoint"):
        pptx_file = generate_pptx(key_details)
        st.download_button(
            label="Download PowerPoint",
            data=pptx_file,
            file_name="RFP_Response_Presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
