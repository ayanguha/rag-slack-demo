import requests
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Pinecone
import pinecone
import os, json


prompt_template = '''You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
   If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
   Question: {question}
   Context: {context}
   Answer:
'''

def pinecone_retriever():
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),  # find at app.pinecone.io
        environment=os.getenv("PINECONE_ENV"),  # next to api key in console
    )
    embedding = OpenAIEmbeddings(openai_api_key = os.getenv('OPENAI_API_KEY'))
    index_name = "langchain-demo"
    index = pinecone.Index(index_name)
    p = Pinecone(index = index, embedding = embedding, text_key = 'text')
    return p.as_retriever(search_type="similarity",
                          search_kwargs={"k": 3})

def ask(query):
    retriever = pinecone_retriever()
    retrieved_docs = retriever.invoke(query)
    prompt = PromptTemplate.from_template(template=prompt_template)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key = os.getenv('OPENAI_API_KEY'))
    qa_chain = RetrievalQA.from_chain_type(llm = llm, retriever = retriever, chain_type_kwargs={"prompt": prompt})
    result = qa_chain({"query": query})
    llm_response = result['result']
    return llm_response

def post_to_slack(msg, response_url):
    url = os.getenv('SLACK_POST_URL')
    data = {"text":msg}
    resp = requests.post(response_url, json = data)
    return resp

def handler(event, context):

    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)
    body = json.loads(message)
    print(body)
    user_msg = body['msg']
    response_url = body['response_url']
    llm_response = ask(user_msg)
    resp = post_to_slack(llm_response, response_url)
    return {'final': True}
