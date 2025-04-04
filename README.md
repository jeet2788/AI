# Ice Breaker
# 🧠 AI SRS Analyzer

A LangChain-based Python application that uses OpenAI's GPT-4 to analyze Software Requirements Specification (SRS) documents and extract structured metadata like topic, complexity, and format.

---

## 🚀 Features

- 📂 Batch process `.txt`, `.pdf`, `.docx` files from a folder
- 🤖 Uses OpenAI GPT-4 to extract:
  - **Topic**
  - **Document Structure** (Structured / Unstructured / One Statement)
  - **Complexity Level** (High / Low)
- 📊 Displays the results in a clean, tabular format using `tabulate`
- ✅ Handles file parsing and LLM JSON responses robustly

---

## 🧰 Tech Stack

| Layer          | Tools / Libraries                  |
|----------------|------------------------------------|
| LLM            | OpenAI GPT-4 via `langchain_openai` |
| Prompting      | `langchain_core.prompts`           |
| File Parsing   | `PyPDF2`, `python-docx`            |
| Env Handling   | `dotenv`                           |
| Display Output | `tabulate`                         |
| Runtime Logic  | `RunnableLambda`, LangChain chains |

---

## 🧠 APIs & Key Modules Used

### 🔹 OpenAI GPT API (via LangChain)
- `ChatOpenAI` with GPT-4o and JSON-mode enforced using:
  ```python
  model_kwargs={"response_format": {"type": "json_object"}}


  🔹 LangChain Components
PromptTemplate: Custom prompt for extracting SRS attributes

RunnableLambda: Lightweight pipeline runner to parse GPT response

chain.invoke(): Executes the prompt-to-response pipeline

🔹 Document Readers
.txt: Basic UTF-8 reader

.pdf: PyPDF2.PdfReader

.docx: python-docx.Document

📦 Installation
✅ Clone the Repo
bash
Copy
Edit
git clone https://github.com/jeet2788/AI.git
cd AI
✅ Create and Activate Virtual Env (Optional but Recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
✅ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
You may need to install:

bash
Copy
Edit
pip install openai langchain python-dotenv tabulate PyPDF2 python-docx
🔐 Environment Setup
Create a .env file in the root directory:

ini
Copy
Edit
OPENAI_API_KEY=your-openai-api-key
🛠️ Usage
✅ Run the Analyzer
Update this line in the script with your folder path:

python
Copy
Edit
folder_path = r"C:\Users\itrad\Downloads\req"
Then run:

bash
Copy
Edit
python your_script.py
It will:

Read all valid SRS files from the folder

Analyze each file using GPT

Display a table with extracted data

📈 Example Output
sql
Copy
Edit
✅ Final GPT Analysis Output:

+--------------+--------------------+----------+--------+--------------------+---------+----------------------+----------+
| Doc Name     | Topic              | Format   | Pages  | Pictures/Tables    | Level   | Structure            | Source   |
+--------------+--------------------+----------+--------+--------------------+---------+----------------------+----------+
| spec1.pdf    | CRM Integration    | .pdf     | Unknown| Unknown            | High    | Structured           | Unknown  |
| doc2.docx    | User Auth System   | .docx    | Unknown| Unknown            | Low     | One Statement        | Unknown  |
+--------------+--------------------+----------+--------+--------------------+---------+----------------------+----------+
📂 Project Structure
bash
Copy
Edit
AI-SRS-Analyzer/
│
├── ai_srs_analyzer.py         # 🔧 Main script
├── requirements.txt           # 📦 Python dependencies
├── .env                       # 🔐 OpenAI API key
├── README.md                  # 📄 Documentation (this file)
└── /req                       # 📂 Folder containing input SRS docs

