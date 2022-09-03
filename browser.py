from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_info(currency_type):
    driver = webdriver.Chrome()
    driver.get('https://yandex.ru')

    wait = WebDriverWait(driver, 10)
    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1

    moex = driver.find_elements(By.CLASS_NAME, 'stocks__item-title')
    if currency_type == 'usd':
        moex[2].click()
    elif currency_type == 'eur':
        moex[3].click()
    else:
        return -1

    wait.until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    
    if currency_type == 'usd':
        wait.until(EC.title_is('Курс доллара США USDTOM_UTS к российскому рублю на MOEX на сегодня: Котировки валют на Яндекс.Новостях'))
    elif currency_type == 'eur':
        wait.until(EC.title_is('Курс евро EURTOM_UTS к российскому рублю на MOEX на сегодня: Котировки валют на Яндекс.Новостях'))
    else:
        return -1

    ten_days_values = driver.find_element(By.CLASS_NAME, 'news-stock-table__content').find_elements(By.CLASS_NAME, 'news-stock-table__cell')
    ten_days_values = ten_days_values[3:]

    ten_days_changes = driver.find_element(By.CLASS_NAME, 'news-stock-table__content').find_elements(By.CLASS_NAME, 'news-stock-table__row')
    ten_days_changes = ten_days_changes[1:]
    
    info = []
    day = []
    for val in ten_days_values:
        if len(day) < 3:
            day.append(val.text)
        else:
            info.append(day)
            day = [val.text]
    info.append(day)

    for i in range(len(info)):
        if ten_days_changes[i].get_attribute('class') == 'news-stock-table__row news-stock-table__row_change_negative':
            info[i][2] = f'-{info[i][2]}'

    driver.quit()

    return info