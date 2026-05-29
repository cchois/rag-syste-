from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector


CONNECTION = (
    "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"
)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def ingest_document(path):

    # cargar PDF
    loader = PyPDFLoader(path)

    docs = loader.load()

    print(f"Loaded {len(docs)} pages")


    # dividir en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(docs)

    print(f"Created {len(chunks)} chunks")


    # conectar vector store
    vector_store = PGVector(
        embeddings=embeddings,
        connection=CONNECTION,
        collection_name="documents"
    )


    vector_store.add_documents(chunks)

    print("Documents stored successfully!")


if __name__ == "__main__":
    import os
    data_dir = "data"
    for filename in os.listdir(data_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(data_dir, filename)
            print(f"Processing {pdf_path}...")
            ingest_document(pdf_path)