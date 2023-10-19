#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import socket
import netifaces
import platform
from ping3 import ping 

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


#### Pa conocer la ip y tal ####

lista_ip = netifaces.interfaces()
async def ip_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lista = ''
    for interfaces in lista_ip:
        try: 
            for addrs in netifaces.ifaddresses(interfaces)[netifaces.AF_INET]:
                
                lista += "IP de la maquina: "+ interfaces+": "+addrs['addr']+"\n" 
        except:
            pass        
    await update.message.reply_text(lista)

#### Esto pa hacer el ping y tal ####
response=" "
async def ping_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global response
    ip = context.args[0]
    for a in range(1,5):
        try:
        
            
            resultado_ping = str(ping(ip))
            if resultado_ping:
                response = resultado_ping[4:7:1]
                response += str(ip) +" -> "+ str(response) + "ms\n"      
            if resultado_ping is False:
                response = "Dame algo valido"  
            else:
                response = "Failed - Ping results: No response"
                #update.message.reply_text(response)
        except:
            print("Faild")

            
    await update.message.reply_text(response)
    response=""
    

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(" -- Primer bot de Telegram -- \n** Instrucciones disponibles ** \n -> /start  \n -> /host \n -> /sistema \n -> /ip \n -> /help")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def host_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Dar el hostname del dispositivo"""
    await update.message.reply_text(socket.gethostname())
    
async def so_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Dar el SO del dispositivo"""
    await update.message.reply_text(platform.platform())




def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6337533931:AAG9KS63MGWowKv67Xj323GoK4gqjVZZpp8").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("host", host_info))
    application.add_handler(CommandHandler("sistema", so_info))
    application.add_handler(CommandHandler("ip", ip_info))
    application.add_handler(CommandHandler("ping", ping_ip))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()