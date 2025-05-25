import streamlit as st
from pathlib import Path
from processors.pdf_parser import extract_text_from_pdf
from processors.summarizer import summarize_text
from processors.quiz_generator import generate_quiz

#Page configuration,
st.set_page_config(page_title="Smart Study Assistant", layout="wide")

#Sidebar settings,
with st.sidebar:
    st.title("⚙️ Settings")
    enable_summary = st.checkbox("Generate Summary", value=True)
    enable_flashcards = st.checkbox("Generate Flashcards", value=True)
    enable_chat = st.checkbox("Enable Chatbot Q&A", value=True)

#Main layout,
st.title("📚 From Lecture to Learning")
st.header("1️⃣ Upload Your Materials")

uploaded_files = st.file_uploader(
    "Upload lecture files (PDF)", type=["pdf"], accept_multiple_files=True
)

#Button: Process content,
if st.button("📥 Process Content") and uploaded_files:
    full_text = ""
    for file in uploaded_files:
        filepath = Path("data") / file.name
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(file.getbuffer())

        raw_text = extract_text_from_pdf(str(filepath))
        full_text += raw_text + "\n"

        if enable_summary:
            st.markdown(f"#### 📝 Summary for {file.name}")
            summary = summarize_text(raw_text)
            st.info(summary)

        if enable_flashcards:
            st.markdown(f"#### ❓ Quiz for {file.name}")
            quiz = generate_quiz(raw_text)
            st.code(quiz)

    # Setup chatbot after processing
    if enable_chat and full_text.strip():
        from processors.chatbot import create_qa_chain, ask_question
        st.session_state.qa_chain = create_qa_chain(full_text)
        st.session_state.ask_question = ask_question

# Chatbot Q&A interface
if enable_chat:
    st.header("💬 Ask Your Assistant")
    user_query = st.text_input("Ask a question about the content...")

    if user_query:
        if "qa_chain" not in st.session_state or "ask_question" not in st.session_state:
            st.warning("⚠️ Please upload and process a document first.")
        else:
            answer = st.session_state.ask_question(
                st.session_state.qa_chain, user_query
            )
            st.markdown("#### 📌 Answer")
            st.write(answer)