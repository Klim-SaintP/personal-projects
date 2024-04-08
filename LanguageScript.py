import cv2
from PIL import ImageGrab
import pytesseract
import pyperclip
import numpy as np
from pynput.mouse import Button, Listener
from googletrans import Translator

translator = Translator()

def translate_to_russian(text):
    translation = translator.translate(text, dest='ru')
    return translation.text

def process_image(text):
    # Удаление лишних пробелов и символов перевода строк
    text = ' '.join(text.split())
    # Перевод текста на русский
    translated_text = translate_to_russian(text)
    return translated_text

def copy_to_clipboard(text):
    pyperclip.copy(text)

def on_mouse_click(x, y, button, pressed):
    if pressed:
        if button == Button.x1:
            image = ImageGrab.grabclipboard()
            if image is not None:
                image_np = np.array(image)
                gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
                _, threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                text = pytesseract.image_to_string(threshold_img, lang='chi_sim+chi_tra+eng+kor+ara+jpn+rus')
                text = ' '.join(text.split())
                copy_to_clipboard(text)
                print("Скопированный текст:")
                print(text)
            else:
                print("Изображение не найдено в буфере обмена.")

        elif button == Button.x2:
            # Обрабатываем изображение и выполняем перевод
            image = ImageGrab.grabclipboard()
            if image is not None:
                image_np = np.array(image)
                gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
                _, threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                text = pytesseract.image_to_string(threshold_img, lang='chi_sim+chi_tra+eng+kor+ara+jpn+rus')
                translated_text = process_image(text)
                pyperclip.copy(translated_text)
                print("Переведенный текст на русский:")
                print(translated_text)
            else:
                print("Изображение не найдено в буфере обмена.")

with Listener(on_click=on_mouse_click) as listener:
    listener.join()
