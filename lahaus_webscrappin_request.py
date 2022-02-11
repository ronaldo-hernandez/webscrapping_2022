from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from csv import reader
from selenium import webdriver

##medellin - Antioquia
""" urls = []
for x in range(1,51):
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}=&price=100%3A235')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=235%3A280')   
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=280%3A320')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=320%3A359')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=359%3A399')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=399%3A449')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=449%3A488')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=488%3A540')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=540%3A590')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=590%3A660')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=650%3A700')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=700%3A780')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=780%3A890')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=880%3A999')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=1000%3A1300')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=1250%3A1700')
    urls.append(f'https://www.lahaus.com/propiedades/medellin?is_new=false&pagina={x}&price=1700%3A3000')
    urls.append(f'https://www.lahaus.com/propiedades/santa-fe-de-antioquia?is_new=false&pagina={x}')
    urls.append(f'https://www.lahaus.com/propiedades/rionegro?is_new=false&pagina={x}&price=100%3A460')
    urls.append(f'https://www.lahaus.com/propiedades/rionegro?is_new=false&pagina={x}&price=460%3A999')
    urls.append(f'https://www.lahaus.com/propiedades/rionegro?is_new=false&pagina={x}&price=1000%3A3000')
    urls.append(f'https://www.lahaus.com/propiedades/bello?is_new=false&pagina={x}&price=100%3A259')
    urls.append(f'https://www.lahaus.com/propiedades/bello?is_new=false&pagina={x}&price=259%3A3000')
    urls.append(f'https://www.lahaus.com/propiedades/barbosa?is_new=false&pagina={x}')
    urls.append(f'https://www.lahaus.com/propiedades/sabaneta?is_new=false&pagina={x}&price=100%3A330')
    urls.append(f'https://www.lahaus.com/propiedades/sabaneta?is_new=false&pagina={x}&price=330%3A430')
    urls.append(f'https://www.lahaus.com/propiedades/sabaneta?is_new=false&pagina={x}&price=430%3A3000')
    urls.append(f'https://www.lahaus.com/propiedades/guatape?is_new=false&pagina={x}')
    urls.append(f'https://www.lahaus.com/propiedades/oriente-antioqueno?is_new=false&pagina={x}')

links = urls

all_in = []
def extract_urls(url):
    s = HTMLSession()
    r = s.get(url)
    baseurl = 'https://www.lahaus.com'
    urle = r.html.find('div.server-cards article div div:nth-of-type(2) h3 a')
    results = [baseurl + link.attrs['href'] for link in urle]
    data = list(dict.fromkeys(results))
    all_in.extend(data)
    print('Cantidad de links extraídos:',len(all_in))
    return 

with ThreadPoolExecutor() as executor:
    executor.map(extract_urls,links)
all_in = pd.unique(all_in)
df = pd.DataFrame(all_in)
df.to_csv('lahaus_links_antioquia_20220209.csv',index = False) """

###---------------- Extraer links ---------------------------------------####
all_in = []
with open('lahaus_links_antioquia_20220209.csv','r') as f:
    reader_csv = reader(f)
    for row in reader_csv:
        all_in.append(row[0])

all_in = all_in[1:len(all_in)]

register = []
def parse(url):
    s = HTMLSession()
    r = s.get(url)
    try:
        title = r.html.find('h1.font-semibold',first = True).text.strip()
    except:
        title = 'None'
    try:
        place = r.html.find('div.flex h2.font-regular.text-14',first = True).text
    except:
        place = 'None'
    try:
        props_labels = r.html.find('div.col-span-12 section.main-amenities-area div h3')
        props_values = r.html.find('div.col-span-12 section.main-amenities-area p')
        prop_lab_list = []
        for prop_lab in props_labels:
            prop_lab_list.append(prop_lab.text)
        prop_val_list = []
        for prop_val in props_values:
            prop_val_list.append(prop_val.text)
        props = dict(zip(prop_lab_list,prop_val_list))
    except:
        props = 'None'
    try:
        caracts = r.html.find('div.show-more-component div.show-more-content div')
        caracts_list = []
        for cars in caracts:
            caracts_list.append(cars.text)
    except:
        caracts_list = 'None'
    try:
        zonas_comunes = r.html.find('div.grid.grid-cols-2.text-lh-green-gray div')
        zonas_com_list = []
        for zonas in zonas_comunes:
            zonas_com_list.append(zonas.text)
        boolean_list = []
        for zonas in zonas_comunes:
            boolean_list.append('Si')
        zonas_com = dict(zip(zonas_com_list,boolean_list))
    except:
        zonas_com = 'None'
    try:    
        precio = r.html.find('div.flex.justify-center.items-center > h2:nth-child(1)',first = True).text
    except:
        precio = 'None'
    try:
        extras = r.html.find('div.grid.grid-cols-1 div.my-4.font-regular.flex.justify-center.items-center div.mr-3')
        extras_labls = []
        for ex in extras:
            extras_labls.append(ex.text)
        extras2 = r.html.find('div.grid.grid-cols-1 div.my-4.font-regular.flex.justify-center.items-center span.font-medium span')
        extras_values = []
        for ext2 in extras2:
            extras_values.append(ext2.text)
        extrass = dict(zip(extras_labls,extras_values))
    except:
        extrass = 'None'
    try:
        latitude = r.html.find('div.embedded-location-component-wrapper.relative.hidden > div',first = True).get_attribute('latitude')
        longitude = r.html.find('div.embedded-location-component-wrapper.relative.hidden > div',first = True).get_attribute('longitude')
    except:
        latitude = 'None'
        longitude = 'None'
    try:
        buttons =  r.html.find('div.map-filters button')
        nearby_places = []
        for but in buttons:
            nearby_places.append(but.get_attribute('data-heap'))
        boolean_list2 = []
        for but in buttons:
            boolean_list2.append('Si')
        nearby_place = dict(zip(nearby_places,boolean_list2))
    except:
        nearby_place = "None"
    url_page = url
    detal = {
    'titulo':title,
    'ubicacion':place,
    'propiedades':props,
    'caracteristicas':caracts_list,
    'zonas_comunes':zonas_com,
    'precio':precio,
    'valores_extras':extrass,
    'latitude':latitude,
    'longitude':longitude,
    'more_values':nearby_place,
    'url_page':url_page
    }
    register.append(detal)
    print('Size of list is:',len(register))
    return

""" driver = webdriver.Chrome(executable_path = '/Users/Thony/Documents/chromedriver') """
""" register2 = []
def parse_coords(url):
    driver.get(url)
    try:
        latitude = driver.find_element_by_css_selector('div.embedded-location-component-wrapper.relative.hidden > div').get_attribute('latitude')
        longitude = driver.find_element_by_css_selector('div.embedded-location-component-wrapper.relative.hidden > div').get_attribute('longitude')
    except:
        latitude = 'None'
        longitude = 'None'
    try:
        buttons =  driver.find_elements_by_css_selector('div.map-filters button')
        nearby_places = []
        for but in buttons:
            nearby_places.append(but.get_attribute('data-heap'))
        boolean_list2 = []
        for but in buttons:
            boolean_list2.append('Si')
        nearby_place = dict(zip(nearby_places,boolean_list2))
    except:
        nearby_place = "None"
    url_page = url
    dictt = {
        'more_values':nearby_place,'url_page':url_page, 'latitude':latitude,
    'longitude':longitude
    }
    register2.append(dictt)
    return """

""" for url in tqdm(all_in[1:10]):
    parse_coords(url) """

with ThreadPoolExecutor() as executor:
    executor.map(parse,all_in)

df = pd.DataFrame(register)
df.to_csv('lahaus_data_antioquia_20220209.csv', index = False)