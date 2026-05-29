# RAG System con LangChain, LangGraph y PGVector

Este proyecto implementa un sistema RAG (Retrieval-Augmented Generation) usando documentos PDF como fuente de contexto.
El objetivo es poder hacer preguntas y generar respuestas usando la información almacenada en los documentos cargados.


## Tecnologías usadas

* Python
* LangChain
* LangGraph
* PostgreSQL + PGVector
* Ollama
* Sentence Transformers
* Docker

---

## Cómo ejecutar el proyecto

### 1. Levantar PostgreSQL

```bash
docker compose up -d
```

Esto inicia la base de datos donde se almacenan los embeddings.

---

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 3. Procesar los documentos

```bash
python app/ingestion.py
```

Este script:

* carga los PDFs,
* divide el texto en fragmentos,
* genera embeddings,
* y los guarda en PGVector.

Los documentos deben estar dentro de la carpeta `data/`.

---

### 4. Ejecutar el sistema RAG

```bash
python app/rag_graph.py
```

Después de iniciar, puedes escribir preguntas directamente en la terminal.

---

## Ejemplos de uso

### Ejemplo 1

**Pregunta:**

```text
¿Qué es una ventana de contexto en un LLM?
```

**Respuesta esperada:**

```text
Una ventana de contexto es la cantidad máxima de tokens que el modelo puede "ver" a la vez y recordar en su memoria de trabajo. Cualquier cosa fuera de esa ventana se olvida.
```

---

### Ejemplo 2

**Pregunta:**

```text
¿Qué diferencia existe entre modelos abiertos y cerrados?
```

**Respuesta esperada:**

```text
"Modelos abiertos son aquellos que pueden aprender de grandes cantidades de datos y adaptarse a nuevos conocimientos o cambios en el entorno, mientras que los modelos cerrados son preprogramados para realizar una tarea específica y no pueden aprender ni adaptarse".
```

---

### Ejemplo 3

**Pregunta:**

```text
¿Cómo integrar esto con Kubernetes?
```

**Respuesta esperada:**

```text
Un token es la unidad atómica de los LLMs (Modelos de Lenguaje Grande) y se refiere a la forma en que estos modelos procesan el texto.

Un token no siempre equivale a una palabra. Esto se debe a que los LLMs utilizan un tokenizer aprendido (BPE - Sub-Word Tokenization) que divide el texto en sub-palabras, es decir, palabras que se han encontrado con frecuencia en la entrenada red y que son optimezadas para la tarea de entrenamiento. Esto significa que un token puede ser una sub-palabra que no tiene exactamente la misma estructura o contenido que una palabra individual.
```

---

## Estructura del proyecto

```text
rag-system-feature-initial_setup/
├── app/
│   ├── config.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── vector_store.py
│   ├── ingestion.py
│   └── rag_graph.py
├── data/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Configuración

En `app/config.py` se puede cambiar la conexión a PostgreSQL o el modelo utilizado.

```python
CONNECTION = "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "llama3.2"
```

---

### Si Ollama no responde

```bash
ollama serve
ollama pull llama3.2
```

---

