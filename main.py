import telebot
import requests

BOT_TOKEN = "6906494698:AAExoq6m9DAU7_I2vDTDItrL7VTDCLYhQtU"

bot = telebot.TeleBot(BOT_TOKEN)


def get_daily_horoscope(sign, day):
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params=params)

    return response.json()


@bot.message_handler(commands=["start"])
def send_welcome(message):
    print(message)
    bot.reply_to(message, f"Hello ,{message.from_user.first_name} Welcome to my new bot")


@bot.message_handler(commands=["horoscope"])
def sign_horoscope(message):
    text = "Hello , please write me your zodiac sign"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="html"
    )
    bot.register_next_step_handler(sent_msg, day_handler)


def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\n <b>TODAY</b>,<b>TOMORROW</b>"
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="html"
    )
    bot.register_next_step_handler(sent_msg, get_horoscope, str(sign).capitalize())


def get_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    horoscope_message = f"<b>Horoscope</b>\n {horoscope['data']['horoscope_data']}\n <b>Day{horoscope['data']['date']} </b>"
    bot.send_message(message.chat.id, "Your horoscope!!!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="html")


bot.infinity_polling()
