# 📌 Imports
import os
import fitz  # PyMuPDF for PDF text extraction
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st

# Load environment variables (API key)
load_dotenv()

# 🔹 Function to Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# 🔹 LangChain Resume Summarization Prompt
resume_template = """
Given the following resume information: {resume_text}

Generate:
1. A professional summary of the candidate.
2. Top 5 key skills.
3. Relevant work experience in bullet points.
"""

# 🔹 Create Prompt Template
resume_prompt_template = PromptTemplate(
    input_variables=["resume_text"],
    template=resume_template
)

# 🔹 Initialize OpenAI LLM
llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)

# 🔹 Streamlit UI
st.title("📄 AI-Powered Resume Summarizer")

uploaded_file = st.file_uploader("Upload your Resume (PDF file)", type=["pdf"])

if uploaded_file:
    # ✅ Ensure the 'uploads/' directory exists
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # ✅ Save the uploaded file
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"File saved successfully: {file_path}")

    # ✅ Extract text from PDF resume
    resume_text = extract_text_from_pdf(file_path)
    st.subheader("Extracted Resume Text:")
    st.text_area("", resume_text, height=300)

    # ✅ Generate structured summary
    st.subheader("📌 AI-Generated Resume Summary:")
    chain = resume_prompt_template | llm
    res = chain.invoke(input={"resume_text": resume_text})

    st.text_area("", res.content, height=400)

    # ✅ Option to download the summary
    st.download_button("Download Summary", res.content, file_name="Resume_Summary.txt")
