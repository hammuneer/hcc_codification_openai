import streamlit as st

from hcc_codifier.coder import extract_assessment

st.title("Clinical Note Diagnosis Extractor")

clinical_note_input = st.text_area("Enter Clinical Note:", height=300)

if st.button("Get Diagnosis"):
    if clinical_note_input:
        with st.spinner("Processing..."):
            result = extract_assessment(clinical_note_input)
        st.success("Diagnosis extracted successfully!")
        st.text_area("Extracted Diagnoses:", value=result, height=300)
    else:
        st.error("Please enter a clinical note before proceeding.")
