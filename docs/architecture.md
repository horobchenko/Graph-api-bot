# Architecture Overview

## Components

### Telegram bot
- Uses `aiogram` for async messaging.
- The main handler responds to `/start` and user questions.

### Microsoft Graph integration
- Uses `msal` and `aiohttp`.
- Connects to SharePoint or OneDrive with application-only (Client Credentials) authentication.

### RAG pipeline
- Downloads or indexes documents from SharePoint/OneDrive.
- Splits documents into chunks using `RecursiveCharacterTextSplitter`.
- Creates embeddings with OpenAI.
- Stores them in ChromaDB for semantic search.

### LLM answer generation
- Retrieves matched chunks.
- Sends them to GPT-4o as context.
- Returns grounded responses to the user.
