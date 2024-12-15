import streamlit as st
from groq import Groq
import json
import os

# Initialize Groq client
client = Groq(
    api_key='YOUR_API_KEY',
)

# File for storing chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Function to load chat history from the JSON file
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save chat history to the JSON file
def save_chat_history(chat_history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(chat_history, file)

# Function to handle text-based chat
def get_text_response(user_input, history, model_name):
    try:
        # Append history to the payload for conversation continuation
        messages = history + [{"role": "user", "content": user_input}]
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Initialize session state for chat history if not present
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = load_chat_history()

# Sidebar for choosing chat module
menu = st.sidebar.selectbox("Choose Learning Module", ["Data Science", "Full Stack Development"])

# Track the current module in session state to reset the history when module changes
if "current_module" not in st.session_state:
    st.session_state["current_module"] = menu

# If module has changed, reset chat history
if st.session_state["current_module"] != menu:
    st.session_state["chat_history"] = []
    st.session_state["current_module"] = menu

# Set model based on selected learning module
if menu == "Data Science":
    model_name = "llama3-70b-8192"
    st.title("Hi! I'm a Data Scientist")
    st.markdown("Ask questions related to Data Science concepts, theories, or coding!")
elif menu == "Full Stack Development":
    model_name = "llama3-70b-8192"
    st.title("Hi! I'm a Full Stack Web Developer")
    st.markdown("Ask questions related to Full Stack Development concepts, theories, or coding!")

# Display chat history
for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.markdown(f"👤 **You**: {chat['content']}")
    else:
        st.markdown(f"🤖 **Assistant**: {chat['content']}")

# Input box for user message
user_input = st.text_input("You:", key="chat_input", placeholder="Enter your question or code...")

# Send button to submit input
if st.button("Send"):
    if user_input.strip():
        # Add user input to chat history
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        # Display the user input immediately
        st.markdown(f"👤 **You**: {user_input}")
        # Get assistant response from the selected model
        with st.spinner("Thinking..."):
            assistant_response = get_text_response(user_input, st.session_state["chat_history"], model_name)
            st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})
            # Show the response from the assistant
            st.markdown(f"🤖 **Assistant**: {assistant_response}")
            # Show the response from the assistant
            if 'code' in assistant_response:
                # If the assistant provides code, display it with a copy option
                st.code(assistant_response, language="python")
                st.markdown(f'<button onclick="copyCode()" id="copy-button">Copy Code</button>', unsafe_allow_html=True)

        # Save chat history to JSON file
        save_chat_history(st.session_state["chat_history"])

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state["chat_history"] = []
    save_chat_history([])

# Custom JavaScript for copying code (to be injected into the page)
st.markdown("""
    <script>
        function copyCode() {
            var code = document.querySelector('pre code').innerText;
            var textarea = document.createElement('textarea');
            textarea.value = code;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            alert('Code copied to clipboard!');
        }
    </script>
""", unsafe_allow_html=True)
