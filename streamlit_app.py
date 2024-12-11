import streamlit as st
from groq import Groq

st.title("👨‍💼📊📈📁 John Doe's Interactive Resume")
st.write(
    "Welcome to John Doe's personal chat bot to answer John's previous experiences and his skillsets. Ask away what you want to know!"
)

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

with open('resume.txt') as f:
    document = f.readlines()

question = st.text_area(
        "Ask questions about my experience and skills!",
        placeholder="How many years of working experience do you have?",
    )

messages = [
    {
        "role": "user",
        "content": f"I have put in my resume between <document> and </document>. Your job is to answer the questiosn that the recruiter has on my resume in a very professional and concise manner. Be helpful and provide additional information which the recuiter might want to know but have not asked in their question. By doing so the recruiter will want to ask more about my resume. The questions are between <question> and </question>. <document>{document}</document> <question>{question}</question>",
    }
]

stream = client.chat.completions.create(
    messages=messages,
    model="llama-3.3-70b-versatile",
    stream=True
)

# Stream the response to the app using `st.write_stream`.
st.write_stream(stream)
