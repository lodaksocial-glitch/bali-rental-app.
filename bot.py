import telebot
import requests
import json

API_TOKEN = 'ТВОЙ_ТОКЕН_ОТ_BOTFATHER'
GOOGLE_SCRIPT_URL = 'ТВОЯ_ССЫЛКА_ИЗ_ШАГА_2'
ADMIN_ID = 12345678  # Твой ID (узнай в @userinfobot)

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['web_app_data'])
async def handle_web_app_data(message):
    # 1. Получаем данные из приложения
    raw_data = message.web_app_data.data
    data = json.loads(raw_data)
    data['user'] = message.from_user.username or message.from_user.first_name

    # 2. Отправляем в Google Таблицу
    try:
        requests.post(GOOGLE_SCRIPT_URL, json=data)
    except:
        print("Ошибка отправки в таблицу")

    # 3. Формируем сообщение для тебя (админа)
    report = (
        f"🔔 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"👤 Клиент: @{data['user']}\n"
        f"🚘 Модель: {data['model']}\n"
        f"📅 Срок: {data['dates']}\n"
        f"📍 Локация: {data['loc']}\n"
        f"💰 Сумма: {data['total']:,} IDR"
    )
    
    bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
    bot.send_message(message.chat.id, "✅ Спасибо! Заказ принят. Мы свяжемся с вами!")

bot.polling()
