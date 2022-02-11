from selenium import webdriver
from requests_html import HTMLSession
import chompjs
import pandas as pd
import json
import time
from csv import reader
from concurrent.futures import ThreadPoolExecutor as TPE
##------------------------:: Extracción de links ::------------------------------------------##
url = 'https://www.fincaraiz.com.co/inmueble'
driver = webdriver.Chrome(executable_path = '/Users/Thony/Documents/chromedriver')
driver.get(url)
driver.find_element_by_css_selector('#PoliticaCookies > div > div > button').click()

driver.find_element_by_css_selector('#olBCFilters > div:nth-child(1) > div > div > div.anchor').click()
driver.find_element_by_css_selector('#olBCFilters > div:nth-child(1) > div > div > div.ContentCollapse > div > ul > div > li:nth-child(2) > a').click()
links = []
for x in range(2,1125):
    tab = driver.find_elements_by_css_selector('li > div > a')
    for p in tab:
        t = p.get_property('href')
        links.append(t)
        print("Numero de link extraido :",len(links))
    driver.find_element_by_xpath(f'//*[@id="lnkPage{x}"][1]').click()
    time.sleep(2)
urls = pd.unique(links)
df = pd.DataFrame(urls)
df.to_csv('fincaraiz_links_antioquia20220207.csv',index = False)

### Extrac data from urls
urls = urls[1:len(urls)]
""" urls = []
with open('fincaraiz_links_cordoba20220131.csv','r') as f:
    csv_reader = reader(f)
    for row in csv_reader:
        urls.append(row[0]) """

print('La cantidad urls a extraer',len(urls))
all_det = []
def parse(url):
    s = HTMLSession()
    r = s.get(url)
    ### inform for application/json
    info_css_2 = 'script[type="application/json"]'
    script_txt_2 = r.html.find(info_css_2,first = True).text.strip()
    json_data_2 = chompjs.parse_js_object(script_txt_2)
    ## data_2
    data_2= json.dumps(json_data_2)
    dta_2 = json.loads(data_2)
    ## datos
    try:
        fecha_publicacion = dta_2['props']['pageProps']['dates']['published']
        description = dta_2['props']['pageProps']['description']
        estrato = dta_2['props']['pageProps']['stratum']['name']
        n_estrato = dta_2['props']['pageProps']['stratum']['id']
        price_M2 = dta_2['props']['pageProps']['priceM2']
        address = dta_2['props']['pageProps']['address']
        categories = dta_2['props']['pageProps']['categories']
        contact = dta_2['props']['pageProps']['contact']
        name = dta_2['props']['pageProps']['propertyType']['name']
        title = dta_2['props']['pageProps']['title']
        price = dta_2['props']['pageProps']['price']
        rooms = dta_2['props']['pageProps']['rooms']['id']
        baths = dta_2['props']['pageProps']['baths']['id']
        area_const = dta_2['props']['pageProps']['area']
        tipo_inmueble = dta_2['props']['pageProps']['client']['type']
        first_name = dta_2['props']['pageProps']['client']['firstName']
        lastName = dta_2['props']['pageProps']['client']['lastName']
        lat = dta_2['props']['pageProps']['locations']['lat']
        lon = dta_2['props']['pageProps']['locations']['lng']
        pais = dta_2['props']['pageProps']['locations']['country']['name']
        dept = dta_2['props']['pageProps']['locations']['state']['name']
        ciudad = dta_2['props']['pageProps']['locations']['city']['name']
        barrio = dta_2['props']['pageProps']['locations']['neighbourhood']['name']
        zona = dta_2['props']['pageProps']['locations']['zone']
        condition = dta_2['props']['pageProps']['condition']
        tiempo = dta_2['props']['pageProps']['age']['name']
        garages = dta_2['props']['pageProps']['garages']['id']
        floor = dta_2['props']['pageProps']['floor']['name']
        parking = dta_2['props']['pageProps']['parking']
        environment = dta_2['props']['pageProps']['environment']
        url_page = dta_2['props']['pageProps']['seo']['url']
    except:
        fecha_publicacion = 'None'
        description = 'None'
        estrato = 'None'
        n_estrato = 'None'
        price_M2 = 'None'
        address = 'None'
        categories = 'None'
        contact = 'None'
        name = 'None'
        title = 'None'
        price = 'None'
        rooms = 'None'
        baths = 'None'
        area_const = 'None'
        tipo_inmueble = 'None'
        first_name = 'None'
        lastName = 'None'
        lat = 'None'
        lon = 'None'
        pais = 'None'
        dept = 'None'
        ciudad = 'None'
        barrio = 'None'
        zona = 'None'
        condition = 'None'
        tiempo = 'None'
        garages = 'None'
        floor = 'None'
        parking = 'None'
        environment = 'None'
        url_page = 'None'
    dett = {
            'fecha_publicacion':fecha_publicacion, 
            'description':description,
            'estrato':estrato, 
            'n_estrato':n_estrato, 
            'price_M2':price_M2,
            'address':address, 
            'categories':categories,
            'contact':contact,
            'name':name,
            'title':title,
            'price':price,
            'rooms':rooms,
            'baths':baths,
            'area_const':area_const,
            'tipo_inmueble':tipo_inmueble,
            'first_name':first_name,
            'lastName':lastName,
            'latitude':lat,
            'longitude':lon,
            'pais':pais,
            'dept':dept,
            'ciudad':ciudad,
            'barrio':barrio,
            'zona':zona,
            'condition':condition,
            'tiempo':tiempo,
            'garages':garages,
            'floor':floor,
            'parking':parking,
            'environment':environment,
            'url_page':url_page
        }
    all_det.append(dett)
    print("Amount of info :",len(all_det))

start = time.perf_counter() 
fin = time.perf_counter() - start

with TPE() as executor:
    executor.map(parse, urls)

print('Time taken:',fin)

df = pd.DataFrame(all_det)
print(df.shape)
df.to_csv('fincaraiz_antioquia_data_todos_20220207.csv',index = False)