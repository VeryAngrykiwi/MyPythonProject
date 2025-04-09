import time

from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
import pandas as pd
from tkinter import Tk, filedialog
import sys
import os


def select_file():
    """Диалоговое окно выбора файла"""
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)

    file_path = filedialog.askopenfilename(
        title="Выберите файл Excel",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    return file_path


# Получаем путь к файлу
file_path = select_file()

if not file_path:
    print("Файл не выбран!")
    sys.exit()

try:
    # Чтение данных из Excel
    df = pd.read_excel(
        file_path,
        sheet_name='реестр',
        usecols='A,B',
        header=None,
        names=['phone', 'message'],
        dtype={'phone': str}
    )
    # Удаление пустых строк
    df = df.dropna().reset_index(drop=True)
except Exception as e:
    print(f"Ошибка чтения файла: {e}")
    sys.exit()

# Проверка данных
if df.empty:
    print("Файл не содержит данных!")
    sys.exit()

# Данные из my.telegram.org
api_id = '22964491'
api_hash = 'e5540975a1f2cfad68fd4389152a58c1'
phone = '+79266331776'

# Авторизация
client = TelegramClient('session_name', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    try:
        client.send_code_request(phone)
        code = input('Введите код из Telegram: ')
        client.sign_in(phone, code)
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        sys.exit()

# Отправка сообщений
for index, row in df.iterrows():
    try:
        # Очистка номера от лишних символов
        phone_clean = ''.join(filter(str.isdigit, str(row['phone'])))
        if not phone_clean.startswith('7') or len(phone_clean) != 11:
            print(f"Некорректный номер: {row['phone']}")
            continue

        formatted_phone = f"+{phone_clean}"
        user = client.get_input_entity(formatted_phone)
        client.send_message(user, str(row['message']))
        print(f"Отправлено: {formatted_phone}")

    except Exception as e:
        print(f"Ошибка для {row['phone']}: {str(e)[:100]}...")
    time.sleep(15)
client.disconnect()
print("Рассылка завершена!")