import streamlit as st
from groq import Groq

st.title("👨‍💼📊📈📁 John Doe's Interactive Resume")
st.write(
    "Welcome to John Doe's personal chat bot to answer John's previous experiences and his skillsets. Ask away what you want to know!"
)

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

# with open('resume.txt') as f:
#     document = f.readlines()

# question = st.text_area(
#         "Ask questions about my experience and skills!",
#         placeholder="How many years of working experience do you have?",
#     )

# messages = [
#     {
#         "role": "user",
#         "content": f"I have put in my resume between <document> and </document>. Your job is to answer the questiosn that the recruiter has on my resume in a very professional and concise manner. Be helpful and provide additional information which the recuiter might want to know but have not asked in their question. By doing so the recruiter will want to ask more about my resume. The questions are between <question> and </question>. <document>{document}</document> <question>{question}</question>",
#     }
# ]

# stream = client.chat.completions.create(
#     messages=messages,
#     model="llama-3.3-70b-versatile",
#     stream=True
# )

# # Stream the response to the app using `st.write_stream`.
# st.write_stream(stream)


if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama-3.3-70b-versatile"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

