from langchain.document_loaders import SeleniumURLLoader
from .link_scraper import *
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List

scraped_links = scrape_links(url=settings.NEXT_DOCS_URL)


def load_documents(scraped_links: list) -> List[Document]:
    documents = []

    for url in scraped_links:
        loader = SeleniumURLLoader(urls=[url])
        new_documents = loader.load()
        documents.extend(new_documents)

    return documents


# ------------------- embeddings -------------------------------
embeddings = OpenAIEmbeddings()


def embed_documents(documents):
    embedded_documents = []
    for doc in documents:
        embedded_doc = embeddings.embed_documents(doc.page_content)
        embedded_documents.append(embedded_doc)

    return embedded_documents
