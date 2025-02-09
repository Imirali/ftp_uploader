# Модуль для работы с операционной системой(пути к файлам, создание директорий)
import os 
# Модуль для работы с датой и временем
import datetime
# Модуль для логирования
import logging
# Модуль для работы с файлами и папками (перемещение, клонирование)
import shutil
# библиотека для работы с SFTP
import paramiko
from config import SFTP_SERVER, SFTP_USER, SFTP_PASSWORD, SFTP_REMOTE_DIR


def check_ftp_connection():
    """
    Функция проверки соединения с сервером.
    """
    try:
        transport = paramiko.Transport((SFTP_SERVER,22)) #Объект для подключения к серверу
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)#авторизация
        sftp = paramiko.SFTPClient.from_transport(transport)#Объект сфтклиент на основе подключения

        if sftp: #Если подключение успешно
            logging.info('Соединение с SFTP-сервером успешно установлено.')
            sftp.close()
            transport.close()
            return True
    except Exception as e:
        logging.error(f"Не удалось подключиться к SFTP-серверу: {e}")
        return False
def upload_files_sftp():
    """
    Загрузка файлов на SFTP-сервер
    """
    current_date = datetime.date.today() 
    uploaded_files = [] #Список загруженных файлов

    try:
        transport = paramiko.Transport((SFTP_SERVER,22)) #Объект для подключения к серверу
        transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)#авторизация
        sftp = paramiko.SFTPClient.from_transport(transport)#Объект сфтклиент на основе подключения

        try:
            # Проверка наличия папки на сервере
            sftp.chdir(SFTP_REMOTE_DIR)
            logging.info(f"Создана {SFTP_REMOTE_DIR} найдена на сервере.")
        except IOError:
            pass

        sftp.chdir(SFTP_REMOTE_DIR)

        for file_name in os.listdir('.'):
            if file_name.endswith('.txt'):
                file_path = os.path.join(os.getcwd(),file_name)
                file_modified_time = datetime.date.fromtimestamp(os.path.getmtime(file_path))

                if file_modified_time == current_date:
                    try:
                        sftp.put(file_path, os.path.join(SFTP_REMOTE_DIR, file_name))
                        uploaded_files.append(file_name)
                        logging.info(f"Файл {file_name} успешно загружен на сервер.")
                    except Exception as e:
                        logging.error(f"Не удалось загрузить файл {file_name} на сервер: {e}")
        sftp.close()
        transport.close()

        return uploaded_files
    except Exception as e:
        logging.error(f"Произошла ошибка при загрузке файлов: {e}")
        return []

def process_local_file(uploaded_files):
    """
    Обработка локальных файлов после загрузки (переименование, перемещение)
    """

    destination_folder = os.path.join(os.getcwd(), '1')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        logging.info(f"Создана директория {destination_folder}")

    for file_name in uploaded_files:
        try:
            new_file_name = f"{os.path.splitext(file_name)[0]}_has been sent{os.path.splitext(file_name)[1]}.txt"
            new_file_path = os.path.join(os.getcwd(), new_file_name)

            os.rename(file_name, new_file_name)
            shutil.move(new_file_name, os.path.join(destination_folder, new_file_name))
            logging.info(f"Файл {file_name} успешно переименован в {new_file_name} и перемещен в папку {destination_folder}")
        except Exception as e:
            logging.error(f"Произошла ошибка при обработке файла {file_name}: {e}")