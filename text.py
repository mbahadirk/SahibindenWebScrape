from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, SessionNotCreatedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import Alignment
import sqlite3


chrome_profile_path = 'C:/Users/Mustafa Bahadır/AppData/Local/Google/Chrome/User Data/'
options = Options()

options.add_argument("start-maximized")
options.add_argument(f'user-data-dir={chrome_profile_path}')  # Profil dizinini belirtir.
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Otomasyon uyarısını kaldırır.
options.add_experimental_option('useAutomationExtension', False)
# options.add_experimental_option("detach", True)
service = Service()



while True:
    try:
        driver = webdriver.Chrome(service=service, options=options)
        url = "https://www.sahibinden.com/"
        driver.get(url)
        break
    except SessionNotCreatedException as e:
        print("### TÜM AÇIK CHROME UYGULAMALARINI KAPATIN VE TEKRAR DENEYİN ###")
        input(">>> Denemek için ENTER tuşuna basın")


def extract_slug(link):
    parts = link.split("/", 3)
    return "/" + parts[3] if len(parts) > 3 else "/"


def get_parent3(parent2):
    elements1 = driver.find_elements(By.XPATH, '//*[@id="searchCategoryContainer"]/div/div')
    elements2 = driver.find_elements(By.XPATH, '//*[@id="search_cats"]/ul')

    elements = elements1

    for element in elements:
        lis = element.find_elements(By.TAG_NAME, "li")
        for li in lis:
            try:
                a_element = li.find_element(By.TAG_NAME, "a")
                title = a_element.get_attribute("title")
                if title not in [parent2, "Emlak"]:
                    href = a_element.get_attribute("href")
                    print(f"          Parent3 title: {title}         Slug: {extract_slug(href)}")


            except NoSuchElementException:
                continue
        break




wait = WebDriverWait(driver, 10)

while True:
    try:
        driver.get("https://www.sahibinden.com/")  # Ana sayfa URL'si

        # Ana `ul` elementini bulun
        root_xpath = '/html/body/div[5]/div[3]/div/aside/div[1]/nav/ul[4]'
        root_element = driver.find_element(By.XPATH, root_xpath)
        # Ana `ul` içindeki tüm `li` elementlerini bulun
        parent_lis = root_element.find_elements(By.XPATH, './li')[:2]  # İlk 5 li elementi al
        for parent_li in parent_lis:
            child_a = parent_li.find_element(By.XPATH, './/a')
            parent_title = child_a.get_attribute('title')
            href = child_a.get_attribute('href')
            print(f"Root Title: {parent_title}      Slug: {extract_slug(href)}")

            child_ul = parent_li.find_elements(By.XPATH, './ul')
            for ul in child_ul:
                child_lis = ul.find_elements(By.XPATH, './li')
                for child_li in child_lis:
                    try:
                        child_a = child_li.find_element(By.XPATH, './/a')
                        child_title = child_a.get_attribute('title')
                        href = child_a.get_attribute('href')
                        print(f"  Parent1 Title: {child_title}      Slug: {extract_slug(href)}")

                        driver.execute_script("window.open(arguments[0]);", href)
                        driver.switch_to.window(driver.window_handles[1])

                        original_window = driver.current_window_handle
                        divs = driver.find_elements(By.CSS_SELECTOR, "div.jspPane")
                        for div in divs:
                            try:
                                parent2 = div.find_elements(By.TAG_NAME, "li")
                            except NoSuchElementException:
                                    break
                                    driver.close()  # İşlem bittikten sonra pencereyi kapatın
                                    driver.switch_to.window(driver.window_handles[1])  # Orta seviyeye geri dön
                            for li in parent2:
                                try:
                                    try:
                                        child_a = li.find_element(By.TAG_NAME, "a")
                                        title = child_a.get_attribute("title")
                                        href = child_a.get_attribute("href")
                                        print(f"        Parent2 title: {title}      Slug: {extract_slug(href)}")
                                    except NoSuchElementException:
                                        break
                                    driver.execute_script("window.open(arguments[0]);", href)
                                    driver.switch_to.window(driver.window_handles[2])

                                    ## TODO getparent3 burada çalışıyor
                                    get_parent3(title)  # parent3 elementlerini çekmek için fonksiyonu çağırın

                                    driver.close()  # İşlem bittikten sonra pencereyi kapatın
                                    driver.switch_to.window(driver.window_handles[1])  # Orta seviyeye geri dön

                                except NoSuchElementException:
                                    continue
                            driver.close()  # Orta seviye pencereyi kapat
                            driver.switch_to.window(driver.window_handles[0])  # En dış seviyeye geri dön
                            i = 0

                    except NoSuchElementException:
                        continue

    except Exception as e:
        print(f"Exception occurred: {e}")
        break



while True:
    input("test")

    # bu kod çalışıyor vasıta için denemeler yapacağız mainde