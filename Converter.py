import telebot
from currency_converter import CurrencyConverter
from telebot import types

BOT_TOKEN = "6906494698:AAExoq6m9DAU7_I2vDTDItrL7VTDCLYhQtU"
currency = CurrencyConverter()
amount = 0

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,"Привет, введите сумму")
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text)
    except:
        bot.send_message(message.chat.id,"Повторите операцию ,вводим только числа")
        bot.register_next_step_handler(message,summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('USD/EUR',callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD',callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP',callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('RUB/USD',callback_data='rub/usd')
        markup.add(btn1,btn2,btn3,btn4)
        bot.send_message(message.chat.id, "Выберите пару валют", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Сумма должна быть больше нуля")
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    values = call.data.upper().split("/")
    res = currency.convert(amount,values[0],values[1])
    bot.send_message(call.message.chat.id, f"Получилось {res}, Введите следующую сумму")
    bot.register_next_step_handler(call.message, summa)
bot.infinity_polling()