from loader import extract_from_pdf_folder
from recursive_textsplitter import recursive_split
from Astra_db import vector_database_creation


# === Step 1: Load all PDFs ===
pdf_folder = r"C:\Users\rudra\Desktop\hackathon\pdf"  # Change this path as needed
all_docs = extract_from_pdf_folder(pdf_folder)
print("\n📄 All PDFs loaded and content extracted")

# === Step 2: Recursive Text Splitting ===
pages = recursive_split(all_docs)
print("\n✂️ Recursive splitting completed")

print(pages[0])

# === Step 3: Create vector store and embed documents ===
vector_store = vector_database_creation()
vector_store.add_documents(pages)
print("\n📦 Pages embedded and added to vector database")

# === Step 4: Create Retriever and RAG Chain ===
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={'k': 10, 'fetch_k': 30}
)


# === Step 5: Take Query Input and Generate Answer ===
query = input("\n❓ Enter your query: ")
answer = retriever.invoke(query)

print(answer)



