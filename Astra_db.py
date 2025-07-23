import os
from dotenv import load_dotenv
load_dotenv()
from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

os.environ['HUGGING_FACE_TOKEN'] = os.getenv('HUGGING_FACE_TOKEN')
api_endpoint = os.getenv('ASTRA_DB_ENDPOINT')
token = os.getenv('ASTRA_DB_TOKEN')

embeddings= HuggingFaceEmbeddings(model= 'allenai-specter')

def vector_database_creation():
    vector_Store = AstraDBVectorStore(
    embedding=embeddings,
    collection_name='hackathon',
    token=token,
    api_endpoint = api_endpoint,
    namespace = "default_keyspace"
)
    return vector_Store 