from langchain_url_handler import *
from link_scraper import *
import os
from dotenv import load_dotenv
import openai
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ChatMessageHistory,ConversationBufferWindowMemory, ConversationBufferMemory

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

llm = OpenAI(temperature=0.8)


def generate_chat(history, user_input, context):
    context = llm_data
    chat_history = ChatMessageHistory()
    for message in history:
        if message['role'] == 'user':
            chat_history.add_user_message(message['text'])
        elif message['role'] == 'ai':
            chat_history.add_ai_message(message['text'])

    memory = ConversationBufferMemory(chat_memory=chat_history)

    prompt = PromptTemplate(
        input_variables=["history", "input", "context"],
        template="Assistant is a large language model trained by OpenAI."
                 "Assistant is designed to be able to assist with a wide range of tasks, from answering simple "
                 "questions to providing"
                 "in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is "
                 "able to generate"
                 "human-like text based on the input it receives, allowing it to engage in natural-sounding "
                 "conversations and provide"
                 "responses that are coherent and relevant to the topic at hand."
                 "Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is "
                 "able to process"
                 "and understand large amounts of text, and can use this knowledge to provide accurate and "
                 "informative responses to a"
                 "wide range of questions. Additionally, Assistant is able to generate its own text based on the "
                 "input it receives,"
                 "allowing it to engage in discussions and provide explanations and descriptions on a wide range of "
                 "topics."
                 "Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable "
                 "insights and"
                 "information on a wide range of topics. Whether you need help with a specific question or just want "
                 "to have a"
                 "conversation about a particular topic, Assistant is here to assist."
                 "{history}"
                 "the following contents are updates in the 'nextjs' framework. please update your knowledge base"
                 " according to it and assume its the latest update in the area: {context}"
                 "Human: {input};"
                 "Assistant:",
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=prompt,
        verbose=True,
        memory=memory,
    )

    output = chatgpt_chain.predict(input=user_input,context=context)
    # nesta funcao acima utilizaremos a logica da view para trazer o user_input  do front para o back 'seguir logicas'
    # dos projetos passados

    return output
