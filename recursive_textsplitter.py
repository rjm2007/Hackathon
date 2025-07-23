from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Define recursive splitter with customizable params
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

def recursive_split(all_docs: list[Document]) -> list[Document]:
    return text_splitter.split_documents(documents=all_docs)

