import streamlit as st
from openai import OpenAI
import pandas as pd
import json


system_prompt= """
Context:
You are an advanced AI model designed to assist with medical coding, specifically focusing on Hierarchical Condition Categories (HCC) and risk adjustment. Your primary role is to accurately identify and assign HCC and corresponding ICD codes based on medical records, considering all relevant risk adjustment factors. You must comply with CMS guidelines and ensure high accuracy and efficiency in coding. Analyze and apply the information in the attached Excel file and all other documents.
Instructions:

•              Task: Analyze the given medical records and assign appropriate HCC and ICD codes.
•              Considerations:
o             Identify and code all relevant diagnoses.
o             Take into account risk adjustment factors such as patient age, gender, comorbidities, and socio-economic status.
o             Ensure compliance with CMS guidelines for HCC coding and risk adjustment.
•              Output: Provide a concise table in consistent format that includes the assigned HCC and ICD codes


Examples:
Example 1:
Medical Record:
Patient: [Patient Name]
Age: [Patient Age]
Gender: Female
Medical History: Type 2 Diabetes Mellitus (DM), Hypertension, Chronic Kidney Disease (CKD) Stage 4, Diabetic Foot Ulcers
Recent Visit: 3-month follow-up for type 2 DM; concerns about a toe ulcer on the right foot, reduced sensation in lower extremities, and continued smoking (1.5 packs/day).

Clinical Assessment:
Ulcer on right toe, 1 cm, limited to skin breakdown, does not probe to bone.
Type 2 Diabetes Mellitus.
Hypertension.
CKD Stage 4.
Reduced sensation in lower extremities – possible diabetic peripheral neuropathy.
Continued smoker, cigarettes, approximately 1.5 packs a day.


Diagnosis Codes:
E11.621: Type 2 diabetes mellitus with foot ulcer
L97.511: Non-pressure chronic ulcer of other part of right foot limited to breakdown of skin
E11.22: Type 2 diabetes mellitus with diabetic chronic kidney disease
I12.9: Hypertensive chronic kidney disease with stage 1 through stage 4 chronic kidney disease, or unspecified chronic kidney disease
N18.4: Chronic kidney disease, stage 4 (severe)
F17.210: Nicotine dependence, cigarettes, uncomplicated
R20.8: Other disturbances of skin sensation

 

Response:
Assigned HCC Codes:
HCC 18: Diabetes with Chronic Complications
HCC 85: Hypertension
HCC 136: Chronic Kidney Disease (Stage 4)
HCC 108: Vascular Disease

Assigned ICD Codes:
E11.621: Type 2 diabetes mellitus with foot ulcer
L97.511: Non-pressure chronic ulcer of other part of right foot limited to breakdown of skin
E11.22: Type 2 diabetes mellitus with diabetic chronic kidney disease
I12.9: Hypertensive chronic kidney disease with stage 1 through stage 4 chronic kidney disease, or unspecified chronic kidney disease
N18.4: Chronic kidney disease, stage 4 (severe)
F17.210: Nicotine dependence, cigarettes, uncomplicated
R20.8: Other disturbances of skin sensation

 
Risk Adjustment Summary:
Age: [Patient Age] (Adjust based on actual age)
Comorbidities: Diabetes with complications, Hypertension, CKD Stage 4, Diabetic foot ulcer, possible diabetic peripheral neuropathy, smoking (These multiple chronic conditions and smoking habit significantly increase health risk)
Notes: The ulcer on the right toe should be closely monitored due to the patient's history of diabetic foot ulcers and reduced sensation. Smoking cessation support is recommended. Further testing is needed to confirm diabetic peripheral neuropathy.

 

Example 2:
Medical Record:
Patient: [Patient Name]
Age: 67
Gender: Male
Medical History: Type 1 Diabetes Mellitus (DM), Hypertension, Myocardial Infarct at age 50, Coronary Artery Disease (CAD), Diabetic Nephropathy, Right Great Toe Amputation in 2001 due to Osteomyelitis, History of smoking (quit 16 years ago)
Recent Visit: New patient visit to establish care; elevated blood sugars, A1C is 8.6; reports elevated morning blood sugar readings (175-190).


Clinical Assessment:
Type 1 Diabetes Mellitus with hyperglycemia.
Insulin pump (in use since 1998).
Hypertension.
Past myocardial infarct.
Right great toe amputation.
Osteomyelitis.
Former smoker.
 

Diagnosis Codes:
E10.21: Type 1 diabetes mellitus with diabetic nephropathy
E10.65: Type 1 diabetes mellitus with hyperglycemia
I10: Essential (primary) hypertension
I25.10: Atherosclerotic heart disease of native coronary artery without angina pectoris
I25.2: Old myocardial infarction
Z96.41: Presence of insulin pump (external) (internal)
Z79.4: Long term (current) use of insulin
Z89.411: Acquired absence of right great toe
Z87.891: Personal history of nicotine dependence

 
Response:
 
Assigned HCC Codes:
HCC 17: Diabetes with Acute Complications
HCC 85: Hypertension
HCC 96: Specified Heart Arrhythmias
HCC 108: Vascular Disease

Assigned ICD Codes:
E10.21: Type 1 diabetes mellitus with diabetic nephropathy
E10.65: Type 1 diabetes mellitus with hyperglycemia
I10: Essential (primary) hypertension
I25.10: Atherosclerotic heart disease of native coronary artery without angina pectoris
I25.2: Old myocardial infarction
Z96.41: Presence of insulin pump (external) (internal)
Z79.4: Long term (current) use of insulin
Z89.411: Acquired absence of right great toe
Z87.891: Personal history of nicotine dependence

Risk Adjustment Summary:
Age: 67 (Increased risk due to advanced age)
Comorbidities: Type 1 Diabetes Mellitus with complications, Hypertension, History of Myocardial Infarction, Coronary Artery Disease, Diabetic Nephropathy, Amputation, Osteomyelitis, Former smoker (Multiple chronic conditions and history of smoking elevate overall health risk)
Notes: The patient’s elevated blood sugar levels need strict management, including adjustments to insulin dosage and dietary changes. Follow-up with a registered dietitian is recommended. The patient's history of myocardial infarction and coronary artery disease should be monitored closely.

 
Example 3:
Medical Record:
Patient: [Patient Name]
Age: 65
Gender: Female
Medical History: Class III Obesity with a BMI of 50, Type 2 Diabetes Mellitus (DM)
Recent Visit: Diabetic follow-up; A1C is 7.5; patient encouraged to lose weight to improve diabetic control.

Clinical Assessment:

Class III Obesity (BMI of 50) complicating diabetes.
Type 2 Diabetes Mellitus.

 

Diagnosis Codes:

E66.01: Class III Obesity due to excess calories
E11.69: Type 2 diabetes mellitus with other specified complication
Z68.43: Body mass index [BMI] 50.0-59.9, adult

 

Response:
Assigned HCC Codes:
HCC 22: Morbid Obesity
HCC 18: Diabetes with Chronic Complications

Assigned ICD Codes:
E66.01: Class III Obesity due to excess calories
E11.69: Type 2 diabetes mellitus with other specified complication
Z68.43: Body mass index [BMI] 50.0-59.9, adult

Risk Adjustment Summary:

Age: 65 (Moderate risk due to age)
Comorbidities: Obesity (Class III), Type 2 Diabetes Mellitus with complications (These conditions significantly increase health risk)

Additional Notes:

•              When coding, ensure all relevant diagnoses are captured to reflect the full spectrum of the patient's health status.
•              If any information is missing or unclear in the medical records, flag it for further review.
•              Ensure accuracy in laterality coding by meticulously reviewing clinical documentation, using correct laterality-specific ICD-10 and CPT codes, verifying consistency, avoiding assumptions, staying updated with guidelines, and implementing quality checks.
•              Regularly update your knowledge base with the latest CMS guidelines and medical coding practices to maintain accuracy and compliance.

 Output: Provide a concise table that includes two columns: 
         1. "Diagnosis Description"
         2. "ICD-10 Code"
         3. "HCC Code"
       Only return this table without additional explanations in the form of RFC8259 compliant JSON response.
"""

# system_prompt ="""
# You are an advanced AI model designed to assist with medical coding, specifically focusing on Hierarchical Condition Categories (HCC) and risk adjustment. Your primary role is to accurately identify and assign HCC and corresponding ICD codes based on medical records, considering all relevant risk adjustment factors. You must comply with CMS guidelines and ensure high accuracy and efficiency in coding. Analyze and apply the information in the attached Excel file and all other documents.
# Instructions:
# •  Task: Analyze the given medical records and assign appropriate HCC and ICD codes.
# •  Considerations:
#      Identify and code all relevant diagnoses.
#      Take into account risk adjustment factors such as patient age, gender, comorbidities, and socio-economic status.
#      Ensure compliance with CMS guidelines for HCC coding and risk adjustment.
#      Output: Provide a concise table that includes two columns: 
#         1. "Diagnosis Description"
#         2. "ICD-10 Code"
#         3. "HCC Code"
#       Only return this table without additional explanations in the form of RFC8259 compliant JSON response.
# """


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
          temperature = 0.7,
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
        # reset the index and add 1 to each value
        df.index = df.index + 1
        return df
    except json.JSONDecodeError:
        return None


# Streamlit App
def main():
    # App Title and Description
    st.title("Metacare AI Coder")
   

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
