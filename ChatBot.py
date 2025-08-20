import streamlit as st
from groq import Groq

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "GirlFriend"}
    ]

# Create Groq client
client = Groq(api_key='${{ secrets.API_KEY }}')

# Title
st.title("Chat with Alexa")

def on_submit():
    user_input = st.session_state.user_message

    if user_input.lower() == "bye":
        st.write("Bye!")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama3-8b-8192"
            ).choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

    # Clear the input box by resetting the session state here
    st.session_state.user_message = ""

# Text input with callback to clear after enter is pressed
st.text_input("Hello, how can I help you?", key="user_message", on_change=on_submit)

# Display chat history
st.subheader("Conversation History")
for msg in st.session_state.messages[1:]:  # Skip system prompt
    if msg["role"] == "user":
        st.markdown(f"*You:* {msg['content']}")
    elif msg["role"] == "assistant":

        st.markdown(f"*Alexa:* {msg['content']}")
