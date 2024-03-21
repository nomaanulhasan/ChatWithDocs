import streamlit as st
import anthropic
from dotenv import load_dotenv
# from PyPDF2 import PdfReader
import os

load_dotenv()

# def get_pdf_text(pdf_docs):
#   text = ""
#   for pdf in pdf_docs:
#     pdf_reader = PdfReader(pdf)
#     for page in pdf_reader.pages:
#       text += page.extract_text()
#   return text

with st.sidebar:
  anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", None) or st.session_state.get("ANTHROPIC_API_KEY", "")
  st.title(":books: Upload files here")
  uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

st.title(":books: Chat with Docs")

question = st.chat_input(
  placeholder="Ask something about the documents you have uploaded",
  disabled=not uploaded_file,
)

if uploaded_file and question and not anthropic_api_key:
  st.info("Please add your Anthropic API key to continue.")

if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
  st.chat_message(msg["role"]).write(msg["content"])

if uploaded_file and question and anthropic_api_key:
  article = uploaded_file.read().decode()
  prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
  {article}\n\n</article>\n\ngive me short answer for: {question}{anthropic.AI_PROMPT}"""
  user_asked = question

  client = anthropic.Client(api_key=anthropic_api_key)
  st.session_state.messages.append({"role": "user", "content": user_asked})
  st.chat_message("user").write(user_asked)

  response = client.completions.create(
    prompt=prompt,
    stop_sequences=[anthropic.HUMAN_PROMPT],
    # model="claude-v1",  # "claude-2" for Claude 2 model
    model="claude-2",
    temperature=0.8,
    # max_tokens=10,
    max_tokens_to_sample=100,
  )
  msg = response.completion
  st.session_state.messages.append({"role": "assistant", "content": msg})
  st.chat_message("assistant").write(msg)
