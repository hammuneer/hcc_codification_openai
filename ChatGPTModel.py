import streamlit as st
from openai import OpenAI
import pandas as pd
import json

system_prompt ="""
You are an advanced AI model designed to assist with medical coding, specifically focusing on Hierarchical Condition Categories (HCC) and risk adjustment. Your primary role is to accurately identify and assign HCC and corresponding ICD codes based on medical records, considering all relevant risk adjustment factors. You must comply with CMS guidelines and ensure high accuracy and efficiency in coding. Analyze and apply the information in the attached Excel file and all other documents.


Instructions:

•              Task: Analyze the given medical records and assign appropriate HCC and ICD codes.

•              Considerations:

o             Identify and code all relevant diagnoses.

o             Take into account risk adjustment factors such as patient age, gender, comorbidities, and socio-economic status.

o             Ensure compliance with CMS guidelines for HCC coding and risk adjustment.

•              Output: Provide a concise table that includes two columns: 
                1. "Diagnosis Description"
                2. "ICD-10 Code"
                3. "HCC Code"

                Only return this table without additional explanations in the form of RFC8259 compliant JSON response.
"""
# OpenAI API key setup (Replace with your own API key)
# openai.api_key = 
# system_prompt = """
# You are an advanced AI model designed to assist with medical coding, specifically focusing on Hierarchical Condition Categories (HCC) and ICD-10. 
# Your primary role is to accurately identify and assign HCC and corresponding ICD-10 codes based on medical records.

# Instructions:

# • Task: Analyze the given clinical note, get all the mentioned diagnosis from the note and assign the appropriate HCC and ICD-10 codes.
# • Output: Provide a concise table that includes two columns: 
#   1. "Diagnosis Description"
#   2. "ICD-10 Code"
#   3. "HCC Code"

#   Only return this table without additional explanations in the form of RFC8259 compliant JSON response.
# """




api_key = '***REMOVED-OPENAI-KEY***'
client = OpenAI(api_key=api_key)
# Function to interact with OpenAI's GPT API

def get_codification(system_prompt, sample_user_prompt):
    try: 
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
            {"role": "system", "content":system_prompt},
            {"role": "user", "content": sample_user_prompt}
            ]
        )

        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"Error: {str(e)}"

# Function to parse the JSON string response into a table
def parse_codified_output_to_table(codified_note):
    try:
        sliced_note = codified_note[8:-4]
        # Convert the JSON string into a Python list of dictionaries
        data = json.loads(sliced_note)
        
        # Convert it into a pandas DataFrame
        df = pd.DataFrame(data)
        
        return df
    except json.JSONDecodeError:
        return None


# Streamlit App
def main():
    # App Title and Description
    st.title("Clinical Note Codification")
   

    # Input Section
    st.header("Input Clinical Note")
    clinical_note = st.text_area("Enter the clinical note below:", height=200)

    # Button to trigger codification
    if st.button("Codify Clinical Note"):
        if clinical_note:
            # Placeholder for output
            with st.spinner("Processing..."):
                # Call the backend GPT API to codify the clinical note
                codified_note = get_codification(system_prompt, clinical_note)
                
                # Parse the response and display it as a table
                df = parse_codified_output_to_table(codified_note)
                # Apply styling to the DataFrame (increase font-size, width, etc.)
                styled_df = df.style.set_table_styles(
                    [{
                        'selector': 'th',
                        'props': [('font-size', '16px'), ('text-align', 'center')]
                    }, {
                        'selector': 'td',
                        'props': [('font-size', '14px')]
                    }]).set_properties(**{'text-align': 'left'})

                # Set custom CSS to adjust width and table layout
                st.markdown(
                    """
                    <style>
                    .stDataFrame {
                        width: 100% !important;
                        margin: 0 auto;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                if df is not None:
                    st.success("Codification Completed")

                    # Display the output as a table
                    st.header("Codified HCC and ICD-10 Codes")
                    st.dataframe(df, width=1000, height=500)  # Display as an interactive table
                else:
                    st.error("The response was not a valid JSON format.")
        else:
            st.error("Please enter a clinical note to process.")

if __name__ == "__main__":
    main()
