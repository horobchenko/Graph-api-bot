"""LLM orchestration module for the Telegram bot."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from config.settings import OPENAI_API_KEY
from services.rag_storage import RAGStorage


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful real estate assistant. Use the provided context to answer the user's question. "
            "If the context is insufficient, say so clearly and do not invent facts.",
        ),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ]
)


async def answer_user_question(question: str) -> str:
    """Retrieve relevant context and generate an answer using OpenAI chat models."""
    if not OPENAI_API_KEY:
        return "OpenAI API key is not configured. Add OPENAI_API_KEY to your .env file."

    storage = RAGStorage()
    results = storage.semantic_search(question, k=4)

    context = "\n\n".join(item["content"] for item in results if item.get("content"))
    if not context:
        return "No indexed documents were found. Please import documents into the ChromaDB first."

    model = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
    chain = PROMPT | model | StrOutputParser()
    return await __run_chain(chain, context=context, question=question)


async def __run_chain(chain, **kwargs: str) -> str:
    return chain.invoke(kwargs)
