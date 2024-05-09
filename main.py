import time
import csv
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://coinmarketcap.com/ru/'


def driver_browser(link):
    '''
    Функция создает драйвер имитации работы браузера, чтобы загрузить динамические данные
    :param link: https://
    :return: str (HTML data)
    '''
    driver = webdriver.Chrome()
    driver.get(link)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        # Wait to load page
        time.sleep(1)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return driver.page_source


def parse_html(html_data):
    '''
    Функция для парсинга данных с сайта
    :param html_data:
    :return: list
    '''
    crypts_list = []
    markets_list = []
    values_list = []
    percent_list = []
    all_values = 0

    soup = BeautifulSoup(html_data, 'html.parser')
    table = soup.find('tbody')
    market_caps = table.find_all('p', class_='sc-4984dd93-0 kKpPOn')
    value_cap = table.find_all('span', class_='sc-7bc56c81-1 bCdPBp')

    for names, values in zip(market_caps, value_cap):
        name = names.text[0: + names.text.find(" ")]
        markets_list.append(name)

        value = values.text[1:]
        values_list.append(value)

        crypt_dict = {'Name': name, 'MC': value}
        crypts_list.append(crypt_dict)

        all_values += int(values.text[1:].replace(',', ''))

    counter = 0
    for value in values_list:
        percent = int(value.replace(',', '')) / (all_values / 100)
        percent_list.append(str(format(percent, '.2f')) + '%')
        crypts_list[counter]['MP'] = str(format(percent, '.2f')) + '%'
        counter += 1

    return crypts_list


def save_to_file(data):
    '''
    Функция записи данных в файл
    :param data: list
    :return: *.csv
    '''
    file_name = f'{datetime.datetime.now().strftime("%H.%M_%d.%m.%Y")}'
    with open(file_name + '.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=' ', fieldnames=data[0])
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    save_to_file(parse_html(driver_browser(url)))
