import openai

def generate_quiz(text):
    prompt = (
        "Με βάση το παρακάτω ελληνικό κείμενο, γράψε 3 ερωτήσεις πολλαπλής επιλογής με 4 επιλογές η καθεμία και σωστή απάντηση:\n\n"
        + text[:3000]
    )
    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response["choices"][0]["message"]["content"]
