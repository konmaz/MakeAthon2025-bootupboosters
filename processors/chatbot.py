from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

# Φόρτωση Azure OpenAI API key από περιβάλλον
os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")

# Φάκελος όπου αποθηκεύονται τα vectors (μπορείς να το αλλάξεις)
persist_directory = "./chroma_db"

def text_to_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def create_qa_chain(text):
    chunks = text_to_chunks(text)
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_texts(chunks, embeddings, persist_directory=persist_directory)
    vectordb.persist()  # Αποθήκευση vectors στον δίσκο
    retriever = vectordb.as_retriever(search_kwargs={"k":3})
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa_chain

def ask_question(chain, question):
    return chain.run(question)
