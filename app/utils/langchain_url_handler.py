from langchain.document_loaders import UnstructuredURLLoader
from .link_scraper import *
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List


def load_documents(scraped_links: list) -> List[Document]:
    loader = UnstructuredURLLoader(urls=scraped_links)

    documents = []

    for url, content in zip(scraped_links, loader.load()):
        document = Document(content=content)
        documents.append(document)

    return documents


scraped_links = scrape_links(url=settings.NEXT_DOCS_URL)


# ------------------- embeddings -------------------------------
embeddings = OpenAIEmbeddings()


def embed_documents(documents):
    embedded_documents = []
    for doc in documents:
        embedded_doc = embeddings.embed_document(doc.content)
        embedded_doc.metadata.update({"url": doc.url})
        embedded_documents.append(embedded_doc)

    return embedded_documents