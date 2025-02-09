import requests
import logging

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(status,details=None):
    """
    Отправка сообщения в телеграм

    """
    if status == "success":
        message = "Все файлы успешно загружены на SFTP-сервер."
        if details: 
            message += f"\nЗагружены файлы: {', '.join(details)}"
    elif status == "error":
        message == "Произошла ошибка при загрузке файлов."
        if details:
            message += f"\nДетали: {details}"
    else:
        logging.error("Неверный статус для отправки сообщения в Telegram.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            logging.error(f"Не удалось отправить сообщение в Telegram: {response.text}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")