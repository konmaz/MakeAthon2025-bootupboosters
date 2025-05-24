import streamlit as st
from pathlib import Path

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

# Upload Section
st.header("1️⃣ Upload Your Materials")
uploaded_files = st.file_uploader(
    "Upload lecture files (PDF, DOCX, PPTX)",
    type=["pdf", "docx", "pptx"],
    accept_multiple_files=True
)

# YouTube Input Section
st.header("2️⃣ Or Paste a YouTube Video Link")
youtube_url = st.text_input("YouTube video link (with subtitles)")

# Submit Button
if st.button("📥 Process Content"):
    st.success("Processing your content... (placeholder)")
    # Placeholder for processing logic

# Results Section
st.header("3️⃣ Generated Study Materials")

if enable_summary:
    st.subheader("📝 Summary")
    st.info("Summary will appear here after processing...")

if enable_flashcards:
    st.subheader("🧠 Flashcards")
    st.warning("Flashcards will be generated here...")

if enable_chat:
    st.subheader("💬 Ask Your Assistant")
    user_query = st.text_input("Ask a question about the content...")
    if user_query:
        st.write("Chatbot response goes here...")

# Footer
st.markdown("---")
st.caption("Built with 💡 for the EY Makeathon 2025")
