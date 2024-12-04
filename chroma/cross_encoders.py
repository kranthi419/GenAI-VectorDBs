import os

import openai
from openai import OpenAI

import chromadb
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import SentenceTransformerEmbeddingFunction

from sentence_transformers import CrossEncoder

from dotenv import load_dotenv, find_dotenv

from helper_functions import read_pdf, chunk_texts


_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ["OPENAI_API_KEY"]

openai_client = OpenAI()
chromadb_client = chromadb.Client()

embed_function = SentenceTransformerEmbeddingFunction()
chroma_collection = chromadb_client.create_collection("data_collection", embedding_function=embed_function)

cross_encoder = CrossEncoder("cross_encoder/ms-marco-MiniLM-L-6-v2")


def embed_document(documents):
    try:
        ids = [str(i) for i in range(len(documents))]
        chroma_collection.add(ids=ids, documents=documents)
    except Exception as e:
        print(e)


def rank_documents(query, documents):
    try:
        scored_docs = []
        pairs = [(query, doc) for doc in documents]
        scores = cross_encoder.predict(pairs)
        for i, score in enumerate(scores):
            scored_docs.append((documents[i], score))
        ranked_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)
        return ranked_docs
    except Exception as e:
        print(e)


if __name__ == "__main__":
    pdf_data = read_pdf("sample.pdf")
    documents = chunk_texts(pdf_data)
    embed_document(documents)
    query = "What is the capital of France?"
    results = chroma_collection.query(query, n_results=10, include=["documents", "embeddings"])
    retrieved_docs = results["documents"]
    ranked_docs = rank_documents(query, retrieved_docs)
    print(ranked_docs)
