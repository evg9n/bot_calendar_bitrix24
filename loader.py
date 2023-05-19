from telebot import TeleBot
from config import TOKEN
from telebot.storage import StateMemoryStorage

storage = StateMemoryStorage()
bot = TeleBot(token=TOKEN, state_storage=storage)
