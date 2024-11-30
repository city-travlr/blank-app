import streamlit as st
from app.pdf_utils import extract_text_from_pdf  # PDF processing
from app.ppt_generator import generate_pptx      # PowerPoint generation
from app.nlp_utils import extract_key_details_hf, summarize_text  # Hugging Face NLP

st.title("RFP to PowerPoint Generator")

# Step 1: Upload the PDF
uploaded_file = st.file_uploader("Upload an RFP PDF", type=["pdf"])
if uploaded_file:
    st.write("**Uploaded RFP Content:**")
    rfp_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted RFP Text", value=rfp_text, height=300)

    # Step 2: Extract key details
    st.write("**Extracted Key Details Using NLP:**")
    key_details = extract_key_details_hf(rfp_text)
    for section, content in key_details.items():
        st.write(f"**{section}:** {content}")

    # Step 3: Summarize the text
    st.write("**Summarized Content:**")
    summary = summarize_text(rfp_text)
    st.write(summary)

    # Step 4: Generate PowerPoint
    if st.button("Generate PowerPoint"):
        pptx_file = generate_pptx(key_details)
        st.download_button(
            label="Download PowerPoint",
            data=pptx_file,
            file_name="RFP_Response_Presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
