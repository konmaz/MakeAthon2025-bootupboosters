import asyncio
import io

import streamlit as st
from google.genai.types import File

import gemini

# Set app title and layout
st.set_page_config(page_title="Smart Study Assistant", layout="wide")

# Sidebar

enable_summary = True
enable_flashcards = True
enable_chat = True

# App Title
st.title("📚 From Lecture to Learning")
st.markdown("Transform lecture content into structured, interactive study material.")

# Upload Section


col1, col2 = st.columns(2)

with col1:
    st.header("Materials")
    tab_bring_data, tab_download, tab_youtube = st.tabs(["Bring your own data", "Download from e class", "YouTube", ])

    with tab_bring_data:
        uploaded_files = st.file_uploader(
            "Upload lecture files",
            type=["pdf"],
            accept_multiple_files=True
        )
    with tab_download:
        st.markdown("""
           Examples:
           - https://oyc.yale.edu/astronomy/astr-160
           - https://opencourses.uoa.gr/
           """)
        class_url = st.text_input("Enter e learning platform URL")

    with tab_youtube:
        youtube_url = st.text_input("Enter YouTube video link")

    langauge = st.selectbox("The language of which the material will be generated", ("Greek", "English", "France", "Dutch", "Cantonese"))
    if st.button("📥 Process Content"):
        processed_files: list[File] = [
            gemini.upload_files(io.BytesIO(file.read()))
            for file in uploaded_files
        ]
        # clear quiz state
        for key in ['current_question', 'score', 'answered', 'shuffled_answers', 'quiz_data']:
            if key in st.session_state:
                del st.session_state[key]

        # Run all tasks in parallel
        async def process_all():
            return await asyncio.gather(
                gemini.ai(processed_files, langauge),
                gemini.ai_flash_cards(processed_files, langauge),
                gemini.ai_quiz(processed_files, langauge)
            )

        # Run the async functions
        summary, flashCards, st.session_state.quiz_data = asyncio.run(process_all())

summary = None
# # YouTube Input Section
# st.header("2️⃣ Or Paste a YouTube Video Link")
# youtube_url = st.text_input("YouTube video link (with subtitles)")

# Submit Button

with col2:
    st.header("📝 Summary")
    if summary is None:
        st.info("Summary will appear here after processing...")
    else:
        st.write(summary)

#
# if enable_chat:
#     st.subheader("💬 Ask Your Assistant")
#     user_query = st.text_input("Ask a question about the content...")
#     if user_query:
#         st.write("Chatbot response goes here...")

# Footer
st.markdown("---")
st.caption("Built with 💡 for the EY Makeathon 2025")
