# Graph API Bot Documentation

This folder contains the project documentation for the Telegram bot with Microsoft Graph and RAG capabilities.

## Project overview
- Telegram bot built with aiogram
- Microsoft Graph API integration for SharePoint/OneDrive access
- ChromaDB-backed RAG retrieval with OpenAI embeddings
- Local development scaffold for real estate document search

## Main entry points
- `main.py` starts the Telegram bot
- `services/graph_api.py` handles Microsoft Graph authentication and file access
- `services/rag_storage.py` indexes and searches documents
- `services/llm_chain.py` generates answers from retrieved context

## Setup notes
1. Copy `.env.example` to `.env` and fill in credentials.
2. Install dependencies with `python3 -m pip install -r requirements.txt`.
3. Run the bot with `python3 main.py`.
