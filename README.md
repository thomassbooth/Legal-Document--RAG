# Retrieval Augmented Generation - System

## Overview
- This project implements a Retrieval-Augmented Generation (RAG) system using Python and a frontend built with Nextjs - TypeScript, and advanced retrieval strategies: Multi-Query, RAG Fusion It leverages Qdrant and uses streaming response mechanisms to delivery queries to the frontend. The system is designed to manage both English and Arabic versions of a legal document, routing queries through distinct index databases and utilizing a modular, containerized architecture.

- This project supports querying in Arabic, returning an Arabic response and also the same in English.

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
  - Handles user history

- **`connections`**
  - Class for handling connections with the websocket

- **`router.py`**
  - Holds our routes for the Fastapi server, this is just a websocket and history endpoint.

### rag-system-fe - frontend application (nextjs)

- Generic Nextjs app structure (App router + src directory)
  
## Running the application

1. **Setup environment variables**

    Ensure at the root of the directory, create a .env file and create a value called
    ```OPENAI_API_KEY=YOURAPIKEY```

1. **Build the application**

    Ensure youre at the root directory of the project

    ```bash
    docker-compose build
    docker-compose up -d
    ```

2. **Accessing the application**

    The frontend application is being hosted locally on port 3000:
    ```http://localhost:3000```

## Additions

- **Server Startup**
  - On startup of the server, it generates and stores the embeddings. This might take a couple of mins to do.


- **Qdrant dashboard**
  - Check your qdrant data is populated after server start up here: http://localhost:6333/dashboard
 
- **UserID**
  - At the top of the webpage there is a UserID feature, this is just to simulate someone logging in for history purposes. Please put in any ID you wish, ideally this would be done using an OAuth login utilizing JWTs to pass a user identifier between the server and client.
