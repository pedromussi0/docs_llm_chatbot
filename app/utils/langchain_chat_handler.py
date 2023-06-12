from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from .langchain_url_handler import get_split_docs, get_vectorstore, embed_documents
import os
from dotenv import load_dotenv
import openai
from langchain.llms import OpenAI
from app.models import ProcessedDocument

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI()


def get_llm_response(user_input):
    # Get split documents
    docs = get_split_docs()

    # Create a vector store
    vectorstore = get_vectorstore(docs)

    # Prepare the LLM chain
    prompt = "Relevant information:\n"

    for index, doc in enumerate(docs):
        prompt += f"\n[{index + 1}] {doc.page_content}\n"
        prompt += f"Source: {doc.metadata['source']}\n"

    prompt += f"\nQuestion: {user_input}\nAnswer:"

    # Run the LLM chain on the user input
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run(user_input)

    return response
