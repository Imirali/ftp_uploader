import os
import logging
from datetime import datetime
from ftp_handler import check_ftp_connection, upload_files_sftp, process_local_file
from telegram_bot import send_telegram_message
from config import LOGS_BASE_DIR

def setup_logging():
    """
    установка логирования, делим файлы на месяцы
    """
    if not os.path.exits(LOGS_BASE_DIR):
        os.makedirs(LOGS_BASE_DIR)

    current_date = datetime.now()
    log_file_name = f"logs_{current_date.strftime('%Y_%m')}.txt"
    log_file_path = os.path.join(LOGS_BASE_DIR, log_file_name)

    file_exists = os.path.exists(log_file_path)
    
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        fromat="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode='a' if file_exists else 'w'

    )

def main():
    """
    ------------
    """
    # Проверяем соединения с сервером
    if not check_ftp_connection():
        send_telegram_message("error", "Не удалось подключиться к серверу")
        return
    
    # Загружаем файлы на сервер.
    uploaded_files = upload_files_sftp()

    if uploaded_files:
        process_local_file(uploaded_files)
        send_telegram_message("success", uploaded_files)
    else:
        send_telegram_message("error", "Нет файлов для загрузки или произошла ошибка.")
    
if __name__ == "__main__":
    main()