from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import  openai
import sys
import logging

class Reference:
    '''
    A class to store previously response from the GhatGPT API
    '''

    def __init__(self) -> None:
        self.response = ""


load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TOKEN")

# model name
MODEL_NAME = "gpt-3.5-turbo-0613"

#Initialize bot and dispatcher
bot =Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

#Configure logging
logging.basicConfig(level=logging.INFO)

def clear_past():
    '''
    This function to clear the previous conversation and context,
    '''
    reference.response = ""


@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start`  command
    """

    await message.reply("Hi\nI am Tele Bot!\nPowered by Anurag. How can i assist you?")


@dispatcher.message_handler(commands = ['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and contest.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
                    Hi There, I'm chatGpt Telegarm bot created by Anurag! Please follow the commands..
        /start - to start the conversation 
        /clear - to clear the past conversation and context
        /help - to get this help menu.
        I hope this help, : 
    """
    await message.reply(help_command)


@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """A hendler to process the user'r input and generate a response using the chatGPT APT.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {"role":"assistant","content":reference.response},  #role assistant
            {"role":"user","content": message.text} #our query
        ]        
    )
    reference.response = response.choices[0].message.content
    print(f">>> chatGPT: \n\t {reference.response}")
    await bot.send_message(chat_id=message.chat.id, text = reference.response)


if __name__=="__main__":
    executor.start_polling(dispatcher, skip_updates=True)