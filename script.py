import io

import streamlit as st
from google.genai.types import File

import gemini

# Set app title and layout
st.set_page_config(page_title="Smart Study Assistant", layout="wide")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("Customize your study assistant")
    enable_summary = st.checkbox("Generate Summary", value=True)
    enable_flashcards = st.checkbox("Generate Flashcards", value=True)
    enable_chat = st.checkbox("Enable Chatbot Q&A", value=True)

tab1, tab2 = st.tabs(["Bring your own data", "Download from e class"])


# App Title
st.title("📚 From Lecture to Learning")
st.markdown("Transform lecture content into structured, interactive study material.")
langauge = st.selectbox("Language", ("Greek", "English", "France"))
# Upload Section

with tab1:
    st.header("1️⃣ Upload Your Materials")
    uploaded_files = st.file_uploader(
        "Upload lecture files (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )
with tab2:
    st.header("Download from e learning platform")
    st.markdown("""
    Supported websites:
    - https://oyc.yale.edu/
    - https://opencourses.uoa.gr/
    """)

    class_url = st.text_input("Enter e learning platform URL")


flashCards, summary, quiz = None, None, None
# # YouTube Input Section
# st.header("2️⃣ Or Paste a YouTube Video Link")
# youtube_url = st.text_input("YouTube video link (with subtitles)")

# Submit Button
if st.button("📥 Process Content"):

    processed_files: list[File] = [
        gemini.upload_files(io.BytesIO(file.read()))
        for file in uploaded_files
    ]

    summary = gemini.ai(processed_files, langauge)
    flashCards = gemini.ai_flash_cards(processed_files, langauge)
    quiz = gemini.ai_quiz(processed_files, langauge)


# Results Section
st.header("3️⃣ Generated Study Materials")

if enable_summary:
    st.subheader("📝 Summary")
    if summary is None:
        st.info("Summary will appear here after processing...")
    else:
        st.write(summary)


if enable_flashcards:
    st.subheader("🧠 Flashcards")
    if flashCards is None:
        st.warning("Flashcards will be generated here...")
    else:
        st.write(flashCards)
st.subheader("Quiz")
if quiz is None:
    st.warning("Quiz will be generated here...")
else:
    st.write(quiz)

#
# if enable_chat:
#     st.subheader("💬 Ask Your Assistant")
#     user_query = st.text_input("Ask a question about the content...")
#     if user_query:
#         st.write("Chatbot response goes here...")

# Footer
st.markdown("---")
st.caption("Built with 💡 for the EY Makeathon 2025")
