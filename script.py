import streamlit as st
import io
from threading import Thread
import time

from google.genai.types import File, FileData
from streamlit import button

import gemini
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

# Page config
st.set_page_config(page_title="Smart Study Assistant", layout="wide")
st.title("📚 From Lecture to Learning")
st.markdown("Transform lecture content into structured, interactive study material.")

col1, col2 = st.columns(2)



with col1:
    st.header("Materials")
    tab_bring_data, tab_download, tab_youtube = st.tabs(["Bring your own data", "Download from e class", "YouTube"])
    with tab_bring_data:
        uploaded_files = st.file_uploader("Upload lecture files", type=["pdf"], accept_multiple_files=True)
    with tab_download:
        class_url = st.text_input("Enter e-learning platform URL")
    with tab_youtube:
        youtube_url = st.text_input("Enter YouTube video link")

    langauge = st.selectbox("Select material language", ("Greek", "English", "France", "Dutch", "Cantonese"))

    if button("h"):
        print(youtube_url)
        print(len(youtube_url))
    # ---- BUTTON ACTION ----
    if st.button("📥 Process Content") and uploaded_files:
        # Upload PDFs
        processed_files: list[File] = [
            gemini.upload_files(io.BytesIO(file.read()))
            for file in uploaded_files
        ]

        # Clear previous state
        for key in ['summary', 'flashcard_data', 'quiz_data', 'mindmap', 'current_question', 'score', 'answered', 'shuffled_answers']:
            st.session_state.pop(key, None)

        # Containers to live-update
        st.subheader("⏳ Generating Content...")
        summary_box = st.empty()
        flashcard_box = st.empty()
        quiz_box = st.empty()
        mindmap_box = st.empty()

        # Define thread class
        class TaskThread(Thread):
            def __init__(self, target_func, state_key, container):
                super().__init__()
                self.target_func = target_func
                self.state_key = state_key
                self.container = container
                add_script_run_ctx(self, get_script_run_ctx())

            def run(self):
                try:
                    result = self.target_func(processed_files, (youtube_url if len(youtube_url) != 0 else None), langauge)
                    st.session_state[self.state_key] = result
                    self.container.success(f"{self.state_key.capitalize()} ready ✅")
                except Exception as e:
                    self.container.error(f"Error in {self.state_key}: {e}")

        # Launch threads
        threads = [
            TaskThread(gemini.ai, 'summary', summary_box),
            TaskThread(gemini.ai_flash_cards, 'flashcard_data', flashcard_box),
            TaskThread(gemini.ai_quiz, 'quiz_data', quiz_box),
            TaskThread(gemini.ai_mindmap, 'mindmap', mindmap_box),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

with col2:
    st.header("📝 Summary")
    if st.session_state.get("summary"):
        st.write(st.session_state.summary)
    else:
        st.info("Summary will appear here after processing...")

st.markdown("---")
st.caption("Built with 💡 for the EY Makeathon 2025")
