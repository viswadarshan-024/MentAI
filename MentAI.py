import streamlit as st
from groq import Groq
import json
import os

# Initialize Groq client (add your groq API key)
client = Groq(
    api_key='YOUR_API_KEY',
)

CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

def save_chat_history(chat_history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(chat_history, file)

def get_text_response(user_input, history, model_name):
    try:
        messages = history + [{"role": "user", "content": user_input}]
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = load_chat_history()

menu = st.sidebar.selectbox("Choose Learning Module", ["Data Science", "Full Stack Development"])

if "current_module" not in st.session_state:
    st.session_state["current_module"] = menu

if st.session_state["current_module"] != menu:
    st.session_state["chat_history"] = []
    st.session_state["current_module"] = menu

if menu == "Data Science":
    model_name = "llama3-70b-8192"
    st.title("Hi! I'm a Data Scientist")
    st.markdown("Ask questions related to Data Science concepts, theories, or coding!")
elif menu == "Full Stack Development":
    model_name = "llama3-70b-8192"
    st.title("Hi! I'm a Full Stack Web Developer")
    st.markdown("Ask questions related to Full Stack Development concepts, theories, or coding!")

for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.markdown(f"👤 **You**: {chat['content']}")
    else:
        st.markdown(f"🤖 **Assistant**: {chat['content']}")

user_input = st.text_input("You:", key="chat_input", placeholder="Enter your question or code...")

if st.button("Send"):
    if user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        st.markdown(f"👤 **You**: {user_input}")
        with st.spinner("Thinking..."):
            assistant_response = get_text_response(user_input, st.session_state["chat_history"], model_name)
            st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})
            st.markdown(f"🤖 **Assistant**: {assistant_response}")
            if 'code' in assistant_response:
                st.code(assistant_response, language="python")
                st.markdown(f'<button onclick="copyCode()" id="copy-button">Copy Code</button>', unsafe_allow_html=True)

        save_chat_history(st.session_state["chat_history"])

if st.sidebar.button("Clear Chat"):
    st.session_state["chat_history"] = []
    save_chat_history([])

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
