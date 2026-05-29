from vector_store import get_vector_store

vector_store = get_vector_store()

vector_store.delete_collection()

print("Collection deleted")