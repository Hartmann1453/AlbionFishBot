import time

import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
from mss import mss

# Окно запуска
res_but = pyautogui.confirm(text='Необходимо развернуть игру и лишь потом нажать ОК', title='Вопрос', buttons=['Да', 'Нет'])
print(res_but)

def find_window():

    # Загружаем иконку
    template = cv2.imread('img/icon.png', 0)
    #w, h = template.shape[::-1]

    bounding_box = {'top': 0, 'left': 0, 'width': 1300, 'height': 700}
    sct = mss()
    for i in range(100):
        # Захват картинки
        sct_img = sct.grab(bounding_box)
        img = np.array(sct_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        print(f'Ищем рабочее окно.[{i}/100]')

        # Ищем объект на экране
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.9)
        x, y = 0, 0
        # Берем последнее совпадение и записываем координаты
        for pt in zip(*loc[::-1]):
            x = pt[0]
            y = pt[1]

        if(x != 0 and y != 0):
            x -= 7
            y -= 4
            print(f'Рабочее окно найдено! x: {x} | y: {y}')
            return x, y

def start(x = 0, y = 0):

    x += 500 + win_x
    y += 380 + win_y

    time.sleep(1)
    pyautogui.moveTo(x, y)
    time.sleep(0.5)
    pyautogui.mouseDown()
    time.sleep(0.05)
    pyautogui.mouseUp()
    time.sleep(3)

def see_pop():
    # Переменная отклонения поплавка в покое
    average = [0, ]
    # Загружаем образец поплавка в покое и приводим в машинный вид
    template = cv2.imread('img/2.png', 0)
    w, h = template.shape[::-1]

    # Делаем скрин экрана
    #print('Делаем скрин.')
    base_screen = ImageGrab.grab(bbox=(0, 0, 900, 700))
    base_screen.save('img/scr.png')

    # Переводим картинки в машинный вид
    img_rgb = cv2.imread('img/scr.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Ищем поплавок на экране
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.6)

    _i = 0

    # Запускаем цикл на отлов "Клюет"
    while True:
        try:
            clean_screen = ImageGrab.grab(bbox=(x, y, x + w, y + h))  #
            mean = np.mean(clean_screen)  # Отслеживаем изменения
            diff = average[-1] - mean  # Остлеживаем серьезность изменения
            print(average[-1] - mean)
            _i += 1
            print(_i)
            if _i > 500:
                print('Клёв не был найден.')
                pyautogui.press('numlock')
                pyautogui.press('numlock')
                return False
            if diff > 2 :  # НАДО ОТСЛЕДИТЬ РУЧКАМИ если изменения серьезные
                #print('КЛЮЁТ')
                pyautogui.mouseDown()  # Нажали мышь
                time.sleep(0.4)
                pyautogui.mouseUp()  # Отжали мышь
                return True
            average.append(mean)
        except:
            # Ищем поплавок
            for pt in zip(*loc[::-1]):
                x = pt[0]
                y = pt[1]
                print(f'Коорд поплавка: [{x}|{y}]')
                # print(f'Нашли полавок. Координаты:\nПервая:{x}|{coord[0]}\nВторая:{y}|{coord[1]}\nТретья:{x+w}|{coord[2]}\nЧетвертая:{y+h}|{coord[3]}')

def start_mini():
    # Загружаем образец поплавка в покое и приводим в машинный вид
    template = cv2.imread('img/mini.png', 0)
    #w, h = template.shape[::-1]

    bounding_box = {'top': 0, 'left': 0, 'width': 1024, 'height': 768}
    sct = mss()
    _i = 0
    for i in range(10000):
        # Захват картинки
        sct_img = sct.grab(bounding_box)
        img = np.array(sct_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Ищем поплавок на экране
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.7)

        #print('____________________________________')
        #print(f'Номер итерации:{i}')
        #print(f'Сырой loc: {loc}')
        x = 0
        # Проверяем положение поплавка
        for pt in zip(*loc[::-1]):
            x = pt[0]

        if x <= win_x + 520 and x != 0:
            pyautogui.mouseDown()  # Нажали мышь
            _i = 0
        if x > win_x + 520:
            pyautogui.mouseUp()  # Отжали мышь
            _i = 0

        if x == 0:
            _i += 1

        #print(f'x: {x}, _i: {_i}')

        if _i == 5:
            pyautogui.mouseUp()
            time.sleep(5)
            break
    time.sleep(2)

def fishing(count, x, y):
    z = 0
    for i in range(count):
        start(x, y) # Закидываем поплавок
        _bool = see_pop() # Отлавливаем клёв. Если клюнет - клацнем по воде.
        if _bool == True:
            start_mini()
            z += 1
            print(f'Рыбка в кармане![{z}/{i+1}/{count}]')
    print('Рыбалка окончена.')

if res_but == 'Да':
    win_x, win_y = find_window()
    fishing(20, 150, -150)
