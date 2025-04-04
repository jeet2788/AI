from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from scrapin.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()

    print("Hello LangChain")

    summary_template = """
        Given the LinkedIn information {information} about a person, generate the following:

        1. **Short Summary**: A concise summary of their profile.
        2. **Interesting Facts**: Two unique or notable facts about them.

        Format:
        **Short Summary:** <summary>
        **Interesting Facts:**  
        - <fact 1>  
        - <fact 2>
        **Profile Score:** <score>/10  
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain = summary_prompt_template | llm
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/jeet-chatterjee-87622436/"
    )
    res = chain.invoke(input={"information": linkedin_data})
    print("\n--- LinkedIn Profile Summary ---\n")
    print(res.content.strip())  # Extracts the text content correctly
