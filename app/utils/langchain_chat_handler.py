from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from .langchain_url_handler import get_split_docs, get_vectorstore, find_answer
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import load_dotenv
import openai
from langchain.llms import OpenAI
from app.models import ProcessedDocument
from langchain.schema import Document
from langchain.memory import InMemoryEntityStore

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI()


def chat_template(user_input, context):
    template = """Assistant is a large language model trained by OpenAI.
    
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Also, some additional context may be provided, take it into consideration when building your answer, and correlate the context with your knowledge. context: {context}/
    
    {history}
    Human: {user_input}
    Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "user_input", "context"], template=template
    )
    formatted_prompt = prompt.format(
        user_input=user_input, context=find_answer(user_input), history=""
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=formatted_prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2),
    )

    output = chatgpt_chain.predict(user_input)

    return output
