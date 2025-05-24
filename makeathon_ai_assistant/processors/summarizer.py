from openai import OpenAI
import os

# Θέσε πρώτα τις απαραίτητες περιβαλλοντικές μεταβλητές
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT")  # πχ https://ey-makeathon.openai.azure.com/
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

# Δημιουργία client ΜΕΤΑ τον ορισμό των μεταβλητών
client = OpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"))

def summarize_text(text):
    prompt = (
        "Δώσε μια σύντομη περίληψη στα ελληνικά του παρακάτω περιεχομένου:\n\n"
        + text[:4000]
    )
    response = client.chat.completions.create(
        model="gpt-4.1",  # Βάλε εδώ το σωστό deployment name
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content
