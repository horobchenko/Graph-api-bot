from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from services.llm_chain import answer_user_question

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Welcome to the real estate RAG bot. Send me a question and I will try to answer it from your indexed documents."
    )


@router.message()
async def handle_query(message: Message) -> None:
    if not message.text or message.text.startswith("/"):
        return

    try:
        answer = await answer_user_question(message.text)
        await message.answer(answer)
    except Exception as exc:
        await message.answer(f"I could not generate an answer right now: {exc}")
