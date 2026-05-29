# Este archivo implementa el flujo RAG (Retrieval-Augmented Generation) usando LangGraph
# Orquesta la recuperación de documentos y la generación de respuestas

from typing import TypedDict

from langgraph.graph import StateGraph, END

from vector_store import get_vector_store
from llm import get_llm


# Inicializar componentes
vector_store = get_vector_store()
llm = get_llm()


# Grafo RAG con las variables que se pasarán entre nodos
class RAGState(TypedDict):
    question: str  # Pregunta del usuario
    context: str  # Contexto recuperado de los documentos
    answer: str  # Respuesta generada por el LLM


def retrieve(state: RAGState):
    # Busca los documentos más similares a la pregunta en el vector store
    results = vector_store.similarity_search(
        state["question"],
        k=3,  # Número de chunks a recuperar
    )

    # Combina el contenido de los documentos recuperados en un solo contexto
    context = "\n\n".join(doc.page_content for doc in results)

    return {"context": context}


def generate(state: RAGState):
    # Crea el prompt para el LLM usando el contexto recuperado y la pregunta
    prompt = f"""
You are a helpful assistant.

Use ONLY the provided context.

If the answer is not present in the context say:

"I could not find the answer in the retrieved documents"

Context:
{state["context"]}

Question:
{state["question"]}

Answer:
"""

    # Invoca el LLM con el prompt para generar la respuesta
    answer = llm.invoke(prompt)

    return {"answer": answer}


# Construye el grafo de estado que define el flujo RAG
graph = StateGraph(RAGState)

# Añade los nodos (funciones) al grafo
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

# Define el punto de entrada y las transiciones entre nodos
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

# Compila el grafo para hacerlo ejecutable
app = graph.compile()


# Bucle principal que permite al usuario hacer preguntas continuamente
if __name__ == "__main__":
    while True:
        # Solicita una pregunta al usuario
        question = input("\nAsk a question ('exit' to quit): ")

        # Permite salir del bucle escribiendo 'exit'
        if question.lower() == "exit":
            break

        # Ejecuta el grafo RAG con la pregunta como entrada
        result = app.invoke({"question": question})

        # Muestra la respuesta generada
        print("\nAnswer:\n")
        print(result["answer"])

