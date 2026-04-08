import telebot

try:
    from config_local import BOT_TOKEN, CHANNEL_ID
except ImportError:
    from config import BOT_TOKEN, CHANNEL_ID

bot = telebot.TeleBot(BOT_TOKEN)


def send_note_to_channel(note):
    text = (
        f'Нова нотатка\n\n'
        f'Назва: {note.title}\n'
        f'Текст: {note.text}\n'
        f'Категорія: {note.category.title}\n'
        f'Нагадування: {note.reminder}'
    )
    bot.send_message(CHANNEL_ID, text)