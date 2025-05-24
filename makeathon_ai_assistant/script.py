import streamlit as st
from pathlib import Path
from processors.pdf_parser import extract_text_from_pdf
from processors.summarizer import summarize_text
from processors.quiz_generator import generate_quiz

st.set_page_config(page_title="Smart Study Assistant", layout="wide")

with st.sidebar:
    st.title("⚙️ Settings")
    enable_summary = st.checkbox("Generate Summary", value=True)
    enable_flashcards = st.checkbox("Generate Flashcards", value=True)
    enable_chat = st.checkbox("Enable Chatbot Q&A", value=True)

st.title("📚 From Lecture to Learning")
st.header("1️⃣ Upload Your Materials")
uploaded_files = st.file_uploader(
    "Upload lecture files (PDF)", type=["pdf"], accept_multiple_files=True
)

if st.button("📥 Process Content") and uploaded_files:
    full_text = ""
    for file in uploaded_files:
        filepath = Path("makeathon_ai_assistant/data") / file.name
        with open(filepath, "wb") as f:
            f.write(file.getbuffer())
        raw_text = extract_text_from_pdf(str(filepath))
        full_text += raw_text + "\n"

        if enable_summary:
            summary = summarize_text(raw_text)
            st.markdown("#### 📝 Περίληψη")
            st.info(summary)

        if enable_flashcards:
            quiz = generate_quiz(raw_text)
            st.markdown("#### ❓ Quiz")
            st.code(quiz)

    if enable_chat:
        from processors.chatbot import create_qa_chain, ask_question
        st.session_state.qa_chain = create_qa_chain(full_text)

if enable_chat:
    st.header("💬 Ask Your Assistant")
    user_query = st.text_input("Ask a question about the content...")
    if user_query:
        if "qa_chain" not in st.session_state:
            st.warning("Please upload and process a document first.")
        else:
            answer = ask_question(st.session_state.qa_chain, user_query)
            st.write(answer)
