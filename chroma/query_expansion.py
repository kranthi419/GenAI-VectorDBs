import os

import openai
from openai import OpenAI

import chromadb
from chromadb.utils.embedding_functions.sentence_transformer_embedding_function import SentenceTransformerEmbeddingFunction


from dotenv import load_dotenv, find_dotenv

from helper_functions import read_pdf, chunk_texts


_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ["OPENAI_API_KEY"]

openai_client = OpenAI()
chroma_client = chromadb.Client()

embed_function = SentenceTransformerEmbeddingFunction()
chroma_collection = chroma_client.create_collection("data_collection", embedding_function=embed_function)


def embed_documents(documents):
    try:
        ids = [str(i) for i in range(len(documents))]
        chroma_collection.add(ids=ids, documents=documents)
    except Exception as e:
        print(e)


# Expansion with generated answer
# https://arxiv.org/abs/2305.03653
def hypothetical_answer_generation(query, model="gpt-4o-mini"):  # HyDe: Hypothetical Document Expansion
    # https://medium.aiplanet.com/advanced-rag-improving-retrieval-using-hypothetical-document-embeddings-hyde-1421a8ec075a
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. You will be shown the user's question. "
                       "Please provide a example answer to the user's question."
        },
        {"role": "user", "content": f"Question: {query}"}
    ]
    response = openai_client.chat.completions.create(model=model, messages=messages)
    content = response.choices[0].message.content
    return content


def sub_query_generation(query, model="gpt-4o-mini"):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. You will be shown the user's question. "
                       "Suggest Up to five additional related questions to help them find the information they need, for the provided question."
                       "Suggest only short questions without compound sentences. Suggest a variety of questions that cover different aspects of the topic."
                       "Make sure they are complete questions, and that they are related to the original question."
                       "Output one question per line. Do not number the questions."
        },
        {"role": "user", "content": f"Question: {query}"}
    ]
    response = openai_client.chat.completions.create(model=model, messages=messages)
    content = response.choices[0].message.content
    content = content.split("\n")
    return content


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
    response = openai_client.chat.completions.create(model=model, messages=messages)
    content = response.choices[0].message.content
    return content


if __name__ == "__main__":
    pdf_data = read_pdf("sample.pdf")
    pdf_data_documents = chunk_texts(pdf_data)
    embed_documents(pdf_data_documents)

    # HyDe: Hypothetical Document Expansion
    query = "what is attention?"
    hypothetical_answer = hypothetical_answer_generation(query)
    results = chroma_collection.query(query_texts=[hypothetical_answer], n_results=5)
    retrieved_documents = results["documents"][0]
    print(retrieved_documents)

    response = rag(query, retrieved_documents)
    print(response)

    # Sub-query generation
    sub_queries = sub_query_generation(query)
    results = chroma_collection.query(query_texts=sub_queries+["query"], n_results=5)
    unique_documents = set()
    for documents in retrieved_documents:
        for document in documents:
            unique_documents.add(document)
    print(unique_documents)

    response = rag(query, unique_documents)
    print(response)




