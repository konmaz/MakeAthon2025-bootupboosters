import pathlib
import types
from io import BytesIO
from google import genai
from google import *
from google.genai.types import File, GenerateContentConfig
from pydantic import BaseModel

class QuizQuestion(BaseModel):
    question: str
    correct_answer: str
    incorrect_answer: str
    incorrect_answer: str

class FlashCard(BaseModel):
    front: str
    back: str


client = genai.Client(api_key="AIzaSyA6hW_h-moKxXythxGYDCXYfykn9vzRzNA")


def upload_files(file: BytesIO) -> File:
    return client.files.upload(
        file=file,
        config=dict(mime_type='application/pdf')
    )


doc_url = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"

# Retrieve and encode the PDF byte
filepath = pathlib.Path(r"C:\Users\Konstantinos\Downloads\Church_history3.pdf")
# filepath.write_bytes(httpx.get(doc_url).content)


promptQuiz = "Create 20 Q&A in the form of in please respond only the JSON :[{'question':'Text in back', 'correct_answer':'Text in front', 'incorrect_answer':'Incorrect answer', 'incorrect_answer':'Incorrect answer'}]"
promptSummary = "Create a summary of all the materials."


def ai(files: list[File], lan: str) -> str:


    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            system_instruction=f"Create a summary of all the materials! You are an AI Teacher! Please all your responses should be in {lan} language!"),
        contents=files)
    print(response.text)
    return response.text


def ai_flash_cards(files: list[File], lan: str) -> list[FlashCard]:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            response_schema=list[FlashCard],
            response_mime_type="application/json",
            system_instruction=f"Please all your responses should be in {lan} language!"),
        contents=["Create 20 flashcards!"] + files)
    print(response.text)
    return response.parsed

def ai_quiz(files: list[File], lan: str) -> list[QuizQuestion]:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            response_schema=list[QuizQuestion],
            response_mime_type="application/json",
            system_instruction=f"Please all your responses should be in {lan} language!"),
        contents=["Create 20 quiz questions!"] + files)
    print(response.text)
    return response.parsed
