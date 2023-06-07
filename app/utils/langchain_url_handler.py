from langchain.document_loaders import UnstructuredURLLoader
from .link_scraper import *
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers.document_compressors import EmbeddingsFilter


def load_url_content(url: str):
    loader = UnstructuredURLLoader(urls=[url])
    data = loader.load()
    return data[0] if data else None


def load_urls_contents(urls: list):
    data = []
    for url in urls:
        url_data = load_url_content(url)
        if url_data:
            data.append(url_data)

    return data


urls = get_urls()

# the llm data will be used as a variable in the prompt template

# ------------------- embeddings -------------------------------
embeddings = OpenAIEmbeddings()


def embed_documents(contents):
    embedded_contents = []
    for content in contents:
        embedded_content = embeddings.embed_document(content)
        embedded_contents.append(embedded_content)

    return embedded_contents


llm_data_contents = load_urls_contents(urls)
llm_data_embedded = embed_documents(llm_data_contents)
