import webbrowser
from urllib.parse import quote # дополнительная проверка кодировки
import pyautogui
import time
from screeninfo import get_monitors

#phone_number = '+79266331776'
phone_number_list = ['+79266331776','+79005258586', '+79266331776']
message = ['Motorhead Rules', 'YeahBaby', 'You better run!']
# encoded_messege = quote(message.encode('utf-8')) # кодировка (при необходимости)


# РАЗОВАЯ ОТПРАВКА
# webbrowser.open('http://web.whatsapp.com') # браузер по умолчанию
# webbrowser.register('Edge', None, webbrowser.BackgroundBrowser(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'))
# webbrowser.get('Edge').open_new_tab(f'https://web.whatsapp.com/send?phone={phone_number}&text={message}')
# time.sleep(10)
# pyautogui.press('enter')
# time.sleep(2)
# pyautogui.hotkey('ctrl', 'w')


#ВЫБОР МОНИТОРА И НАСТРОЙКА КЛИКА
monitors = get_monitors()
# Выбрать второй монитор (индекс 1, если индекс 0 — первый)
second_monitor = monitors[1]  # Проверь порядок мониторов в системе!
# print(f"Ширина: {second_monitor.width}, Высота: {second_monitor.height}")
primary_width, primary_height = pyautogui.size()
second_monitor_width = second_monitor.width
second_monitor_height = second_monitor.height

webbrowser.register('Edge', None,
                        webbrowser.BackgroundBrowser(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'))
msg_indx = 0

for phone_number in phone_number_list:
    if msg_indx < len(phone_number_list) - 1:
        webbrowser.get('Edge').open_new_tab(f'https://web.whatsapp.com/send?phone={phone_number}&text={message[msg_indx]}')
        time.sleep(10)
        # pyautogui.click(screen_width/2, screen_height/2) основной монитор
        pyautogui.click(x=primary_width + second_monitor_width // 2, y=second_monitor_height // 2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'w')
    else:
        webbrowser.get('Edge').open_new_tab(f'https://web.whatsapp.com/send?phone={phone_number}&text={message[msg_indx]}')
        time.sleep(10)
        # pyautogui.click(screen_width/2, screen_height/2) основной монитор
        pyautogui.click(x=primary_width + second_monitor_width // 2, y=second_monitor_height // 2)
        pyautogui.press('enter')
    msg_indx += 1

print('im done!')