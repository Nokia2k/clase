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
import re
import netifaces
import platform
import nmap
import psutil
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

async def ping_ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    salida=""
    try:
        ip = context.args[0]
        for a in range(1,5):
            
                resultado_ping = ping(ip)
                if isinstance(resultado_ping, float):

                    resultado_ping = str(resultado_ping)
                    response = resultado_ping[4:7]
                    salida += str(ip) +" -> "+ str(response) + "ms\n"      

                elif isinstance(resultado_ping, bool):
                    salida += "IP: " + ip + " -> no response\n"
                    
                else:
                    salida +="IP: " + ip + " -> not reachable\n"
    except:
        salida = "** ERROR ** \n -> USO: /ping [IP]"

            
    await update.message.reply_text("** PING IP: " + ip+" **"+"\n\n"+salida )
    salida=""
    
#### esto para hacer ver los error log que se han pedido ####

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    salida = ''
    grep = 'error'
    cont = 0
    
    try:
        n = int(context.args[0])
        with open('/var/log/syslog', 'r') as logs:
            lines = logs.readlines()
            lines.reverse()
            for line in lines:
                if re.search(grep, line):
                    salida += line + "\n"
                    cont += 1
                    if cont >= n:
                        break
    except:
        salida = "** ERROR ** \n -> USO: /log [numero]"
    
    await update.message.reply_text("** Log de errores ** \n \n"+salida)
    salida=''

#### esto para hacer ver los puertos y programas que estan en uso ####

## SOLO FALTA ORDENARLO ##
 
async def port(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    salida=''
    var = psutil.net_connections(kind='inet')

    for line in var:
        local = str(line.status)
        puerto = str(line.laddr.port)
        pid = line.pid
        process = psutil.Process(pid)
        pro_name = str(process.name())

        if local == "ESTABLISHED":
            salida += " * Puerto: "+ puerto + " --  "+pro_name+"\n"
    
    await update.message.reply_text("** Puertos en uso ** \n \n"+salida)
    salida = ''

#### esto hace un nmap de la red que le diga ####
## HAY QUE ARREGLARLO PARA QUE SE VEA BONITO ##
nm = nmap.PortScanner()
async def nmap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    salida=''
    
    ip_probe = r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$'
    ip = context.args[0]
    if re.match(ip_probe, ip):

        hola = nm.scan(hosts=ip, arguments='-n -sP -PE -PA21,23,80,3389')
        if hola:
            hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
            for host, status in hosts_list:
                salida += host +"\n"
    else:
        
        salida = "Me has dado una ip incorrecta"
    
    await update.message.reply_text("** IP encendidas en la red ** \n \n"+salida)



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
    await update.message.reply_text(" -- Primer bot de Telegram -- \n** Instrucciones disponibles ** \n -> /start  \n -> /host \n -> /sys \n -> /net \n -> /ping [IP] \n -> /log [numero]\n -> /port \n -> /nmap [IP RED] \n -> /help")


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
    application.add_handler(CommandHandler("sys", so_info))
    application.add_handler(CommandHandler("net", ip_info))
    application.add_handler(CommandHandler("ping", ping_ip))
    application.add_handler(CommandHandler("log", log))
    application.add_handler(CommandHandler("port", port))
    application.add_handler(CommandHandler("nmap", nmap))




    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()