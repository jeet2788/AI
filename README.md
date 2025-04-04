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
