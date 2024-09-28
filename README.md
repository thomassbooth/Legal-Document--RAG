# Retrieval Augmented Generation - System

## Overview
- This project implements a Retrieval-Augmented Generation (RAG) system using Python and a frontend built with Nextjs - TypeScript, and advanced retrieval strategies like Multi-Query, RAG Fusion, HyDE, and more. It leverages Qdrant and uses streaming response mechanisms to delivery queries to the frontend. The system is designed to manage both English and Arabic versions of a legal document, routing queries through distinct index databases and utilizing a modular, containerized architecture.

## Project Structure
### rag-system-be - backend server application

- **`ebeddings.py`**
  - Generates embeddings for both English and Arabic documents using openais pre-trained model.
  - Splits documents into smaller chunks to index phrases.
  - Populates a Qdrant (vector database) with the embeddings.

- **`main.py`**
  - Setsup the Fastapi backend

- **`retrieval.py`**
  - Retrieves relevent parts of the document based upon user queries.
  - Handles retrieval strategies:
    - MultiQuery
    - RAG Fusion


- **`router.py`**
  - Holds our routes for the Fastapi server, this is just a websocket endpoint.

### rag-system-fe - frontend application (nextjs)

- Generic Nextjs app structure (App router + src directory)
  
## Running the application

1. **Setup environment variables**

1. **Build the application**

    Ensure youre at the root directory of the project

    ```bash
    docker-compose build
    docker-compose up -d
    ```

2. **Accessing the application**

    The frontend application is being hosted at
    ```http://localhost:3001```

## Additions
