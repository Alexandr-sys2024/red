import time
import csv
import sys
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

if not is_connected():
    print("Ошибка: Отсутствует подключение к интернету.")
    sys.exit(1)

try:
    driver = init_driver()
    wait = WebDriverWait(driver, 20)
    url = "https://www.divan.ru/category/svet"
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._Ud0k')))
        luminaires = driver.find_elements(By.CSS_SELECTOR, 'div._Ud0k')
        parsed_data = []

        for luminaire in luminaires:
            try:
                name = luminaire.find_element(By.CSS_SELECTOR, 'div.lsooF span').text
                price = luminaire.find_element(By.CSS_SELECTOR, 'div.pY3d2 span').text
                link = luminaire.find_element(By.TAG_NAME, 'a').get_attribute('href')
                print(f"Найдено: {name} - {price}")
                parsed_data.append([name, price, link])
            except Exception as e:
                print(f"Ошибка при парсинге элемента: {str(e)}")
                continue

        with open('luminaires.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Название', 'Цена', 'Ссылка'])
            writer.writerows(parsed_data)

    except TimeoutException:
        print("Ошибка: Превышено время ожидания загрузки элементов.")
    except WebDriverException as e:
        print(f"Ошибка Selenium: {str(e)}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {str(e)}")

finally:
    try:
        driver.quit()
    except:
        pass

print("Парсинг завершен")