#!/usr/bin/env python

# pylint: disable=unused-argument, wrong-import-position

# This program is dedicated to the public domain under the CC0 license.


"""

Simple Bot to send ip of personal server.


Usage:

Press Ctrl-C on the command line or send a signal to the process to stop the

bot.


Note:

To use arbitrary callback data, you must install ptb via

`pip install python-telegram-bot[callback-data]`

"""


import logging

from telegram import Update

from telegram.ext import Application, CommandHandler, ContextTypes

import os

import datetime as dt

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Define a few command handlers. These usually take the two arguments update and

# context.

# Best practice would be to replace context with an underscore,

# since context is an unused local variable.

# This being an example and not having context present confusing beginners,

# we decided to have it present as context.


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Sends explanation on how to use the bot."""
    await update.message.reply_text(
        "Hi! this bot sends you the ip of the server using /send."
    )


async def send_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send the ip of the server"""
    os.system("dig @resolver1.opendns.com myip.opendns.com +short > ip.txt")
    with open("ip.txt", "r") as ip_file:
        ip = str(ip_file.read())
    await update.message.reply_text(ip)


def main() -> None:

    """Run bot."""

    # Create the Application and pass it your bot's token.
    with open("token.txt", "r") as token:
        tok = str(token.read())

    application = (
        Application.builder()
        .token()
        .build()
    )

    # on different commands - answer in Telegram

    application.add_handler(CommandHandler(["start", "help"], start))

    application.add_handler(CommandHandler("send", send_ip))

    application.run_polling()

if __name__ == "__main__":

    main()

