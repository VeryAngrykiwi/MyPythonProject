from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
import pandas as pd
from tkinter import Tk, filedialog
import sys
import time
import os

# Настройки
DELAY_BETWEEN_MESSAGES = 15  # Задержка между сообщениями (в секундах)
MAX_RETRIES = 3  # Максимальное количество попыток отправки
API_ID = 'ВАШ_API_ID'  # Замените на свои данные
API_HASH = 'ВАШ_API_HASH'  # Замените на свои данные
PHONE = '+ВАШ_НОМЕР'  # Замените на свой номер


def select_file():
    """Диалоговое окно выбора файла Excel"""
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)

    file_path = filedialog.askopenfilename(
        title="Выберите файл Excel",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    return file_path


def process_excel(file_path):
    """Чтение данных из Excel"""
    try:
        df = pd.read_excel(
            file_path,
            sheet_name='реестр',
            usecols='A,B',
            header=None,
            names=['phone', 'message'],
            dtype={'phone': str}
        )
        # Удаление пустых строк и строк с некорректными номерами
        df = df.dropna().reset_index(drop=True)
        df['phone'] = df['phone'].apply(lambda x: ''.join(filter(str.isdigit, str(x))))
        df = df[df['phone'].str.len() == 11]  # Фильтр для российских номеров
        return df
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None


def main():
    # Выбор файла
    file_path = select_file()
    if not file_path:
        print("Файл не выбран!")
        return

    # Обработка Excel
    df = process_excel(file_path)
    if df is None or df.empty:
        print("Нет данных для отправки!")
        return

    # Авторизация в Telegram
    client = TelegramClient('session_name', API_ID, API_HASH)
    client.start(phone=PHONE)

    # Отправка сообщений
    for index, row in df.iterrows():
        retries = 0
        formatted_phone = f"+7{row['phone'][1:]}"  # Формат +79123456789
        message = str(row['message']).strip()

        while retries < MAX_RETRIES:
            try:
                user = client.get_input_entity(formatted_phone)
                client.send_message(user, message)
                print(f"Отправлено: {formatted_phone}")
                time.sleep(DELAY_BETWEEN_MESSAGES)
                break
            except Exception as e:
                print(f"Ошибка ({retries + 1}/{MAX_RETRIES}): {str(e)[:100]}...")
                retries += 1
                time.sleep(30 * retries)

    client.disconnect()
    print("Рассылка завершена!")


if __name__ == "__main__":
    # Для Windows: поддержка кириллицы
    if os.name == 'nt':
        os.system('chcp 65001 > nul')
    main()