from openai import OpenAI
import os

client = OpenAI()

def summarize_text(text):
    prompt = (
        "Δώσε μια σύντομη περίληψη στα ελληνικά του παρακάτω περιεχομένου:\n\n"
        + text[:4000]
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content
