import json
import chompjs
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
from selenium import webdriver
import time
import pandas as pd
from csv import reader
""" driver = webdriver.Chrome(executable_path = '/Users/Thony/Documents/chromedriver')
url_base = 'https://www.metrocuadrado.com/apartamento-casa-oficina-local-bodega-lote-finca-consultorio-edificio-de-oficinas-edificio-de-apartamentos/venta/bogota'
driver.get(url_base)
driver.find_element_by_css_selector('#__next > div > div > div.Layout__LayoutStyled-sc-9y7jis-0.ibZBWk.page-container > section > div > div > div.disclamer-action.text-center.text-lg-left > a').click()
 """### obtenidos: 9898 --> 0 a 279,900,000$
### obtenidos: 8452 --> 219,900,000$ a 390,000,000$
### obtenidos: 9755 --> 390,000,000$ a 505,000,000$
### obtenidos: 9879 --> 505,000,000$ a 655,000,000$
### obtenidos: 9926 --> 655,000,000$ a 850,000,000$
### obtenidos: 9408 --> 850,000,000$ a 1'149,000,000$
### obtenidos: 9917 --> 1'149,000,000$ a 1'590,000,000$
### obtenidos: 9144 --> 1'590,000,000$ a 2'450,000,000$
### obtenidos: 9809 --> 2'450,000,000$ a 2'450,000,000$
""" precio_desde = driver.find_element_by_css_selector('#__next > div > div > div.Layout__LayoutStyled-sc-9y7jis-0.ibZBWk.page-container > div.Container-u38a83-0.jDuhNh.inner-container.container > div:nth-child(2) > div.Col-sc-14ninbu-0.lfGZKA.d-none.d-sm-block.col-md-4.col-lg-3 > div.sc-jqCOkK.ghoOCR.Panel-sc-1yxh53u-0.hRHiTs.has-filter.card > div > form > form > div:nth-child(1) > input')
precio_desde.send_keys('2450000000')
precio_hasta = driver.find_element_by_css_selector('#__next > div > div > div.Layout__LayoutStyled-sc-9y7jis-0.ibZBWk.page-container > div.Container-u38a83-0.jDuhNh.inner-container.container > div:nth-child(2) > div.Col-sc-14ninbu-0.lfGZKA.d-none.d-sm-block.col-md-4.col-lg-3 > div.sc-jqCOkK.ghoOCR.Panel-sc-1yxh53u-0.hRHiTs.has-filter.card > div > form > form > div:nth-child(2) > input')
precio_hasta.send_keys('9000000000')
driver.find_element_by_css_selector('#filter-price').click()
### extracción de datos
links = []
condition = True
while condition:
    block = driver.find_elements_by_css_selector('div.card-header a.sc-bdVaJa.ebNrSm')
    for e in block:
        i = e.get_attribute('href')
        links.append(i)
        print('Número de link extraido: ', len(links))
    try:
        driver.find_element_by_css_selector('.item-icon-next > a:nth-child(1)').click()
        time.sleep(2)
    except:
        condition = False
 """
urls = []
for x in range(1,10):
    with open(f'links_mc_parte{x}.csv','r') as f:
        reader_csv = reader(f)
        for row in reader_csv:
            urls.append(row[0])

datos = []
def parse(url):
    s = HTMLSession()
    r = s.get(url,timeout = 20)
    info = 'script[type="application/json"]'
    script_txt = r.html.find(info, first = True).text.strip()
    json_data = chompjs.parse_js_object(script_txt)
    data = json.dumps(json_data)
    dt = json.loads(data)
    try:
        price = dt['props']['initialState']['realestate']['basic']['salePrice']
        rentprice = dt['props']['initialState']['realestate']['basic']['rentPrice']
        propertyId = dt['props']['initialState']['realestate']['basic']['propertyId']
        businessType = dt['props']['initialState']['realestate']['basic']['businessType']
        publicationStatus = dt['props']['initialState']['realestate']['basic']['publicationStatus']
        rentTotalPrice = dt['props']['initialState']['realestate']['basic']['rentTotalPrice']
        area = dt['props']['initialState']['realestate']['basic']['area']
        areac = dt['props']['initialState']['realestate']['basic']['areac']
        rooms = dt['props']['initialState']['realestate']['basic']['rooms']
        bathrooms = dt['props']['initialState']['realestate']['basic']['bathrooms']
        garages = dt['props']['initialState']['realestate']['basic']['garages']
        city = dt['props']['initialState']['realestate']['basic']['city']
        zone = dt['props']['initialState']['realestate']['basic']['zone']
        sector = dt['props']['initialState']['realestate']['basic']['sector']
        neighborhood = dt['props']['initialState']['realestate']['basic']['neighborhood']
        commonNeighborhood = dt['props']['initialState']['realestate']['basic']['commonNeighborhood']
        comment = dt['props']['initialState']['realestate']['basic']['comment']
        detail = dt['props']['initialState']['realestate']['basic']['detail']
        companyId = dt['props']['initialState']['realestate']['basic']['companyId']
        companyName = dt['props']['initialState']['realestate']['basic']['companyName']
        companyAddress = dt['props']['initialState']['realestate']['basic']['companyAddress']
        contactPhone = dt['props']['initialState']['realestate']['basic']['contactPhone']
        whatsapp = dt['props']['initialState']['realestate']['basic']['whatsapp']
        propertyState = dt['props']['initialState']['realestate']['basic']['propertyState']
        coord = dt['props']['initialState']['realestate']['basic']['coordinates']
        title = dt['props']['initialState']['realestate']['basic']['title']
        subtitle = dt['props']['initialState']['realestate']['basic']['subtitle']
        featured = dt['props']['initialState']['realestate']['basic']['featured']
        builtTime = dt['props']['initialState']['realestate']['basic']['builtTime']
        stratum = dt['props']['initialState']['realestate']['basic']['stratum']
        linkSeo = dt['props']['initialState']['realestate']['basic']['linkSeo']
        localPhone = dt['props']['initialState']['realestate']['basic']['localPhone']
        details = {
            'price':price,
            'rentprice':rentprice,
            'propertyId':propertyId,
            'businessType':businessType,
            'publicationStatus':publicationStatus,
            'publicationStatus':publicationStatus,
            'rentTotalPrice':rentTotalPrice,
            'rentTotalPrice':rentTotalPrice,
            'area':area,
            'areac':areac,
            'rooms':rooms,
            'bathrooms':bathrooms,
            'garages':garages,
            'city':city,
            'zone':zone,
            'sector':sector,
            'neighborhood':neighborhood,
            'commonNeighborhood':commonNeighborhood,
            'comment':comment,
            'detail':detail,
            'companyID':companyId,
            'companyName':companyName,
            'companyAddress':companyAddress,
            'contactPhone':contactPhone,
            'whatsapp':whatsapp,
            'propertyState':propertyState,
            'coordinates':coord,
            'title':title,
            'subtitle':subtitle,
            'featured':featured,
            'builtTime':builtTime,
            'stratum':stratum,
            'linkSeo':linkSeo,
            'localPhone':localPhone
            }
        datos.append(details)
        print(' Cantidad de datos extraidos :',len(datos))
    except:
        datos.append({})
        print('Fallido',len(details))
    return
### urls
### lenks
### lnks
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(parse,urls) 
fin = time.perf_counter() - start
print('time take :', fin)

df = pd.DataFrame(datos)
print(df.head())

df.to_csv('metro_cuadrado_DATOS20211008.csv',index = False)
df.to_csv('metro_cuadrado_DATOS20211008_pc.csv',index = False,sep = ";")