import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def init_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)


try:
    driver = init_driver()
    wait = WebDriverWait(driver, 20)  # Увеличиваем время ожидания до 20 секунд

    url = "https://www.divan.ru/category/svet"
    driver.get(url)

    # Даем странице полностью загрузиться
    time.sleep(5)

    # Прокручиваем страницу, чтобы загрузить все элементы
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    try:
        # Ждем появления первого элемента товара
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._Ud0k')))

        # Получаем все товары
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

        # Записываем данные в CSV файл
        with open('luminaires.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Название', 'Цена', 'Ссылка'])
            writer.writerows(parsed_data)

    except TimeoutException:
        print("Превышено время ожидания загрузки элементов")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

finally:
    try:
        driver.quit()
    except:
        pass

print("Парсинг завершен")