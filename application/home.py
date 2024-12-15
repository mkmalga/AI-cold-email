import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # URL input
    url_input = st.text_input("🔗 Enter a URL:", value="https://www.accenture.com/in-en/careers/jobdetails?id=ATCI-4302664-S1666145_en&title=Application%20Developer")

    # User details inputs
    name_input = st.text_input("📝 Enter your name:")
    qualification_input = st.text_input("🎓 Enter your highest qualification:")
    college_input = st.text_input("🏫 Enter your college name:")
    score_input = st.text_input("📊 Enter your score in the qualification:")
    experience_input = st.text_area("💼 Enter your experience (if any):")
    email_input = st.text_input("📧 Enter your email:")

    # Submit button
    submit_button = st.button("🚀 Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links, name_input, qualification_input, score_input, college_input, email_input)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"⚠️ An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
