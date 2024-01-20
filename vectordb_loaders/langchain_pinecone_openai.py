from langchain.document_loaders import CSVLoader
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
import pinecone

class LangChainPineCOneOpenAILoader:
    def __init__(self, params):
        self.pinecone_api_key = params['pinecone_api_key']
        self.pinecone_api_env = params['pinecone_api_env']
        self.openai_api_key = params['openai_api_key']
        self.index_name = params['index_name']
        self.documents = params['documents']
    def load(self):
        embedding = OpenAIEmbeddings(openai_api_key = self.openai_api_key)
        # initialize pinecone
        pinecone.init(
            api_key=self.pinecone_api_key,  # find at app.pinecone.io
            environment=self.pinecone_api_env,  # next to api key in console
        )

        index_name = self.index_name
        # First, check if our index already exists. If it doesn't, we create it
        if index_name not in pinecone.list_indexes():
            # we create a new index
            pinecone.create_index(name=index_name, metric="cosine", dimension=1536)

        try:
            vectorstore = Pinecone.from_documents(documents = self.documents , embedding = embedding, index_name=index_name)
        except:
            raise BaseException("Problem in Loading data")
