import asyncio
import logging
import openai

import markdown
from aiogram import Bot, Dispatcher, Router, flags, md
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import Settings
from html_to_markdown import markdown_to_html


router = Router()


class Chat(StatesGroup):
    """States for conversation flow"""
    messages = State()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Hi\! I can help you answer your questions\. Please enter your first question\.\n```\npre-formatted fixed-width code block written in the Python programming language\n```",
        parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(Chat.messages)
    
    
@router.message(Chat.messages)
@flags.chat_action(action="typing")
async def answer_question(message: Message, state: FSMContext):
    data = await state.get_data()
    question = message.text
    answer = ""
    
    messages = data.get("messages", [{
        "role": "system",
        "content": "You are a laconic assistant. You reply with brief, to-the-point answers with no elaboration."
    }])
    messages.append({
        "role": "user",
        "content": question
    })
    
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )
    
    answer = markdown_to_html(response['choices'][0].message.content)
        
    await message.reply(
        text=answer,
        parse_mode=ParseMode.HTML
    )
        
            
    messages.append({
        "role": "assistant",
        "content": answer
    })
    await state.update_data(messages=messages)
    

async def main():
    dp = Dispatcher()
    config = Settings()
    
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())
    
    bot = Bot(token=config.bot_token.get_secret_value())
    openai.api_key = config.openai_api_key.get_secret_value()
    openai.organization = config.openai_organization_id.get_secret_value()
    
    kwargs = {
        'config': config
    }

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), **kwargs)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        ...
    