import pathlib
import types
from functools import lru_cache
from io import BytesIO
from google import genai
from google import *
from google.genai.types import File, GenerateContentConfig
from pydantic import BaseModel

class QuizQuestion(BaseModel):
    question: str
    correct_answer: str
    incorrect_answers: list[str]

class FlashCard(BaseModel):
    prompt: str
    answer: str


client = genai.Client(api_key="AIzaSyA6hW_h-moKxXythxGYDCXYfykn9vzRzNA")

@lru_cache
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


async def ai(files: list[File], lan: str) -> str:


    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            system_instruction=f"Create a summary of all the materials! You are an AI Teacher! Please all your responses should be in {lan} language!"),
        contents=files)
    print(response.text)
    return response.text


async def ai_flash_cards(files: list[File], lan: str) -> list[FlashCard]:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            response_schema=list[FlashCard],
            response_mime_type="application/json",
            system_instruction=f"Please all your responses should be in {lan} language!"),
        contents=["Create 20 flashcards!"] + files)
    print(response.text)
    return response.parsed

async def ai_quiz(files: list[File], lan: str) -> list[QuizQuestion]:
    # create mock fake data just for debugging
    # mock_data = [
    #     QuizQuestion(
    #         question="What is the capital of France?",
    #         correct_answer="Paris",
    #         incorrect_answers=["London", "Berlin", "Madrid"]
    #     ),
    #     QuizQuestion(
    #         question="Who painted the Mona Lisa?",
    #         correct_answer="Leonardo da Vinci",
    #         incorrect_answers=["Michelangelo", "Van Gogh", "Picasso"]
    #     ),
    #     QuizQuestion(
    #         question="What is 2+2?",
    #         correct_answer="4",
    #         incorrect_answers=["3", "5", "6"]
    #     )
    # ]
    # return mock_data
    
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=GenerateContentConfig(
            response_schema=list[QuizQuestion],
            response_mime_type="application/json",
            system_instruction=f"Please all your responses should be in {lan} language!"),
        contents=["Create 2 quiz questions!"] + files)
    print(response.text)
    return response.parsed
