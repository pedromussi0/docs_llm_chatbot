from langchain.document_loaders import UnstructuredURLLoader
from link_scraper import *


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

llm_data = load_urls_contents(urls)
# the llm data will be used as a variable in the prompt template
