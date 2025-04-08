import pandas as pd
import webbrowser
import pyautogui
import time
from screeninfo import get_monitors
from tkinter import Tk, filedialog
import sys
import os
os.system('chcp 65001')  # Для поддержки кириллицы в консоли
sys.stdout.reconfigure(encoding='utf-8')

# Настройки
EDGE_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
WAIT_LOAD = 15  # время загрузки WhatsApp Web
DELAY_AFTER_SEND = 2  # задержка после отправки


def get_excel_data(file_path):
    """Чтение данных из Excel файла"""
    try:
        df = pd.read_excel(
            file_path,
            sheet_name='реестр',
            usecols='A,B',
            header=None,
            skiprows=0,
            names=['phone', 'message'],
            engine='openpyxl'
        )
        return df.dropna()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def setup_browser():
    """Настройка браузера для второго монитора"""
    try:
        monitors = get_monitors()
        if len(monitors) < 2:
            print("Не найден второй монитор!")
            return None, None

        second_monitor = monitors[1]
        webbrowser.register('Edge', None, webbrowser.BackgroundBrowser(EDGE_PATH))

        click_x = second_monitor.x + second_monitor.width // 2
        click_y = second_monitor.y + second_monitor.height // 2

        return webbrowser.get('Edge'), (click_x, click_y)
    except Exception as e:
        print(f"Ошибка настройки браузера: {e}")
        return None, None


def send_messages(browser, click_pos, data):
    """Отправка сообщений"""
    # try:
    #     for index, row in data.iterrows():
    #         phone = str(row['phone']).strip()
    #         msg = str(row['message']).strip()
    #
    #         if not phone.startswith('7') or phone.startswith('8'):
    #             print(f"Пропущен некорректный номер: {phone}")
    #             continue
    try:
        for index, row in data.iterrows():
            phone = str(row['phone']).strip()
            msg = str(row['message']).strip()

            # Удаляем все нецифровые символы
            phone_clean = ''.join(filter(str.isdigit, phone))

            # Автоматически добавляем +7 для российских номеров
            if len(phone_clean) == 11 and phone_clean.startswith('7'):
                phone = f"+7{phone_clean[1:]}"
            elif len(phone_clean) == 10 and phone_clean.startswith('9'):
                phone = f"+7{phone_clean}"
            elif not phone.startswith('+'):
                print(f"Пропущен некорректный номер: {phone_clean}")
                continue
            #Формируем URL
            url = f'https://web.whatsapp.com/send?phone={phone}&text={msg}'
            browser.open_new_tab(url)
            if index == 0:
                time.sleep(20)
            else:
                time.sleep(WAIT_LOAD)
            pyautogui.click(*click_pos)
            pyautogui.press('enter')
            time.sleep(DELAY_AFTER_SEND)

            if index != len(data) - 1:
                pyautogui.hotkey('ctrl', 'w')
    except Exception as e:
        print(f"Ошибка при отправке: {e}")


def main():
    # Выбор файла через диалоговое окно
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Выберите Excel файл",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )

    if not file_path:
        print("Файл не выбран!")
        return

    # Проверка расширения файла
    if not file_path.lower().endswith(('.xlsx', '.xls')):
        print("Файл должен быть в формате Excel!")
        return

    data = get_excel_data(file_path)
    if data is None or data.empty:
        print("Нет данных для отправки")
        return

    browser, click_pos = setup_browser()
    if not browser:
        return

    print("Начало рассылки...")
    send_messages(browser, click_pos, data)
    print("Рассылка завершена!")


if __name__ == "__main__":
    main()