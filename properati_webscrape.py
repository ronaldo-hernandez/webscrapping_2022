import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
import time
from csv import reader
import chompjs
import json
""" ##total ---- properati: 40,000
####------------ Filtro de apartamentos --------------------------------------#### estimado de 25000
#### registros estimado de 1.4M a 230MM : 9631, paginas: 322.
'https://www.properati.com.co/s/antioquia-colombia/venta/precio:1400000-230000000?sort=price_asc&page=322'
### registros estimados de 230MM a 315MM: 9441,paginas : 315
'https://www.properati.com.co/s/antioquia-colombia/venta/precio:230000000-320000000?sort=price_asc&page=315'
### registros estimados de 320MM a 420MM: 9190,paginas : 307
'https://www.properati.com.co/s/antioquia-colombia/venta/precio:320000000-420000000?sort=price_asc&page=307'
### registros estimados de 420MM a 590MM: 9091,paginas : 303
'https://www.properati.com.co/s/antioquia-colombia/venta/precio:420000000-590000000?sort=price_asc&page=303'
### registros estimados de 590MM a 910MM: 9091,paginas : 304
'https://www.properati.com.co/s/antioquia-colombia/venta/precio:590000000-910000000?sort=price_asc&page=304'
### registros estimados de 910MM a 2250MM: 9091,paginas : 305
'https://www.properati.com.co/s/antioquia-colombia/venta/precio:910000000-2250000000?sort=price_asc&page=305'
### registros estimados de 2250MM y +mas: 4917,paginas : 164
'https://www.properati.com.co/s/antioquia-colombia/venta/precio:2250000000-100000000000000000?sort=price_asc&page=164'
#### extracción de links:
links = []
for x in range(1,323):
    links.append(f'https://www.properati.com.co/s/antioquia-colombia/venta/precio:1400000-230000000?sort=price_asc&page={x}')

for x in range(1,316):
    links.append(f'https://www.properati.com.co/s/antioquia-colombia/venta/precio:230000000-320000000?sort=price_asc&page={x}')

for x in range(1,308):
    links.append(f'https://www.properati.com.co/s/antioquia-colombia/venta/precio:320000000-420000000?sort=price_asc&page={x}')

for x in range(1,304):
    links.append(f'https://www.properati.com.co/s/antioquia-colombia/venta/precio:420000000-590000000?sort=price_asc&page={x}')

for x in range(1,305):
    links.append(f'https://www.properati.com.co/s/antioquia-colombia/venta/precio:590000000-910000000?sort=price_asc&page={x}')

for x in range(1,306):
    links.append(f'https://www.properati.com.co/s/antioquia-colombia/venta/precio:910000000-2250000000?sort=price_asc&page={x}')

for x in range(1,165):
    links.append(f'https://www.properati.com.co/s/antioquia-colombia/venta/precio:2250000000-100000000000000000?sort=price_asc&page={x}')

l_links = []
def request(url):
    s = HTMLSession()
    r = s.get(url)
    block = r.html.find('div.StyledCard-sc-6ce7as-1.gxrAFy > div > a')
    baseurl = 'https://www.properati.com.co'
    link_ = [baseurl + link.attrs['href'] for link in block]
    l_links.extend(list(dict.fromkeys(link_)))
    print('Cantidad de links extraídos:',len(l_links))

with ThreadPoolExecutor() as executor:
    executor.map(request,links)

l_links_1 = pd.unique(l_links)
df = pd.DataFrame(l_links_1)
df.to_csv('properati_links_antioquia_20220210.csv',index = False) """
###### extrac data
links = []
with open('properati_links_antioquia_20220210.csv','r') as f:
    reader_csv = reader(f)
    for row in reader_csv:
        links.append(row[0])

links = links[1:len(links)]

all_details = []
def parse(url):
    ### Extract data from url
    s = HTMLSession()
    r = s.get(url)
    ### inform for application/json
    info_css_2 = 'script[type="application/json"]'
    script_txt_2 = r.html.find(info_css_2,first = True).text.strip()
    json_data_2 = chompjs.parse_js_object(script_txt_2)
    ## data_2
    data_2= json.dumps(json_data_2)
    dta_2 = json.loads(data_2)
    ## Information details
    try:
        url_page = dta_2['props']['pageProps']['canonicalUrl']
    except:
        url_page = 'None'
    try:
        internal_id = dta_2['props']['pageProps']['property']['internal_id']
    except:
        internal_id = 'None'
    try:
        title = dta_2['props']['pageProps']['property']['title']
    except:
        title = 'None'
    try:
        description= dta_2['props']['pageProps']['property']['description']
    except:
        description='None'
    try:
        type_registro= dta_2['props']['pageProps']['property']['type']
    except:
        type_registro = 'None'
    try:    
        estr= dta_2['props']['pageProps']['property']['stratum']
    except:
        estr = 'None'
    try:
        direccion= dta_2['props']['pageProps']['property']['address']
    except:
        direccion = 'None'
    try:    
        precio= dta_2['props']['pageProps']['property']['price']['amount']
    except:
        precio = 'None'
    try:
        features = dta_2['props']['pageProps']['property']['features']
    except:
        features = 'None'
    try:
        floor_plant = dta_2['props']['pageProps']['property']['floor_plan']
    except:
        floor_plant = 'None'
    try:
        geo_location = dta_2['props']['pageProps']['property']['place']['parent_names']
    except:
        geo_location = 'None'
        ## coordinates
    try:
        lat = dta_2['props']['pageProps']['property']['geo_point']['lat']
        lon = dta_2['props']['pageProps']['property']['geo_point']['lon']
    except:
        lat = 'None'
        lon = 'None'
    try:
        tag = dta_2['props']['pageProps']['property']['tags']
    except:
        tag = 'None'
    try:
        published_on = dta_2['props']['pageProps']['property']['published_on']
    except:
        published_on = 'None'
    try:
        created_on = dta_2['props']['pageProps']['property']['created_on']
    except:
        created_on = 'None'
    try:
        place = dta_2['props']['pageProps']['property']['place']
    except:
        place = 'None'
    try:
        seller = dta_2['props']['pageProps']['property']['seller']
    except:
        seller = 'None'
    try:
        agent = dta_2['props']['pageProps']['property']['agent']
    except:
        agent = 'None'
    det = {
        'id':internal_id,
        'url_page':url_page,
        'titulo':title,
        'description': description,
        'tipo': type_registro,
        'estrato': estr,
        'direccion':direccion,
        'precio':precio,
        'features':features,
        'floor_plant':floor_plant,
        'lat':lat,
        'lon':lon,
        'published_on':published_on,
        'place':place,
        'seller':seller,
        'agent':agent,
        'tag':tag,
        'create_on':created_on,
        'geo_location':geo_location
        }
    print("La cantidad de registros son:",len(all_details))
    all_details.append(det)
    return

with ThreadPoolExecutor(max_workers = 2) as executor:
    executor.map(parse,links)

df_1 = pd.DataFrame(all_details)

df_1.to_csv('properati_data_antioquia_20220210.csv',index = False)