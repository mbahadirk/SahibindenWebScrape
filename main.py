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
import dbConnection as db

chrome_profile_path = 'C:/Users/Mustafa Bahadır/AppData/Local/Google/Chrome/User Data/'
options = Options()
options.add_argument("start-maximized")
options.add_argument(f'user-data-dir={chrome_profile_path}')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
service = Service()


p1_name = db.name
counter = 3
i = 0
j = 0
invalid_data = ["İş Makineleri & Sanayi", p1_name]


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

def scrapeBasics(li):
    a_element = li.find_element(By.TAG_NAME, "a")
    title = a_element.get_attribute("title")
    href = a_element.get_attribute("href")
    slug = extract_slug(href)
    return title, href, slug

def car_get_parent2(parent1):
    global i
    divs = driver.find_elements(By.CSS_SELECTOR, "div.jspPane")
    for div in divs:
        try:
            parent2 = div.find_elements(By.TAG_NAME, "li")
        except NoSuchElementException:
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            break
        for li in parent2[i:]:
            try:
                try:
                    parent2, href, slug = scrapeBasics(li)
                    print(f"        Parent2 title: {parent2}      Slug: {slug}  i = {i}")
                    i = i+1
                    db.add_parent2_category(parent2, slug, parent1)

                except NoSuchElementException:
                    break
                driver.execute_script("window.open(arguments[0]);", href)
                driver.switch_to.window(driver.window_handles[2])

                car_get_parent3(parent2)
                driver.close()
                driver.switch_to.window(driver.window_handles[1])

            except NoSuchElementException:
                continue
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        i = 0

def car_get_parent3(parent2):
    global j
    elements1 = driver.find_elements(By.XPATH, '//*[@id="searchCategoryContainer"]/div/div')
    elements2 = driver.find_elements(By.XPATH, '//*[@id="search_cats"]/ul')

    if parent2 == "Anadol":
        elements = elements2
    else:
        elements = elements1

    for element in elements:
        lis = element.find_elements(By.TAG_NAME, "li")
        for li in lis[j:]:
            try:
                parent3, href, slug = scrapeBasics(li)
                if parent3 not in [parent2, invalid_data[0], invalid_data[1]]:
                    print(f"          Parent3 title: {parent3}         Slug: {slug}")
                    db.add_parent3_category(parent3, slug, parent2)

                    driver.execute_script("window.open(arguments[0]);", href)
                    driver.switch_to.window(driver.window_handles[3])

                    car_get_parent4(parent2, parent3)

                    driver.close()
                    driver.switch_to.window(driver.window_handles[2])

            except NoSuchElementException:
                continue
        j = 0
        break



def car_get_parent4(parent2, parent3):
    elements1 = driver.find_elements(By.XPATH, "//*[@id='search_cats']/ul")
    elements2 = driver.find_elements(By.XPATH, '//*[@id="searchCategoryContainer"]/div/div/ul')

    elementsList = [elements1, elements2]
    for elements in elementsList:
        for element in elements:
            lis = element.find_elements(By.TAG_NAME, "li")
            for li in lis:
                try:
                    parent4, href, slug = scrapeBasics(li)
                    if parent4 not in [parent2, parent3, invalid_data[0], invalid_data[1]]:
                        print(f"                Parent4 title: {parent4}       Slug: {slug}")
                        db.add_parent4_category(parent4, slug, parent3)


                        # driver.execute_script("window.open(arguments[0]);", href)
                        # driver.switch_to.window(driver.window_handles[4])
                        #
                        # car_get_parent5(parent2, parent3, parent4)
                        #
                        # driver.close()
                        # driver.switch_to.window(driver.window_handles[3])


                except Exception as e:
                    print(e)
                    continue
            break


def car_get_parent5(parent2, parent3, parent4):
    elements1 = driver.find_elements(By.XPATH, "//*[@id='search_cats']/ul")
    elements2 = driver.find_elements(By.XPATH, '//*[@id="searchCategoryContainer"]/div/div/ul')

    elementsList = [elements1, elements2]
    for elements in elementsList:
        for element in elements:
            lis = element.find_elements(By.TAG_NAME, "li")
            for li in lis:
                try:
                    parent5, href, slug = scrapeBasics(li)
                    if parent5 not in [parent2, parent3, parent4,  invalid_data[0], invalid_data[1] ]:
                        print(f"                    Parent5 title: {parent5}       Slug: {slug}")
                        db.add_parent5_category(parent5, slug, parent4)
                except NoSuchElementException:
                    continue
            break


wait = WebDriverWait(driver, 10)

def getCarInfo():
    try:
        root_xpath = '/html/body/div[5]/div[3]/div/aside/div[1]/nav/ul[4]'
        root_element = driver.find_element(By.XPATH, root_xpath)
        parent_lis = root_element.find_elements(By.XPATH, './li')[4:5]  # TODO alınacak veri kısmı
        for li in parent_lis:
            root, href, slug = scrapeBasics(li)
            print(f"Root Title: {root}       Slug: {slug}")
            db.add_root_category(root, slug)

            child_ul = li.find_elements(By.XPATH, './ul')
            for ul in child_ul:
                child_lis = ul.find_elements(By.XPATH, './li')[counter:counter+1]
                for li in child_lis:
                    try:
                        parent1, href, slug = scrapeBasics(li)
                        print(f"  Parent1 Title: {parent1}      Slug: {slug}")
                        db.add_parent1_category(parent1, slug, root)

                        driver.execute_script("window.open(arguments[0]);", href)
                        driver.switch_to.window(driver.window_handles[1])

                        car_get_parent2(parent1)

                    except NoSuchElementException:
                        continue

    except Exception as exc:
        print(f"Exception occurred: {exc}")



getCarInfo()

while True:
    input("test")