import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توكن البوت الخاص بتليجرام
TELEGRAM_TOKEN = '7032866493:AAHZ8sIgaimA_gQRUI8Tn99qXb2DkPQ1EcM'
# مفتاح API الخاص بـ OpenAI
OPENAI_API_KEY = 'sk-None-9Dwb43GKAFSv1v57yRCKT3BlbkFJrrWWKbAVXoNalRuGZXTH'

# إعداد مفتاح API لـ OpenAI
openai.api_key = OPENAI_API_KEY

# دالة لمعالجة الرسائل
def handle_message(update: Update, context: CallbackContext) -> None:
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
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبًا! أنا بوت تليجرام متكامل مع ChatGPT.')

# إعداد وبدء البوت
def main() -> None:
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
