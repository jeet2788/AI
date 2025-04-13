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
    - **Source**: Industry or University

    Respond **ONLY** in **valid JSON format** without any extra text:
    {{
      "topic": "<Extracted Topic>",
      "structure": "<Structured/Unstructured/One Statement>",
      "level": "<High/Low>",
      "source": "<Industry/University>"
    }}

    Text: {text}
    """
)

# ✅ Initialize OpenAI GPT with JSON enforced output
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    model_kwargs={"response_format": {"type": "json_object"}}
)

def parse_gpt_response(response):
    try:
        raw_content = response.content if hasattr(response, "content") else response
        if isinstance(raw_content, dict):
            return raw_content
        elif isinstance(raw_content, str):
            return json.loads(raw_content.strip())
        return None
    except json.JSONDecodeError:
        print(f"❌ JSON Parsing Error: {response}")
        return None

# ✅ Create a runnable pipeline
chain = prompt_template | llm | RunnableLambda(parse_gpt_response)

def analyze_with_gpt(text):
    try:
        result = chain.invoke({"text": text[:8000]})
        return result if result else None
    except Exception as e:
        print(f"❌ GPT Processing Error: {e}")
        return None

def read_document(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    page_count = 1

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read(), page_count

    elif ext == ".pdf":
        try:
            import PyPDF2
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                page_count = len(reader.pages)
                text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
                return text, page_count
        except Exception as e:
            raise ValueError(f"❌ PDF parsing error: {e}")

    elif ext in [".doc", ".docx"]:
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join(para.text for para in doc.paragraphs)
            word_count = len(text.split())
            page_count = max(1, word_count // 500)
            return text, page_count
        except Exception as e:
            raise ValueError(f"❌ DOCX parsing error: {e}")

    else:
        raise ValueError(f"❌ Unsupported file format: {ext}")

# ✅ Process folder of documents
def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError(f"❌ The provided path is not a directory: {folder_path}")

    results = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            print(f"🔹 Processing file: {filename}")
            document_text, page_count = read_document(file_path)
            analysis_result = analyze_with_gpt(document_text)

            if analysis_result:
                analysis_result["pages"] = page_count
                results[filename] = analysis_result
            else:
                print(f"❌ Failed to analyze {filename}")
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    return results

# ✅ Run the main logic and display table
if __name__ == "__main__":
    folder_path = r"C:\Users\itrad\Downloads\req_doc"  # ✅ Update this to your folder

    try:
        analysis_results = process_folder(folder_path)

        if analysis_results:
            table_data = []
            for filename, data in analysis_results.items():
                # ✅ Fix Source Mapping Here
                source_raw = data.get("source", "").strip().lower()
                source_mapped = {
                    "university": "U",
                    "industry": "I"
                }.get(source_raw, "Unknown")

                table_data.append([
                    filename,
                    data.get("topic", "N/A"),
                    os.path.splitext(filename)[1],
                    data.get("pages", "Unknown"),
                    "Unknown",  # Placeholder for Pictures/Tables
                    data.get("level", "N/A"),
                    data.get("structure", "N/A"),
                    source_mapped
                ])

            headers = [
                "Doc Name", "Topic", "Format", "Pages", "Pictures/Tables",
                "Level", "Structure", "Source"
            ]

            print("\n✅ Final GPT Analysis Output:")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

        else:
            print("❌ No valid SRS documents processed.")

    except Exception as e:
        print(f"❌ Error: {e}")
