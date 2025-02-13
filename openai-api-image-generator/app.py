import boto3
from requests_aws4auth import AWS4Auth
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.openai import OpenAIEmbeddings

from langchain_community.vectorstores import OpenSearchVectorSearch
from opensearchpy import OpenSearch, RequestsHttpConnection



service = "es"
region = "us-east-1"
credentials = boto3.Session(profile_name='aws-rag-demo-1').get_credentials()

awsauth = AWS4Auth(credentials.access_key,credentials.secret_key,region, service, session_token=credentials.token)
client = boto3.client('sts', profile_name='aws-rag-demo-1')

search = OpenSearch(hosts=[{'host': opensearch_url, 'port': 443}], http_auth=awsauth,connection_class=RequestsHttpConnection)


'''loader = TextLoader("../vectordb_loaders/drugs.csv")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(openai_api_key = openai_api_key)

docsearch = OpenSearchVectorSearch.from_documents(
      docs,
      embeddings,
      opensearch_url=opensearch_url,
      http_auth=awsauth,
      timeout=300,
      use_ssl=True,
      verify_certs=True,
      connection_class=RequestsHttpConnection,
      index_name="test-index",
  )'''
