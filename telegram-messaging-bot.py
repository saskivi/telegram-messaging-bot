# -*- coding: utf-8 -*-

"""
This file implements a Telegram bot that uses the Telegram bot API to
forward messages sent to it to a certain chat anonymously. It is also possible
for the users in the chat to respond to the forwarded messages by replying to them.

You need to install Python Telegram Bot -library to run this bot.
pip install --user python-telegram-bot

API documentation: https://python-telegram-bot.readthedocs.io/en/stable/

You might need to change some of the settings of the bot in Botfather to get this
bot to work. For example the bot needs to be able to see all messages, not just commands
and be able to send messages.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

#Change this to your bot's token given by Telegrams Botfather.
BOT_TOKEN = ""

#Change this to your chat where you want you messages to be forwarded.
#To figure out the id, use for example the /whoami command of this bot in the chat.
CHAT_ID = 0

#Sent messages are saved here to enable replying.
sent_messages = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""

    update.message.reply_text("""Heippa! Kirjoita jotain niin se välittyy Kvantin toimitukselle. Viestit ovat täysin anonyymejä, mutta toimitus voi vastata viesteihisi botin välityksellä.

    Hi! Write something and it will be forwarded to the editorial staff of Kvantti. The messages are completely anonymous but the people of Kvantti can reply to your messages through the bot.""")


def error(bot, update, error):
    """Log Errors caused by Updates."""

    logger.warning('Update "%s" caused error "%s"', update, error)

def help(bot, update):
    start(bot, update)

def flush_messages(bot):
    """Flushes the messages send to the bot during downtime so that the bot
    does not start spamming when it gets online again."""

    updates = bot.get_updates()
    while updates:
        print("Flushing {} messages.".format(len(updates)))
        time.sleep(1)
        updates = bot.get_updates(updates[-1]["update_id"] + 1)

def whoami(bot, update):
    id = update.effective_message.chat.id
    bot.send_message(id, "The ID of this chat is: {}".format(id))


def robust_send_message(bot, msg, to, reply_id):
    """A robust method for forwarding different types of messages anonymously."""

    sent = None

    if msg.text:
        sent = bot.send_message(to, msg.text, reply_to_message_id=reply_id)
    elif msg.sticker:
        sent = bot.send_sticker(to, msg.sticker.file_id, reply_to_message_id=reply_id)
    elif msg.photo:
        sent = bot.send_photo(to, msg.photo[0].file_id, msg.caption, reply_to_message_id=reply_id)
    elif msg.video:
        sent = bot.send_video(to, msg.video.file_id, msg.caption, reply_to_message_id=reply_id)
    elif msg.video_note:
        sent = bot.send_video_note(to, msg.video_note.file_id, reply_to_message_id=reply_id)
    elif msg.document:
        sent = bot.send_document(to, msg.document.file_id, reply_to_message_id=reply_id)
    elif msg.voice:
        sent = bot.send_voice(to, msg.voice.file_id, reply_to_message_id=reply_id)
    elif msg.audio:
        sent = bot.send_audio(to, msg.audio.file_id, reply_to_message_id=reply_id)
    elif msg.location:
        sent = bot.send_location(to, location=msg.location, reply_to_message_id=reply_id)
    else:
        bot.send_message(msg.chat.id, "This message format is not supported :(")

    return sent


def send_from_private(bot, update):
    """Forward a private message sent for the bot to the receiving chat anonymously."""

    msg = update.effective_message

    sent_message = robust_send_message(bot, msg, CHAT_ID, None)
    sent_messages[sent_message.message_id] = (msg.chat.id, msg.message_id)


def reply(bot, update):
    """Forward reply from receiving chat back to the original sender."""

    id = update.effective_message.reply_to_message.message_id
    if id in sent_messages:
        org = sent_messages[id]
        robust_send_message(bot, update.effective_message, org[0], org[1])


def main():

    updater = Updater(token=BOT_TOKEN)

    dp = updater.dispatcher

    #Add handlers to the dispatchers. This defines what the bot does when it receives messages.
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("whoami", whoami))

    dp.add_handler(MessageHandler(Filters.private, send_from_private))
    dp.add_handler(MessageHandler(Filters.reply, reply))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()


