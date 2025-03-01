import streamlit as st
import smtplib
import ssl
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from email.message import EmailMessage

def send_email(to_email, subject, body):
    sender_email = "*****************"  # Change to your email
    sender_password = "*******"  # Use an gmail app password (not your real password)

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error sending email: {e}" 
    

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # URL input
    url_input = st.text_input("🔗 Enter a URL:")

    # User details inputs
    name_input = st.text_input("📝 Enter your name:")
    qualification_input = st.text_input("🎓 Enter your highest qualification:")
    college_input = st.text_input("🏫 Enter your college name:")
    score_input = st.text_input("📊 Enter your score in the qualification:")
    experience_input = st.text_area("💼 Enter your experience (if any):")
    email_input = st.text_input("📧 Enter your email:")
    recipient_email = st.text_input("📨 HR/Recruiter Email:")

    # Submit button
    submit_button = st.button("🚀 🚀 Generate & Send Email")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email_body = llm.write_mail(job, links, name_input, qualification_input, score_input, college_input, email_input)
                st.code(email_body, language='markdown')
                if recipient_email:
                    status = send_email(recipient_email, "Application for Job Opportunity", email_body)
                    st.success(status)
                else:
                   st.warning("⚠️ Please enter a recipient email.")
        except Exception as e:
            st.error(f"⚠️ An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

