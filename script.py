import io

import streamlit as st
from google.genai.types import File

from gm import foobar5

# Set app title and layout
st.set_page_config(page_title="Smart Study Assistant", layout="wide")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("Customize your study assistant")
    enable_summary = st.checkbox("Generate Summary", value=True)
    enable_flashcards = st.checkbox("Generate Flashcards", value=True)
    enable_chat = st.checkbox("Enable Chatbot Q&A", value=True)

# App Title
st.title("📚 From Lecture to Learning")
st.markdown("Transform lecture content into structured, interactive study material.")
langauge = st.selectbox("Language", ("Greek", "English", "France"))
# Upload Section
st.header("1️⃣ Upload Your Materials")
uploaded_files = st.file_uploader(
    "Upload lecture files (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)
flashCards, summary = None, None
# # YouTube Input Section
# st.header("2️⃣ Or Paste a YouTube Video Link")
# youtube_url = st.text_input("YouTube video link (with subtitles)")

# Submit Button
if st.button("📥 Process Content"):

    bytes2: list[File] = []
    for uploaded_file in uploaded_files:
        bytes2.append(foobar5.upload_files(io.BytesIO(uploaded_file.read())))

    summary = foobar5.ai(bytes2, langauge)
    flashCards = foobar5.ai_flash_cards(bytes2, langauge)


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
#
# if enable_chat:
#     st.subheader("💬 Ask Your Assistant")
#     user_query = st.text_input("Ask a question about the content...")
#     if user_query:
#         st.write("Chatbot response goes here...")

# Footer
st.markdown("---")
st.caption("Built with 💡 for the EY Makeathon 2025")
