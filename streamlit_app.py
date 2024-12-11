import streamlit as st
from groq import Groq

st.title("👨‍💼📊📈📁 John Doe's Interactive Resume")
st.write(
    "Welcome to John Doe's personal chat bot to answer John's previous experiences and his skillsets. Ask away what you want to know!"
)

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama-3.3-70b-versatile"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is up?"):
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["groq_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        # Ensure correct extraction of response content
        response_content = ""
        for chunk in stream:
            # Assuming chunk contains a 'text' field with the response
            if 'text' in chunk:
                response_content += chunk['text']
                st.write(chunk['text'])  # Stream the response

    # Append assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": response_content})
