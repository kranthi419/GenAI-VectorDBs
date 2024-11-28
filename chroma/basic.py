import openai
import os

import chromadb
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import \
    SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv, find_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter

from openai import OpenAI
from pypdf import PdfReader


_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

openai_client = OpenAI()
chroma_client = chromadb.Client()


def read_pdf(file_path):
    reader = PdfReader(file_path)
    pdf_texts = [p.extract_text().strip for p in reader.pages]
    pdf_texts = [p for p in pdf_texts if p]
    return pdf_texts


def chunk_texts(texts):
    character_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""],
                                                        chunk_size=1000,
                                                        chunk_overlap=0)
    character_split_texts = character_splitter.split_text(texts)
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=250)

    token_split_texts = []
    for text in character_split_texts:
        token_split_texts.extend(token_splitter.split_text(text))

    return token_split_texts


def embed_documents(texts):
    try:
        ids = [str(i) for i in range(len(texts))]
        chroma_collection.add(ids=ids, documents=texts)
    except Exception as e:
        print(e)


def rag(question, retrieved_documents, model="gpt-4o-mini"):
    information = "\n\n".join(retrieved_documents)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. You will be shown the user's question, and the relevant information. "
                       "Answer the user's question using only this information."
        },
        {"role": "user", "content": f"Question: {question}. \n Information: {information}"}
    ]
    response = openai.chat.completions.create(model=model, messages=messages)
    content = response.choices[0].message.content
    return content


embedding_function = SentenceTransformerEmbeddingFunction()
chroma_collection = chroma_client.create_collection("data_collection", embedding_function=embedding_function)


if __name__ == "__main__":
    pdf_data = read_pdf("sample.pdf")
    pdf_data_documents = chunk_texts(pdf_data)
    embed_documents(pdf_data_documents)

    query = "what is attention?"
    results = chroma_collection.query(query_texts=[query], n_results=5)
    retrieved_documents = results["documents"][0]
    print(retrieved_documents)

    response = rag(query, retrieved_documents)
    print(response)

