import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from openai import OpenAI

# Ορισμός περιβαλλοντικών μεταβλητών (ιδανικά εκτός κώδικα)
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT")  # πχ https://ey-makeathon.openai.azure.com/
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

# Δημιουργία OpenAI client με το API key
client = OpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"))

def text_to_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    return splitter.split_text(text)

def create_qa_chain(text):
    chunks = text_to_chunks(text)

    embeddings = OpenAIEmbeddings(
        client=client,
        deployment="text-embedding-3-large"  # Βάλε εδώ το deployment name για embeddings
    )

    vectordb = FAISS.from_texts(chunks, embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        client=client,
        deployment="gpt-4.1",  # Βάλε εδώ το deployment name για GPT-4
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )

    return qa_chain

def ask_question(chain, question):
    return chain.run(question)
