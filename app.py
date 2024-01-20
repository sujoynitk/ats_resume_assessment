import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2 as pdf
import os


load_dotenv()  #load all environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

def get_text_from_pdf(uploaded_pdf_file):
    pdf_data = pdf.PdfReader(uploaded_pdf_file)
    text = ""
    for page in range(len(pdf_data.pages)):
        page_content = pdf_data.pages[page].extract_text()
        text+=str(page_content)
    return text

#Prompt template

input_prompt = """
Hey Act like a very skilled and experienced ATS(Application Tracking System) with deep
knowledge and understanding about technical areas like ABAP Dictionaries, Reports, Forms, Enhancements, 
Workflows, BRFplus, HANA, S4HANA, implementation projects. You have been assigned a task 
to evaluate a resume based on given job-description. Consider that the current job
market is very competitive and hence you should provide best assistance
to improve resume. Assign percentage matching based on Jd and the missing keywords with high accuracy

resume:{text}
description:{jd}

I want the final response as a single string in format {{"JD Match":"%i", "Missing keywords": "[]", "Profile summary": ""}}
"""

#Create streamlit app

st.title("ATS for resume evaluation")
st.text("Check how good your resume fits with the job description")
jd = st.text_area("Paste the job description here")
uploaded_file = st.file_uploader("Upload your resume here", type="pdf")
submit = st.button("Check your resume match")

if submit:
    if uploaded_file:
        text = get_text_from_pdf(uploaded_file)
        response = gemini_response(input_prompt)
        st.subheader(response)
        