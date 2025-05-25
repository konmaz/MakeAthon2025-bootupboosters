import pathlib

from io import BytesIO
from google import genai
from google.genai.types import File, GenerateContentConfig, FileData, Content, Part, UploadFileConfig
from pydantic import BaseModel
import streamlit as st



class QuizQuestion(BaseModel):
    question: str
    correct_answer: str
    incorrect_answers: list[str]


class FlashCard(BaseModel):
    prompt: str
    answer: str


class MindMap(BaseModel):
    markdown: str


client = genai.Client(api_key="AIzaSyA6hW_h-moKxXythxGYDCXYfykn9vzRzNA")


@st.cache_data
def upload_files(file: BytesIO, file_type: str) -> File:
    return client.files.upload(
        file=file,
        config=UploadFileConfig(mime_type=file_type)
    )


doc_url = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"

# Retrieve and encode the PDF byte
filepath = pathlib.Path(r"C:\Users\Konstantinos\Downloads\Church_history3.pdf")
# filepath.write_bytes(httpx.get(doc_url).content)


promptQuiz = "Create 20 Q&A in the form of in please respond only the JSON :[{'question':'Text in back', 'correct_answer':'Text in front', 'incorrect_answer':'Incorrect answer', 'incorrect_answer':'Incorrect answer'}]"
promptSummary = "Create a summary of all the materials."


def generate_content(files: list[File], youTubeURL: str) -> Content | list[File]:
    if youTubeURL is not None:
        content = Content(
            parts=[
                Part(
                    file_data=FileData(file_uri=youTubeURL))])
    else:
        content = files
    return content


def ai(files: list[File], youTubeURL: str, lan: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            system_instruction=f"Create a summary of all the materials Min 7 paragraphs. Please all your responses should be in {lan} language! Also don't say here is your summary show it directly!"),
        contents=generate_content(files, youTubeURL))
    print(response.text)
    return response.text


def ai_flash_cards(files: list[File], youTubeURL: str, lan: str) -> list[FlashCard]:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            response_schema=list[FlashCard],
            response_mime_type="application/json",
            system_instruction=f"Create 10 flashcards! Please all your responses should be in {lan} language!"),
        contents=generate_content(files, youTubeURL))
    print(response.text)
    return response.parsed


def ai_quiz(files: list[File], youTubeURL: str, lan: str) -> list[QuizQuestion]:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            response_schema=list[QuizQuestion],
            response_mime_type="application/json",
            system_instruction=f"Create 10 quiz questions. Please all your responses should be in {lan} language!"),
        contents=generate_content(files, youTubeURL))
    print(response.text)
    return response.parsed


def ai_mindmap(files: list[File], youTubeURL: str, lan: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            response_schema=MindMap,
            response_mime_type="application/json",
            system_instruction=f"""
            You are creating an in-depth MarkMap mindmap in {lan}
            Organize key Threat Intelligence points. Guidelines (apply to {lan}):
                           1. Max 4 primary nodes (top themes).
                           2. Max 4 secondary nodes per primary (context titles).
                           3. Sub-nodes: concise, relevant for threat analysts.
                           4. No icons/emojis. No trailing spaces. No parentheses/special chars in field names.
                           5. Escape/avoid special chars, e.g., `mail.kz` not `mail[.]kz`.
                           6. Enclose text with dashes if needed, not extra parentheses.
                           7.Ensure full MarkMap syntax compliance. No spaces between lines. No ``` at start/end
            """),
        contents=generate_content(files, youTubeURL)
    )
    print(response.text)
    x = f"{response.parsed.markdown}"
    print(x)
    return response.parsed.markdown
