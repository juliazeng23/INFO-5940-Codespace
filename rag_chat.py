import streamlit as st
import os
from openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from pypdf import PdfReader

# Splits documents into chunks and returns the chunks
def get_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 350,
        chunk_overlap = 50
    )

    chunks = text_splitter.split_documents(documents)

    return chunks

# Creates embeddings for chunks and returns the vector database
def get_embeddings(vectorstore, chunks):
    vectorstore = Chroma(
        collection_name="embeddings",
        embedding_function=OpenAIEmbeddings(model="openai.text-embedding-3-large")
    )
    vectorstore.add_documents(chunks)

    # ids = vectorstore.get()["ids"]
    # print(f"Database Size: {len(ids)}")

    return vectorstore

# Returns database of embeddings of file chunks
def get_database(uploaded_files):
    vectorstore = Chroma(collection_name="embeddings")
    vectorstore._client.delete_collection("embeddings")
    
    for file in uploaded_files:
        filename = file.name
        _, file_ext = os.path.splitext(filename)

        # Read contents of uploaded file
        if file_ext == ".txt":
            file_content = file.read().decode("utf-8")
        elif file_ext == ".pdf":
            reader = PdfReader(file)
            file_content = ""
            for page in reader.pages:
                file_content += page.extract_text() + "\n"

        documents = [Document(page_content=file_content, metadata={"source": filename})]
        chunks = get_chunks(documents)
        vectorstore = get_embeddings(vectorstore, chunks)

    return vectorstore

# Joins documents together into one string
def format_docs(docs):
    return "\n\n---\n\n".join(d.page_content for d in docs)

# Finds top k relevant chunks and returns concatenated chunks
def get_top_k_docs(db, question, k=2):
    docs = db.similarity_search(question, k=k)
    context = format_docs(docs)

    # print(f"Context: {context}\n")

    return context

# Returns system prompt with relevant context from files
def get_system_prompt(context):
    return f"""You are a helpful assistant for question answering.
    Use ONLY the provided context to answer concisely (<=3 sentences).
    If the answer isn't in the context, say you don't know.

    Context:\n{context}
    """

# Gets response from model after retrieving relevant information from documents
def get_model_rag_response(db, question):
    llm = ChatOpenAI(
        model="openai.gpt-4o",
        temperature=0.2,
        streaming=True
    )

    context = get_top_k_docs(db, question)
    system_prompt = get_system_prompt(context)

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=question),
    ])

    return response


# Streamlit Application
client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu",
)

st.title("📝 File Q&A with OpenAI")
uploaded_files = st.file_uploader("Upload files", type=("txt", "pdf"), accept_multiple_files=True)

# Get vector database from uploaded files
if uploaded_files:
    db = get_database(uploaded_files)

# Get question from user
question = st.chat_input(
    "Ask something about the documents",
    disabled=not uploaded_files,
)

# Initial message
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about the article"}]

# Write existing chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Answer new question
if question and uploaded_files:
    # Append the user's question to the messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # Get and write model response
    with st.chat_message("assistant"):
        response_generator = get_model_rag_response(db, question)
        response = response_generator.content
        st.write(response)

    # print(f"Answer: {response}\n\n")

    # Append the model's response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": response})