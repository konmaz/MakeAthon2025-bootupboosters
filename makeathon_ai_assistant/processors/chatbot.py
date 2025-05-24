import os
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Ρυθμίσεις Azure OpenAI (βεβαιώσου ότι έχουν οριστεί στο περιβάλλον σου)
os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

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

    embeddings = OpenAIEmbeddings(client=client)

    # Δημιουργούμε vectorstore FAISS αντί για Chroma για να αποφύγουμε το langchain_community
    vectordb = FAISS.from_texts(chunks, embeddings)

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(client=client, model_name="gpt-4.1", temperature=0)

    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    return qa_chain

def ask_question(chain, question):
    return chain.run(question)
