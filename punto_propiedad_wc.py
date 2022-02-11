from selenium import webdriver
import time
import pandas as pd
from csv import reader
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

#### Creamos loops para extraer los links apriori
links = []
for x in range(2,282):
    urls = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_0-230000000-precio/p_{x}'
    links.append(urls)

r = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_0-230000000-precio'
links.append(r)

for x in range(2,298):
    urls = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_230000001-310000000-precio/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_230000001-310000000-precio')

for x in range(2,284):
    urls = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_310000000-380000000-precio/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_310000000-380000000-precio')

for x in range(2,281):
    urls = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_380000000-480000000-precio/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_380000000-480000000-precio')

for x in range(2,294):
    urls = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_480000000-650000000-precio/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_480000000-650000000-precio')

for x in range(2,279):
    urls = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_650000000-970000000-precio/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_650000000-970000000-precio')

for x in range(2,287):
    urls = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_970000000-3000000000-precio/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_970000000-3000000000-precio')

for x in range(2,50):
    urls = f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_3000000000-1000000000000000000000000-precio/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/residenciales/antioquia/list/f_3000000000-1000000000000000000000000-precio')

for x in range(2,26):
    urls = f'https://www.puntopropiedad.com/venta/bodegas/antioquia/list/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/bodegas/antioquia/list')

for x in range(2,80):
    urls = f'https://www.puntopropiedad.com/venta/locales-comerciales/antioquia/list/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/locales-comerciales/antioquia/list')

for x in range(2,53):
    urls = f'https://www.puntopropiedad.com/venta/oficinas/antioquia/list/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/oficinas/antioquia/list')

for x in range(2,256):
    urls = f'https://www.puntopropiedad.com/venta/lotes-terrenos/antioquia/list/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/lotes-industriales/antioquia/list')
links.append(f'https://www.puntopropiedad.com/venta/lotes-terrenos/antioquia/list')
links.append(f'https://www.puntopropiedad.com/venta/proyectos/antioquia/list')

for x in range(2,181):
    urls = f'https://www.puntopropiedad.com/venta/fincas/antioquia/list/p_{x}'
    links.append(urls)

links.append(f'https://www.puntopropiedad.com/venta/fincas/antioquia/list')

### Se genera el driver usando selenium
driver = webdriver.Chrome(executable_path = '/Users/Thony/Documents/chromedriver')
urls_macro = []
for url in tqdm(links):
    driver.get(url)
    ## se le da actualizar a la pagina para aceptar cookies
    tab = driver.find_elements_by_css_selector('div.ad-data > div.data > h2 > a')
    for t in tab:
        urls_macro.append(t.get_property('href'))
    
links1 = pd.unique(urls_macro)
df = pd.DataFrame(links1)
df.to_csv('punto_propiedad_links_antioquia_20220208.csv',index = False)
### importing the urls
""" urls = []
with open('links_pp_uniques.csv','r') as f:
    read_csv = reader(f)
    for row in read_csv:
        urls.append(row[0]) """

""" urls = urls[2:26645] """

all_in = []
def parse(url):
    try:
        s = HTMLSession()
        r = s.get(url)
        title = r.html.find('div#firstLine div h1',first = True).text
        subtitle = r.html.find('div#firstLine div h2',first = True).text
        name_client = r.html.find('a.agency-listing-link div',first = True).text
        price = r.html.find('div.price h2',first = True).text
        detail_list = r.html.find('div.priceChars ul.details_list li')
        details_list = []
        for det in detail_list:
            details_list.append(det.text)
        address = r.html.find('span.location_info',first = True).text
        description = r.html.find('div.info p.description',first = True).text
        caract_int = r.html.find('div.dropdown-list.open.col-md4 ul.list li')
        carac_int_list = []
        for car_int in caract_int:
            carac_int_list.append(car_int.text)
        caract_ext = r.html.find('div.dropdown-list.open.col-md6 ul.list li')
        carac_ext_list = []
        for car_ext in caract_ext:
            carac_ext_list.append(car_ext.text)
        caract_entorno = r.html.find('div.dropdown-list.open ul.list.col-md3 li')
        carac_ent_list = []
        for car_ent in caract_entorno:
            carac_ent_list.append(car_ent.text)
        location = r.html.find('div.dropdown-list.light.open.map-section div button',first = True).attrs
        lat = location['data-x']
        lon = location['data-y']
        detalles = {
            'titles':title,
            'subtitle':subtitle,
            'name_client':name_client,
            'price':price,
            'details_list':details_list,
            'address':address,
            'description':description,
            'caracteristicas_interiores':carac_int_list,
            'caracteristicas_exteriores':carac_ext_list,
            'caracteristicas_entorno':carac_ent_list,
            'latitude':lat,
            'longitude':lon,
            'url_page':url
        }
        all_in.append(detalles)
        print('link parsed:',len(all_in))
    except:
        all_in.append({})
        print('link parsed empty:',len(all_in))
    return

start = time.perf_counter()
with ThreadPoolExecutor() as executor:
    executor.map(parse,urls)
fin = time.perf_counter() - start
print('Time taken:',fin)

df = pd.DataFrame(all_in)
df['titles'] = df['titles'].str.replace('\n','')
df['subtitle'] = df['subtitle'].str.replace('\n','')
df['name_client'] = df['name_client'].str.replace('\n','')
df['address'] = df['address'].str.replace('\n','')
df['description'] = df['description'].str.replace('\n','')

df['titles'] = df['titles'].str.replace('\\n','')
df['subtitle'] = df['subtitle'].str.replace('\\n','')
df['name_client'] = df['name_client'].str.replace('\\n','')
df['address'] = df['address'].str.replace('\\n','')
df['description'] = df['description'].str.replace('\\n','')

df['titles'] = df['titles'].str.replace('\r','')
df['subtitle'] = df['subtitle'].str.replace('\r','')
df['name_client'] = df['name_client'].str.replace('\r','')
df['address'] = df['address'].str.replace('\r','')
df['description'] = df['description'].str.replace('\r','')

df['titles'] = df['titles'].str.replace('\\','')
df['subtitle'] = df['subtitle'].str.replace('\\','')
df['name_client'] = df['name_client'].str.replace('\\','')
df['address'] = df['address'].str.replace('\\','')
df['description'] = df['description'].str.replace('\\','')

df['titles'] = df['titles'].str.replace('\\r','')
df['subtitle'] = df['subtitle'].str.replace('\\r','')
df['name_client'] = df['name_client'].str.replace('\\r','')
df['address'] = df['address'].str.replace('\\r','')
df['description'] = df['description'].str.replace('\\r','')

df['titles'] = df['titles'].str.replace(';','')
df['subtitle'] = df['subtitle'].str.replace(';','')
df['name_client'] = df['name_client'].str.replace(';','')
df['address'] = df['address'].str.replace(';','')
df['description'] = df['description'].str.replace(';','')

df['titles'] = df['titles'].str.replace('\r\n','')
df['subtitle'] = df['subtitle'].str.replace('\r\n','')
df['name_client'] = df['name_client'].str.replace('\r\n','')
df['address'] = df['address'].str.replace('\r\n','')
df['description'] = df['description'].str.replace('\r\n','')

df.to_csv('punto_propiedad_data_todos_20220208.csv',index = False,sep = ';')

