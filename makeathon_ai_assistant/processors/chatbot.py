import os
from langchain_community.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

def create_qa_chain(full_text):
    return {"context": full_text}

def ask_question(chain, question):
    full_text = chain["context"]
    prompt = (
        "Answer the question based on the following content:\n\n"
        f"{full_text}\n\n"
        f"Question: {question}\nAnswer:"
    )

    # Ανάγνωση μεταβλητών από περιβάλλον
    llm = AzureChatOpenAI(
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        temperature=0,
    )

    response = llm([HumanMessage(content=prompt)])
    return response.content
