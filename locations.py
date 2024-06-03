import time
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
import locationDatabase as locdb
from bs4 import BeautifulSoup

chrome_profile_path = 'C:/Users/Mustafa Bahadır/AppData/Local/Google/Chrome/User Data/'
options = Options()
options.add_argument("start-maximized")
options.add_argument(f'user-data-dir={chrome_profile_path}')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
service = Service()



while True:
    try:
        driver = webdriver.Chrome(service=service, options=options)
        url = "https://www.sahibinden.com/kategori/emlak-konut"
        driver.get(url)
        break
    except SessionNotCreatedException as e:
        print("### TÜM AÇIK CHROME UYGULAMALARINI KAPATIN VE TEKRAR DENEYİN ###")
        input(">>> Denemek için ENTER tuşuna basın")

time.sleep(2)

city_button = driver.find_element(By.XPATH,"//*[@id='searchForm']/div/div[1]/div[2]/div[1]/div/span")
cities_html = driver.find_elements(By.XPATH,"//*[@id='searchForm']/div/div[1]/div[2]/div[1]/div/ul")

locdb.create_database()


def getNeighbour(townName):
    neighbour_button = driver.find_element(By.XPATH, "//*[@id='searchForm']/div/div[1]/div[2]/div[3]/div/span")
    neighbour_button.click()

    neighbour_html = driver.find_elements(By.XPATH, "//*[@id='searchForm']/div/div[1]/div[2]/div[3]/div/ul/div/div[1]")

    for neighbour in neighbour_html:
        soup = BeautifulSoup(neighbour.get_attribute('innerHTML'), 'html.parser')

        districts = soup.find_all("li")[1:]
        for district in districts:
            district_label = district.find("label", class_="district-label")
            if district_label:
                district_name = district_label.text.strip()
                print("   "*10, district_name)
                locdb.add_neighborhood(district_name, townName)

                quarters = district.find("ul", class_="quarter")
                if quarters:
                    for quarter in quarters.find_all("li"):
                        quarter_name = quarter.find("label", class_="quarter-label").text.strip()
                        print("     " * 10, quarter_name)
                        locdb.add_street(quarter_name, district_name)
                else:
                    print("         " * 10, "Mahalle bulunamadı")

                print()

def getTown(cityName):
    town_button = driver.find_element(By.XPATH,"//*[@id='searchForm']/div/div[1]/div[2]/div[2]/div/span")
    town_button.click()

    town_html = driver.find_elements(By.XPATH, "//*[@id='searchForm']/div/div[1]/div[2]/div[2]/div/ul/div/div[1]")

    for town in town_html:
        soup = BeautifulSoup(town.get_attribute('innerHTML'), 'html.parser')
        lis = soup.find_all("li")
        for id, li in enumerate(lis[1:]):
            town_name = li.text.strip()
            print("         ", town_name)
            locdb.add_district(town_name, cityName)
            button_xpath = f"//*[@id='searchForm']/div/div[1]/div[2]/div[2]/div/ul/div/div[1]/li[{id+1}]"
            button = driver.find_element(By.XPATH, button_xpath)
            try:
                WebDriverWait(driver, 0.1).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                button.click()
            except:
                ActionChains(driver).move_to_element(button).perform()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                button.click()
            time.sleep(0.5)
            getNeighbour(town_name)
            town_button.click()
            time.sleep(0.5)


for city in cities_html:
    soup = BeautifulSoup(city.get_attribute('innerHTML'), 'html.parser')
    city_button.click()
    lis = soup.find_all("li")
    for id, li in enumerate(lis[1:]):
        cityName = li.text.strip()
        print(cityName)
        id += 1
        locdb.add_city(cityName)

        button_xpath = f"//*[@id='searchForm']/div/div[1]/div[2]/div[1]/div/ul/div/div[1]/li[{id+1}]"
        button = driver.find_element(By.XPATH, button_xpath)
        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            button.click()
        except:
            ActionChains(driver).move_to_element(button).perform()
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            button.click()
        time.sleep(0.5)
        getTown(cityName)
        city_button.click()
        time.sleep(0.5)