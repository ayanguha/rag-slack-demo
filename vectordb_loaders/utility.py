import logging
import json
import argparse
import boto3

from langchain.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter

from langchain_pinecone_openai import LangChainPineCOneOpenAILoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

epilog = '''
 Intended Use:
 Usage: This program is designed to help loading multiple vectorstore via command line options.
 \n :param: target-vector-store: Choose target vector store
 \n :param: embedding-llm-provider: Choose Embedding LLM Model

'''

def parse_args():
    parser = argparse.ArgumentParser(description = epilog)
    ### Key Choices
    parser.add_argument("--target-vector-store",
                        required=True,
                        type=str,
                        default='pinecone',
                        choices=['pinecone', 'opensearch'],
                        help="Choose a vector store.")
    parser.add_argument("--embedding-llm-provider",
                        required=True,
                        type=str,
                        default=0,
                        choices=['openai', 'bedrock'],
                        help="Choose a Embedding provider.")

    ### Openai Specific Params
    parser.add_argument("--openai-api-key",
                        type=str,
                        help="Required if LLM Provider is openai")

    ### Bedrock Specific Params
    parser.add_argument("--bedrock-model-name",
                        type=str,
                        default="amazon.titan-embed-text-v1",
                        choices=['amazon.titan-embed-text-v1'],
                        help="Required if LLM Provider is bedrock. Default is amazon.titan-embed-text-v1")
    parser.add_argument("--bedrock-region",
                        type=str,
                        default="us-east-1",
                        help="Required if LLM Provider is bedrock. Default is us-east-1")

    ### Pinecone Specific Params
    parser.add_argument("--pinecone-api-key",
                        type=str,
                        help="Required if vector database is pinecone")
    parser.add_argument("--pinecone-api-env",
                         type=str,
                         help="Required if vector database is pinecone")

    ### AWS OpenSearch Specific Params
    parser.add_argument("--opensearch-region",
                        type=str,
                        default="ap-southeast-2",
                        help="Required if vector database is opensearch")
    parser.add_argument("--opensearch-password",
                         type=str,
                         help="Required if vector database is opensearch")

    parser.add_argument("--index-name",
                        type=str,
                        default="rag-example")

    parser.add_argument("--recreate",
                        type=bool,
                        default=False)

    return parser.parse_known_args()

def arg_checks(args):
    if args.target_vector_store == 'pinecone':
        if not args.pinecone_api_key:
            raise BaseException("If VectorDB is pinecone, then pinecone_api_env is required")
        if not args.pinecone_api_env:
            raise BaseException("If VectorDB is pinecone, then pinecone_api_env is required")

    if args.target_vector_store == 'opensearch':
        if not args.opensearch_region:
            raise BaseException("If VectorDB is opensearch, then opensearch_region is required")
        if not args.opensearch_password:
            raise BaseException("If VectorDB is pinecone, then opensearch_password is required")

    if args.embedding_llm_provider == 'openai':
        if not args.openai_api_key:
            raise BaseException("If Embedding LLM is openai, then openai_api_key is required")

    if args.embedding_llm_provider == 'bedrock':
        if not args.bedrock_model_name:
            print("bedrock_model_name not provided. amazon.titan-embed-text-v1 is assumed")

        if not args.bedrock_region:
            print("bedrock_region not provided. us-east-1 is assumed")
    return True

def get_loadable_docs():
    try:
        loader = CSVLoader(file_path="drugs.csv",
                       source_column = 'drugName')
        documents = loader.load()
        text_splitter = CharacterTextSplitter(separator = "\n\n", chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
    except:
        raise BaseException("Can't Load or Split Data")

    return texts

def load(args, documents):
    if args.target_vector_store == 'pinecone' and args.embedding_llm_provider == 'openai':

        params = {
              'pinecone_api_key': args.pinecone_api_key,
              'pinecone_api_env': args.pinecone_api_env,
              'openai_api_key': args.openai_api_key,
              'index_name': args.index_name,
              'documents': documents,
        }
        loader = LangChainPineCOneOpenAILoader(params)
        loader.load()


def main():
    args, _ = parse_args()
    arg_checks(args)
    docs = get_loadable_docs()

    load(args, docs)

if __name__ == "__main__":
    main()
