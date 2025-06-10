import os
import streamlit as st
from openai import AsyncOpenAI
from agent import OpenAIChatCompletionsModel
from agent import Agent
from agent import RunConfig
from agent import Runner
import asyncio

from dotenv import load_dotenv
load_dotenv()

MODEL_NAME= 'gemini-2.0-flash'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
       api_key = OPENAI_API_KEY,
       base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=client
)

config = RunConfig(
        model=model,
        tracing_disabled=True
)

cv_agent = Agent(
       name = 'ss agent',
    instructions = (
    f"""You are a professional CV Maker Agent whose goal is to create a 100% hiring-worthy, impressive, and well-formatted CV based strictly on the user's form inputs like name, phone, email, address, about, education, and skills.

Generate the CV in clear, beautiful **Markdown format** with proper section titles using `###`, bullet points for skills and experience, and bold text for important elements like name, degree, and dates.

Use emojis where appropriate to make it friendly and modern. Add dividers (`---`) between sections to enhance readability.

Do NOT use code blocks or technical formatting. Make sure the layout is elegant and simple.

If any information is missing, still generate the best possible version with what’s provided. End with an encouraging message.

expand about me if small by adding user skills and experience make professional

just work with user data make expoerience quite good by your version
"""
)


,
    model = model
)

with st.form("cv_form"):
    st.subheader("👤 Bio Data")
    name = st.text_input("Full Name", placeholder="e.g. Laiba Noman")
    phone = st.text_input("Phone Number", placeholder="e.g. 03XXXXXXXXX")
    email = st.text_input("Email", placeholder="e.g. laiba@email.com")
    address = st.text_input("Address", placeholder="e.g. Bufferzone, Karachi")
    about = st.text_area("About Yourself", placeholder="Write a short bio about yourself...")

    st.subheader("🎓 Education")
    degree = st.text_input("Degree", placeholder="e.g. Intermediate,Bachelors")
    major_degree = st.text_input("Major Degree", placeholder="e.g. Medical,Engeenering")
    institute = st.text_input("Institute", placeholder="e.g. XYZ College")
    start_year = st.date_input("Start Year", value=None, help="Select start date of education")
    end_year = st.date_input("End Year", value=None, help="Select end date of education")
  


    st.subheader("💻 Skills")
    skills = st.text_area("Your Skills", placeholder="e.g. HTML, CSS, JavaScript, React, TypeScript, Tailwind")
    experience = st.text_area("Experience", placeholder="e.g. Internship,Job")

    st.checkbox("✅ I confirm the above information is accurate.")
    submitted = st.form_submit_button("✨ Generate CV")


def call_agent():
 if submitted:
    st.success("🎉 CV Data Collected Successfully!")
    st.snow()
    st.info("✨ Your CV is ready! You're going to shine bright! 💖")

    user_form = f"""
## 🧾 {name}'s CV
📞 **Phone:** {phone} &nbsp;&nbsp;&nbsp;&nbsp; 📧 **Email:** {email}  
🏠 **Address:** {address}

### 🙋‍♀️ About Me
{about}

### 🎓 Education
**{degree}** {major_degree} — *{institute}* ({start_year} -- {end_year})

### 💻 Skills
{skills}
\n
📑Experience:
{experience}
--------
"""
    if user_form:
      with st.spinner("Agent is thinking..."):
        result = asyncio.run(Runner.run(cv_agent, user_form, run_config=config))
        st.session_state.final_output = result.final_output
        st.write()
        st.success("✅ CV Generated!")

# Display Final CV Output (even after rerun)
    if "final_output" in st.session_state:
          st.subheader("📄 Your CV Output")
          st.write(st.session_state.final_output)
    
          st.download_button(
             label="⬇️ Download CV",
             data=st.session_state.final_output,
             file_name=f"{name.replace(' ', '_')}_CV.txt" if name else "cv.txt",
             mime="application/txt"
          )
if '__name__' == "__main__":
    call_agent()
