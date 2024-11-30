import streamlit as st
from pdf_utils import extract_text_from_pdf  # PDF processing
from nlp_utils import summarize_text, extract_key_details  # Hugging Face NLP
from ppt_generator import generate_pptx  # PowerPoint generation

# Title and Introduction
st.title("RFP to PowerPoint Generator")
st.write("Upload an RFP document to generate a summary and extract key details for your proposal.")

# Step 1: Upload the PDF
uploaded_file = st.file_uploader("Upload an RFP PDF", type=["pdf"])
if uploaded_file:
    st.write("**Uploaded RFP Content:**")
    # Extract text from the uploaded PDF
    rfp_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted RFP Text", value=rfp_text, height=300)

    # Step 2: Extract Key Details
    st.write("**Key Details Extracted Using NLP:**")
    key_details = extract_key_details(rfp_text)
    for section, content in key_details.items():
        st.write(f"**{section}:** {content}")

    # Step 3: Summarize the RFP
    st.write("**Summarized Content:**")
    summary = summarize_text(rfp_text)
    st.write(summary)

    # Step 4: Generate PowerPoint
    if st.button("Generate PowerPoint"):
        with st.spinner("Generating PowerPoint..."):
            pptx_file = generate_pptx(key_details)  # Generate the PowerPoint file
        st.success("PowerPoint generated successfully!")
        st.download_button(
            label="Download PowerPoint",
            data=pptx_file,
            file_name="RFP_Response_Presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by [Your Name/Team].")
