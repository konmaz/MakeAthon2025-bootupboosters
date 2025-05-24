import os
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Ρύθμιση περιβαλλοντικών μεταβλητών για Azure
# Βεβαιώσου ότι αυτές οι env vars έχουν οριστεί ΠΡΙΝ τρέξει ο κώδικας
os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = os.getenv("AZURE_OPENAI_ENDPOINT")
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

# Δημιουργία OpenAI client
client = OpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"))

# Φάκελος αποθήκευσης vector DB
persist_directory = "./chroma_db"

def text_to_chunks(text: str) -> list[str]:
    """
    Κόβει το κείμενο σε κομμάτια για ευκολότερη επεξεργασία.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    return splitter.split_text(text)

def create_qa_chain(text: str) -> RetrievalQA:
    """
    Δημιουργεί την αλυσίδα ερωταπαντήσεων με βάση το κείμενο.
    """
    chunks = text_to_chunks(text)

    # Δημιουργία embeddings με τον Azure OpenAI client
    embeddings = OpenAIEmbeddings(client=client)

    # Δημιουργία ή φόρτωση της βάσης vector με τα chunks
    vectordb = Chroma.from_texts(chunks, embeddings, persist_directory=persist_directory)
    vectordb.persist()

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # Δημιουργία LLM με Azure deployment name (βάλτο σωστά)
    llm = ChatOpenAI(client=client, model_name="gpt-4.1", temperature=0)

    # Δημιουργία αλυσίδας RetrievalQA
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa_chain

def ask_question(chain: RetrievalQA, question: str) -> str:
    """
    Κάνει ερώτηση στην αλυσίδα και επιστρέφει απάντηση.
    """
    return chain.run(question)
