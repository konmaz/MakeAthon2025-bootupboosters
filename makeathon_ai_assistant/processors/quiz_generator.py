import os
from openai import AzureOpenAI

# Ρύθμιση περιβαλλοντικών μεταβλητών πριν τον client
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

client = AzureOpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"))

def generate_quiz(text):
    prompt = (
        "Με βάση το παρακάτω ελληνικό κείμενο, γράψε 3 ερωτήσεις πολλαπλής επιλογής με 4 επιλογές η καθεμία και σωστή απάντηση:\n\n"
        + text[:3000]
    )
    response = client.chat.completions.create(
        model="gpt-4.1",  # Βάλε εδώ το deployment name σου
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content
