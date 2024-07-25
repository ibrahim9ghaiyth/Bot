import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import openai

app = Flask(__name__)

# إعداد متغيرات البيئة
TELEGRAM_TOKEN = os.getenv("7032866493:AAHZ8sIgaimA_gQRUI8Tn99qXb2DkPQ1EcM")
OPENAI_API_KEY = os.getenv("sk-None-2o0g4ci6cXMrtQpAqqatT3BlbkFJrxgYtnLQVST7IXo2lQ0U")

# إعداد البوت والموزع
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# إعداد مفتاح API لـ OpenAI
openai.api_key = OPENAI_API_KEY

# دالة لمعالجة الرسائل
def handle_message(update: Update, context) -> None:
    user_message = update.message.text
    response = get_chatgpt_response(user_message)
    update.message.reply_text(response)

# دالة لاستدعاء ChatGPT والحصول على استجابة
def get_chatgpt_response(user_message: str) -> str:
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

# دالة لبدء البوت
def start(update: Update, context) -> None:
    update.message.reply_text('مرحبًا! أنا بوت تليجرام متكامل مع ChatGPT.')

# إضافة المعالجات إلى الموزع
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# نقطة النهاية لـ webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)
