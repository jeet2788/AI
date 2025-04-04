from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables (API key)
load_dotenv()

# Sample Resume Text (You can extract from PDFs using PyMuPDF)
resume_text = """
John Doe
Software Engineer | AI & ML Expert

Experience:
- Google (2020-2024): Worked on large-scale AI models and cloud computing.
- Microsoft (2016-2020): Developed distributed systems and enterprise software.

Education:
- B.Tech in Computer Science, MIT

Skills:
- Python, Java, TensorFlow, PyTorch
- Cloud Computing, Kubernetes, AWS
- System Design, Distributed Systems
"""

# 🔹 Resume Summarization Prompt
resume_template = """
Given the following resume information: {resume_text}

Generate:
1. A professional summary of the candidate.
2. Top 5 key skills.
3. Relevant work experience in bullet points.
"""

# Create Prompt Template
resume_prompt_template = PromptTemplate(
    input_variables=["resume_text"],
    template=resume_template
)

# Initialize OpenAI LLM
llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)

# Create the chain (Pipeline)
chain = resume_prompt_template | llm

# Invoke chain with resume text
res = chain.invoke(input={"resume_text": resume_text})

# Print the structured resume summary
print(res.content)
