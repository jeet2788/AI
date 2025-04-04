import streamlit as st
import os
import mailparser
from dotenv import load_dotenv

from extract_pdf import extract_text_from_pdf
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Ensure OpenAI API Key is set
load_dotenv()

st.title("🚀 AI-Powered SRS Generator")

# File uploader for PDFs and EMLs
uploaded_files = st.file_uploader("📂 Upload Emails or PDFs", accept_multiple_files=True, type=["pdf", "eml"])

# ✅ Function to extract text from EML files
def extract_text_from_email(file_path):
    """Extracts plain text from .eml email files"""
    mail = mailparser.parse_from_file(file_path)
    return "\n".join(mail.text_plain)  # Extract plain text content

# ✅ Function to split text into smaller chunks
def split_text(text, chunk_size=4000, chunk_overlap=500):
    """Splits long text into smaller chunks to avoid exceeding GPT token limits"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n\n", "\n", " "]
    )
    return text_splitter.split_text(text)

# ✅ Function to generate SRS using GPT-4-turbo (preferred) or GPT-3.5-turbo-16k
def generate_srs(text):
    """Processes long text in chunks and generates an SRS using GPT-4-turbo"""
    llm = ChatOpenAI(model_name="gpt-4-turbo")  # 🔹 Use "gpt-3.5-turbo-16k" if needed

    chunks = split_text(text)  # Split text into smaller chunks
    srs_sections = []

    for i, chunk in enumerate(chunks):
        with st.spinner(f"Processing chunk {i+1}/{len(chunks)}..."):
            prompt = f"Extract key software requirements and format as an SRS document:\n\n{chunk}"
            response = llm.invoke(prompt)
            srs_sections.append(response.content)

    return "\n\n".join(srs_sections)  # Merge sections into final SRS

# ✅ Button to process uploaded files
if st.button("📝 Generate SRS"):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one PDF or EML file.")
    else:
        all_text = ""

        # Process uploaded files
        for file in uploaded_files:
            file_path = os.path.join("uploads", file.name)
            os.makedirs("uploads", exist_ok=True)  # Ensure uploads folder exists

            with open(file_path, "wb") as f:
                f.write(file.read())

            if file.name.endswith(".pdf"):
                all_text += extract_text_from_pdf(file_path) + "\n"
            elif file.name.endswith(".eml"):
                all_text += extract_text_from_email(file_path) + "\n"

        # Generate SRS if text is extracted
        if all_text.strip():
            srs_output = generate_srs(all_text)
            st.text_area("📄 Generated SRS", srs_output, height=400)

            # ✅ Download Button
            st.download_button("📥 Download SRS", srs_output, file_name="SRS_Document.txt")
        else:
            st.warning("⚠️ No extractable text found in the uploaded files.")
