import openai
import os

openai.api_key = os.getenv("AZURE_OPENAI_KEY")

def summarize_text(text):
    prompt = (
        "Δώσε μια σύντομη περίληψη στα ελληνικά του παρακάτω περιεχομένου:\n\n"
        + text[:4000]
    )
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response["choices"][0]["message"]["content"]
