import g4f
import telebot

# Replace with your Telegram bot token
bot = telebot.TeleBot("Token")

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, """
Привет меня создал компания Migen-AI(Создател Migen). Я могу быть медленным и вот поэтому подождите я не такой быстрый.(Я использую ChatGPT 3.5 TURBO)
""")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_request = message.text

    if user_request.lower() == "quit":
        bot.reply_to(message, "Goodbye!")
        return

    # Generate the full response
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_request}],
        stream=False,
    )

    # Send the entire response in one message
    bot.reply_to(message, response)

bot.polling()
