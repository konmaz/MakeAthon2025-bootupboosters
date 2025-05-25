import itertools

import httpx
import streamlit as st
import io
from threading import Thread
import time

from google.genai.types import File, FileData
from streamlit import button

import gemini
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

import scrappers.openclass
from scrappers import yale

# Page config
st.set_page_config(page_title="Smart Study Assistant", layout="wide")
st.title("📚 From Lecture to Learning")
st.markdown("Transform lecture content into structured, interactive study material.")

col1, col2 = st.columns(2)

with col1:
    st.header("Materials")
    tab_bring_data, tab_download, tab_youtube = st.tabs(["💾 Bring your own data", "📦 Download from e class", "🎞️ YouTube"])
    with tab_bring_data:
        uploaded_files = st.file_uploader("Upload lecture files", type=["pdf", "png", "jpeg", "mp3", "mp4"],
                                          accept_multiple_files=True)
    with tab_download:
        st.info("Example links\n - https://opencourses.uoa.gr/modules/document/?course=THEOL2\n - https://oyc.yale.edu/history/hist-116")
        class_url = st.text_input("Enter e-learning platform URL")
    with tab_youtube:
        st.info("Example YouTube video link: https://www.youtube.com/watch?v=9hE5-98ZeCg")
        youtube_url = st.text_input("Enter YouTube video link")

    langauge = st.selectbox("What language would you like the content in?",
                            ("Greek", "English", "France", "Dutch", "Cantonese"))

    # ---- BUTTON ACTION ----
    if st.button("📥 Process Content") and (uploaded_files or class_url or youtube_url):
        if ".gr" in class_url:
            processed_files: list[File] = []
            urls: set[str] = scrappers.openclass.get_course_files(class_url)
            for i, url in enumerate(itertools.islice(urls, 2)):
                io.BytesIO(httpx.get(url).content)
                processed_files.append(gemini.upload_files(io.BytesIO(httpx.get(url).content), "application/pdf"))
                st.toast(f"Download file {url}")
        elif "yale.edu" in class_url:
            processed_files: list[File] = [
                gemini.upload_files(yale.serialize_transcripts_to_bytesio(yale.get_yale_transcripts(class_url)), "text/plain")
            ]
        else:
            # Upload PDFs
            processed_files: list[File] = [
                gemini.upload_files(io.BytesIO(file.read()), file.type)
                for file in uploaded_files
            ]

        # Clear previous state
        for key in ['summary', 'flashcard_data', 'quiz_data', 'mindmap', 'current_question', 'score', 'answered',
                    'shuffled_answers', 'slide_index', 'presentation']:
            st.session_state.pop(key, None)

        # Containers to live-update
        st.subheader("⏳ Generating Content...")
        summary_box = st.empty()
        flashcard_box = st.empty()
        quiz_box = st.empty()
        mindmap_box = st.empty()
        presentation = st.empty()


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
                    result = self.target_func(processed_files, (youtube_url if len(youtube_url) != 0 else None),
                                              langauge)
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
            TaskThread(gemini.ai_presentation, 'presentation', presentation)
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
