#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
label = ''
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def echo(update, context):
    """Echo the user message."""
    print(update)
    update.message.reply_text('Bon dia '+ update['message']['chat']['first_name'] + " espero que estiguis calmada perque us ve una de bona a sobre. El qui hagi trobat les meves investigacions no podrà resistir-se a continuar la cerca de la veritat. Si has arribat fins aqui vol dir que ja has trobat la maleta. Per activar l'intel·ligència artificial que és una còpia de mi, escriu /start")



"""
def video(update, context):
    global label
    label = ' '.join(context.args)
    if label == '':
        update.message.reply_text('Add the label of the object after /video')
    else:
        update.message.reply_text('Go ahead, send a video to save.')


def save_img(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('input/photo')
    update.message.reply_text('Photo received! Processing...')

    proc = subprocess.Popen(['python3', 'predict.py',  '-iphoto'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = proc.communicate()[0]

    update.message.reply_text(out.decode("utf-8"))
"""
GENDER, PHOTO, LOCATION, BIO = range(4)


def start(update, context):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER


def gender(update, context):
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')

    return LOCATION


def skip_photo(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(open('token.txt').read()[:-1], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    conv_handler = ConversationHandler(
         entry_points=[CommandHandler("start", start)],

         states={
             GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],

             PHOTO: [MessageHandler(Filters.photo, photo),
                     CommandHandler('skip', skip_photo)],

             LOCATION: [MessageHandler(Filters.location, location),
                        CommandHandler('skip', skip_location)],

             BIO: [MessageHandler(Filters.text & ~Filters.command, bio)]
         },

         fallbacks=[CommandHandler('cancel', cancel)]
     )
    dp.add_handler(conv_handler)

    #dp.add_handler(CommandHandler("train", train))
    #dp.add_handler(CommandHandler("predict", predict))

    dp.add_handler(MessageHandler(Filters.text, echo))
    #dp.add_handler(MessageHandler(Filters.video, process_video))
    #dp.add_handler(MessageHandler(Filters.photo, save_img))


    # log all errors
    #dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
