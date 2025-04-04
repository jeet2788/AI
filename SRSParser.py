
#Imports#
import json
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableLambda
from tabulate import tabulate

# ✅ Load environment variables
load_dotenv()

# ✅ Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""
    You are analyzing a Software Requirements Specification (SRS) document.

    Extract the following information:
    - **Topic**: Identify the main topic.
    - **Structure**: Structured, Unstructured, or One Statement.
    - **Complexity Level**: High or Low.

    Respond **ONLY** in **valid JSON format** without any extra text:
    {{
      "topic": "<Extracted Topic>",
      "structure": "<Structured/Unstructured/One Statement>",
      "level": "<High/Low>"
    }}

    Text: {text}
    """
)

# ✅ Initialize OpenAI GPT with JSON enforced output
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    model_kwargs={"response_format": {"type": "json_object"}}  # ✅ Correct JSON enforcement
)

def parse_gpt_response(response):
    """Ensures GPT response is a valid JSON object."""
    try:
        raw_content = response.content if hasattr(response, "content") else response

        if isinstance(raw_content, dict):  # ✅ Already JSON
            return raw_content
        elif isinstance(raw_content, str):  # ✅ Parse JSON if string
            return json.loads(raw_content.strip())

        print(f"❌ Unexpected GPT response format: {type(raw_content)}")
        return None
    except json.JSONDecodeError:
        print(f"❌ JSON Parsing Error: Could not decode: {response}")
        return None


# ✅ Create a runnable pipeline
chain = prompt_template | llm | RunnableLambda(parse_gpt_response)


def analyze_with_gpt(text):
    """Runs GPT analysis and ensures valid JSON output."""
    try:
        result = chain.invoke({"text": text[:8000]})  # ✅ Limit text to 8000 chars for large docs
        return result if result else None
    except Exception as e:
        print(f"❌ GPT Processing Error: {e}")
        return None


def read_document(file_path):
    """Reads a text-based document (TXT, PDF, or DOCX) and returns its content."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    elif ext == ".pdf":
        try:
            import PyPDF2  # ✅ Ensure PyPDF2 is installed (`pip install PyPDF2`)
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

        except Exception as e:
            raise ValueError(f"❌ PDF parsing error: {e}")

    elif ext in [".doc", ".docx"]:
        try:
            import docx  # ✅ Ensure `python-docx` is installed (`pip install python-docx`)
            doc = docx.Document(file_path)
            return "\n".join(para.text for para in doc.paragraphs)

        except Exception as e:
            raise ValueError(f"❌ DOCX parsing error: {e}")

    else:
        raise ValueError(f"❌ Unsupported file format: {ext}")


# ✅ Process all files in a folder
def process_folder(folder_path):
    """Iterates through all files in the folder and processes them."""
    if not os.path.isdir(folder_path):
        raise ValueError(f"❌ The provided path is not a directory: {folder_path}")

    results = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            print(f"🔹 Processing file: {filename}")
            document_text = read_document(file_path)
            analysis_result = analyze_with_gpt(document_text)

            if analysis_result:
                results[filename] = analysis_result
            else:
                print(f"❌ Failed to analyze {filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    return results


# ✅ Process folder and generate structured table output
if __name__ == "__main__":
    folder_path = r"C:\Users\itrad\Downloads\req"

    try:
        analysis_results = process_folder(folder_path)

        if analysis_results:
            # ✅ Convert results to table format
            table_data = []
            for filename, data in analysis_results.items():
                table_data.append([
                    filename,
                    data.get("topic", "N/A"),
                    os.path.splitext(filename)[1],  # Extract file extension as format
                    "Unknown",  # Placeholder for Pages (you can extract it from word count)
                    "Unknown",  # Placeholder for Pictures/Tables (need image processing)
                    data.get("level", "N/A"),
                    data.get("structure", "N/A"),
                    "Unknown"  # Placeholder for Source
                ])

            # ✅ Define column headers
            headers = [
                "Doc Name", "Topic", "Format", "Pages", "Pictures/Tables",
                "Level", "Structure", "Source"
            ]

            # ✅ Print structured table output
            print("\n✅ Final GPT Analysis Output:")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

        else:
            print("❌ No valid SRS documents processed.")

    except Exception as e:
        print(f"❌ Error: {e}")
