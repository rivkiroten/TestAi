import streamlit as st

from m3_p1_backend import call_llm
st.title("🤖 Languages Learning Assistant")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    
    # Dropdown for speaking language
    lang_speak = st.selectbox(
        "Language you speak:",
        ("English", "Hebrew", "Arabic", "Spanish", "French", "German", "Russian", "Chinese", "Japanese")
    )
    
    # Dropdown for language to teach
    lang_teach = st.selectbox(
        "Language to teach:",
        ("Hebrew", "English", "Arabic", "Spanish", "French", "German", "Russian", "Chinese", "Japanese")
    )
    
    # Dropdown for level
    level = st.selectbox(
        "Level:",
        ("Beginner", "Intermediate", "Advanced")
    )
    
    # Input for topic
    topic = st.text_input("Topic", "Topic")

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What can I help you with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- This is the "fix" ---
    # Get the response from your backend function
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_llm(
                user_input=prompt,
                lang_speak=lang_speak,
                lang_teach=lang_teach,
                level=level,
                topic=topic,
                history=st.session_state.messages
            )
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})