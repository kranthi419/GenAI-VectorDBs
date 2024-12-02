from pypdf import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter


def read_pdf(file_path):
    parser = PdfReader(file_path)
    parsed_texts = [p.extract_text().strip() for p in parser.pages]
    parsed_texts = [p for p in parsed_texts if p]
    return parsed_texts


def chunk_texts(texts, chunk_size=1000, chunk_overlap=0, token_based_chunk=True):
    character_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", ". ", " ", ""],
                                                        chunk_size=chunk_size,
                                                        chunk_overlap=chunk_overlap)
    list_of_chunked_texts = character_splitter.split_text(texts)

    if token_based_chunk:
        token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=250)
        token_based_chunked_texts = []
        for text in list_of_chunked_texts:
            token_based_chunked_texts.extend(token_splitter.split_text(text))
    else:
        token_based_chunked_texts = list_of_chunked_texts
    return token_based_chunked_texts
