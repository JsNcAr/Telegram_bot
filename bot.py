#!/usr/bin/env python

# pylint: disable=unused-argument, wrong-import-position

# This program is dedicated to the public domain under the CC0 license.
"""

Simple Bot to send ip of personal server.

Note:

To use arbitrary callback data, you must install ptb via

`pip install python-telegram-bot[callback-data]`

"""
import asyncio

import logging

from telegram import Update

from telegram.ext import Application, CommandHandler, ContextTypes

import os

import datetime as dt

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)


# Define a few command handlers. These usually take the two arguments update and

# context.

# Best practice would be to replace context with an underscore,

# since context is an unused local variable.

# This being an example and not having context present confusing beginners,

# we decided to have it present as context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_html(
        "Hi! this bot sends you the ip of the server using <em>/send</em>.")


def ip_change() -> bool:
    """Sends the ip of the server."""
    with open("ip.txt", "r") as ip_file:
        ip = str(ip_file.read())
        os.system(
            "dig @resolver1.opendns.com myip.opendns.com +short > ip.txt")
        new_ip = str(ip_file.read())
    return ip != new_ip


def ip() -> str:
    """Sends the ip of the server."""
    os.system("dig @resolver1.opendns.com myip.opendns.com +short > ip.txt")
    with open("ip.txt", "r") as ip_file:
        ip = str(ip_file.read())
    return ip


async def send_changed_ip(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the ip of the server"""
    while True:
        if ip_change():
            ip = ip()
            await update.message.reply_text(ip)
            await asyncio.sleep(3600)


async def send_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the ip of the server"""
    ip = ip()
    await update.message.reply_text(ip)


def main() -> None:
    """Run bot."""

    # Create the Application and pass it your bot's token.
    with open("token.txt", "r") as token:
        tok = str(token.read())

    application = (Application.builder().token(tok).build())

    # Verify if ip has changed every hour and send it if it has

    application.add_handler(CommandHandler("send_changed", send_changed_ip))

    # on different commands - answer in Telegram

    application.add_handler(CommandHandler(["start", "help"], start))

    application.add_handler(CommandHandler("send", send_ip))

    application.run_polling()


if __name__ == "__main__":

    main()
