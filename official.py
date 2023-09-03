from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
from telegram.update import Update
from datetime import datetime
import mysql.connector

updater = Updater('6176096455:AAGsYTiDFbDAmcqIaGUkh9NCHX4JmM2dyZM')

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to Mybot!')

def help(update: Update, context: CallbackContext):
	update.message.reply_text('''These are the commands available in Mybot :-
	/start - Shows a welcome msg 
	/help - Shows the available commands
	/time - Shows the current time
    Hi/hi/Hello/hello - Provides your attendance''')

def time(update: Update, context: CallbackContext):
    now = datetime.now()
    date_time = now.strftime('%d/%m/%y, %H:%M:%S')
    update.message.reply_text(str(date_time))

def receive_contact(update: Update, context: CallbackContext):
    from_number = update['message']['contact']['phone_number']
    from_number = from_number[2:]
    print(from_number)
    db=mysql.connector.connect(database='sql6634321', host='sql6.freemysqlhosting.net', user='sql6634321', password='mcEuizbb2T')
    db1=db.cursor(buffered=True)
    db1.execute('SELECT * FROM `TABLE 2` WHERE `Student Ph no`=%s',(from_number,))
    st_det=db1.fetchone()
    if st_det is not None:
        update.message.reply_text("hello" +" " +str(list(st_det)[0])+" "+ "your attendance is"+" " +str(list(st_det)[2]))
    else:
        update.message.reply_text("""Can't fetch your attendance with this number!
        Try with another number""")

def send_contact(update: Update, context: CallbackContext):
    user_message = str(update.message.text).lower()

    if user_message in ("hello", "hi"):
        update.message.reply_text("To get your attendance provide your contact",reply_markup={
            "keyboard":[[{"text":"Send contact",
                    "request_contact": True}],["Cancel"]],
                        "resize_keyboard": True,
                        "one_time_keyboard": True 
        })
    else:
        update.message.reply_text("""To get your attendance send 'Hi' or 'Hello' """)

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('time', time))
updater.dispatcher.add_handler(MessageHandler(Filters.text, send_contact))
updater.dispatcher.add_handler(MessageHandler(Filters.contact, receive_contact)) 

if __name__=="__main__":
    updater.start_polling()