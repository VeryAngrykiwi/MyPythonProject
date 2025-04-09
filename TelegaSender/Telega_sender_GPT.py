from telethon.sync import TelegramClient
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import time

# Данные авторизации из my.telegram.org
api_id = '22964491'
api_hash = 'e5540975a1f2cfad68fd4389152a58c1'
phone = '+79266331776'

# Выбор Excel-файла через диалоговое окно
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Выберите Excel файл",
    filetypes=[("Excel файлы", "*.xls *.xlsx")]
)

if not file_path:
    print("Файл не выбран. Завершение.")
    exit()

# Чтение данных из листа "реестр" (номер - столбец A, текст - столбец B)
df = pd.read_excel(file_path, sheet_name="реестр", usecols="A:B", header=None)
df.columns = ['phone', 'message']

# Подключение к Telegram
client = TelegramClient('session_name', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Введите код из Telegram: '))

# Импорт контактов. Добавляем номера из Excel, чтобы затем получить их сущности
contacts = [
    InputPhoneContact(client_id=index, phone=str(row['phone']), first_name='User', last_name='')
    for index, row in df.iterrows()
]
client(ImportContactsRequest(contacts))

# Отправка сообщений с паузой в 10 секунд между сообщениями
for index, row in df.iterrows():
    try:
        entity = client.get_input_entity(str(row['phone']))
        client.send_message(entity, row['message'])
        print(f"✅ Отправлено: {row['phone']}")
    except Exception as e:
        print(f"❌ Ошибка для {row['phone']}: {e}")
    time.sleep(10)  # Пауза 10 секунд между отправками

client.disconnect()
print("📬 Рассылка завершена!")