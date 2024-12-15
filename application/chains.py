
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, name, qualification, score, college, email):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are {name}, a graduate in {studies} with an aggregate cgpa of {grade} from {college}. your are the person with a strong passion for leveraging technology to streamline business processes 
            and drive efficiency. During your academic journey, you actively participated in projects that involved automating workflows and 
            optimizing systems, which honed your problem-solving skills and deepened your understanding of process integration. 
            AND Through internships and hands-on experience, I have collaborated with teams to develop tailored solutions that enhanced scalability, 
            reduced costs, and improved overall operational efficiency.
            your strong interpersonal skills enable you to communicate effectively, work collaboratively, 
            and adapt quickly to dynamic environments, making you well-equipped to contribute meaningfully to any team.
            Your job is to write a cold email to the HR regarding the job mentioned above describing the capability of you
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase your portfolio: {link_list}
            Remember you are {name}, provide your {email} at last.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links, "name": name, "studies": qualification, "grade": score, "college": college, "email": email})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_KEY"))
