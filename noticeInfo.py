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
from bs4 import BeautifulSoup
import infoDatabase as db


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
        url = "https://www.sahibinden.com/"
        driver.get(url)
        break
    except SessionNotCreatedException as e:
        print("### TÜM AÇIK CHROME UYGULAMALARINI KAPATIN VE TEKRAR DENEYİN ###")
        input(">>> Denemek için ENTER tuşuna basın")


linkList = [
    "https://www.sahibinden.com/ilan/vasita-motosiklet-cfmoto-memurdan-cf-moto-450sr-favoricilere-indirim-yapildi-1160857498/detay",
    "https://www.sahibinden.com/ilan/vasita-otomobil-opel-degisensiz-tertemiz-gtc-1161391694/detay",
    "https://www.sahibinden.com/ilan/emlak-konut-satilik-3-plus1-daire-1154732442/detay",
    "https://www.sahibinden.com/ilan/vasita-arazi-suv-pickup-volkswagen-volkswagen-amarok-4-4-manuel-1154518094/detay",
    "https://www.sahibinden.com/ilan/vasita-minivan-panelvan-iveco-18-m3-cok-temiz-daily-3000-cc-1146573218/detay",
    "https://www.sahibinden.com/ilan/vasita-ticari-araclar-dorse-2010-model-4-dingil-tirsan-lowbed-dorse-1160819943/detay",
    "https://www.sahibinden.com/ilan/vasita-elektrikli-araclar-elektrikli-hizmet-araclari-yamaha-4-plus2-golf-araci-1162022639/detay",
    "https://www.sahibinden.com/ilan/vasita-deniz-araclari-kiralik-vega-gulet-32-mt-luxs-kaliteli-tatilin-adresi-1161587289/detay",
    "https://www.sahibinden.com/ilan/vasita-hasarli-araclar-otomobil-pilakali-satisi-hazir-1161711194/detay",
    "https://www.sahibinden.com/ilan/vasita-atv-cfmoto-sahibinden-cf-450-1106755231/detay",
    "https://www.sahibinden.com/ilan/vasita-utv-cfmoto-galeri-un-den-dusuk-kilomtre-sifir-ayarinda-z-force-550-1161684838/detay",
    "https://www.sahibinden.com/ilan/vasita-engelli-plakali-araclar-arazi-araci-suv-2024model-pejo-2008-allure-cam-tavan-dizel-engelli-indirimli-1161059659/detay",
    "https://www.sahibinden.com/ilan/vasita-hava-araclari-ucak-rotate-havacilik-bristell-b23-2024-1146311084/detay",
    "https://www.sahibinden.com/ilan/yedek-parca-aksesuar-donanim-tuning-otomotiv-ekipmanlari-yedek-parca-bmw-x5-2008-model-e70-m57-cikma-motor-1160243669/detay",
    "https://www.sahibinden.com/ilan/yedek-parca-aksesuar-donanim-tuning-motosiklet-ekipmanlari-kask-kiyafet-ekipman-motorcu-montu-1161485494/detay",
    "https://www.sahibinden.com/ilan/yedek-parca-aksesuar-donanim-tuning-deniz-araci-ekipmanlari-deniz-motorlari-volvo-td120ga-sinifsinifinin-en-iyisi-360beygir-1146496027/detay",
    "https://www.sahibinden.com/ilan/is-makineleri-sanayi-is-makineleri-satilik-dalgic-pompa-sokme-vinci-1161643611/detay",
    "https://www.sahibinden.com/ilan/is-makineleri-sanayi-tarim-makineleri-traktor-2008-tafe-45-temiz-1154049510/detay",
    "https://www.sahibinden.com/ilan/is-makineleri-sanayi-sanayi-tasima-istifleme-sarpkaya-forklift-guvencesiyle-3-ton-euro-5-motorlu-hecha-1159864022/detay",
    "https://www.sahibinden.com/ilan/is-makineleri-sanayi-elektrik-enerji-gunes-paneli-10-hp-7.5-kw-solar-sulama-sistemi-1154762472/detay"
]
ikinciEl = ["https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-bilgisayar-dizustu-notebook-hatasiz-15-inc-kutulu-mac-pro-2019-32-ram-512-ssd-1161460236/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-cep-telefonu-modeller-15-pro-256-tr-cihazi-garantili-kutulu-faturali-1144160820/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-fotograf-kamera-dijital-fotograf-makinesi-canon-7d-body-sifir-ayarinda-aksesuarli-1149984925/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-ev-elektronigi-televizyon-lg-50uq75006lf-4kultrahd-50-127-ekr.uydu-alicili-android-tv-1150666654/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-elektrikli-ev-aletleri-beyaz-esya-arcelik-6-kg-camasir-makinesi-1161852961/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-giyim-aksesuar-kadin-vizon-kurk-manto-1129687502/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-saat-kol-saati-tertemiz-jacques-philippe-1161804885/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-anne-bebek-tasima-mima-xari-bebek-arabasi-1160622823/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-kisisel-bakim-kozmetik-parfum-bvlgari-le-gemme-tygar-1161359033/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-hobi-oyuncak-rc-araclar-1-10-rc-traxxas-trx-4-chevrolet-k10-cheyenne-waterproof-rtr-1150040343/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-oyun-konsol-oyun-konsolu-sony-playstation-5-slim-1158474634/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-muzik-muzik-aletleri-blackstar-id-core-20-v3-ve-footswitch-cok-az-kullanilmis-1160896830/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-spor-bisiklet-carraro-gravel-g2-2023-48-kadro-1159028499/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-taki-mucevher-altin-kolye-damla-kehribar-kolye-1160609759/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-bahce-yapi-market-yapi-malzemeleri-100-wat-sogutmali-let-pirojoktor-1161269771/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-teknik-elektronik-terazi-sehpali-80x90-cm-baskul-600kg-dayama-siperli-ambalajci-kantari-1160646876/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-ofis-kirtasiye-ofis-mobilyalari-baron-makam-takimi-oturma-grubu-dahil-set-akburo-ofis-de-1161301722/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-yiyecek-icecek-kuruyemis-jumbo-boy-ince-kabuk-1161995012/detay",
    "https://www.sahibinden.com/ilan/ikinci-el-ve-sifir-alisveris-diger-her-sey-otomatlar-vcm-3-mini-yiyecek-ve-icecek-otomati-sifir-2-yil-garantili-1147824087/detay"
    ]


for page in linkList:
    driver.get(page)
    info = driver.find_elements(By.XPATH,"//*[@id='classifiedDetail']/div/div[2]/div[2]/ul")
    propertyList = ""
    for li in info:
        soup = BeautifulSoup(li.get_attribute('innerHTML'), 'html.parser')
        lis = soup.find_all("li")
        for id, li in enumerate(lis[1:]):
            strong = li.find("strong")
            strong = strong.text.strip()

            print(id, strong)
            propertyList += strong + "//"
    db.add_data(page, propertyList)
    propertyList = ""

for page in ikinciEl:
    driver.get(page)
    info = driver.find_elements(By.XPATH,"//*[@id='classifiedDetail']/div/div[3]/div[2]/ul")
    propertyList = ""
    for li in info:
        soup = BeautifulSoup(li.get_attribute('innerHTML'), 'html.parser')
        lis = soup.find_all("li")
        for id, li in enumerate(lis[1:]):
            strong = li.find("strong")
            strong = strong.text.strip()

            print(id, strong)
            propertyList += strong + "//"
    db.add_data(page, propertyList)
    propertyList = ""