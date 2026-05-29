from langchain_postgres import PGVector

from config import CONNECTION
from embeddings import get_embeddings


def get_vector_store():

    return PGVector(
        embeddings=get_embeddings(),
        connection=CONNECTION,
        collection_name="documents"
    )