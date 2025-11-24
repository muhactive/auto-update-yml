import requests
import datetime
import subprocess
from bs4 import BeautifulSoup

def get_html(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Referer": "https://google.com"
    }
    r = session.get(url, headers=headers)
    r.raise_for_status()
    return r.text

    
def pars_product_page(url, categorie_id):
    page = get_html(url)
    soup = BeautifulSoup(page, "lxml")
    
    #NAme product
    name = soup.find("h1", class_="h1-prod-name").text.strip()
    if not name:
        print("Название товара не найдено")
    print(name)
    
    #cod product
    cod_product = soup.find("div", class_="info-model")
    cod_text = cod_product.find("span").text
    if not cod_text:
        print("Код не найден")
    print(cod_text)
    
    #quantity
    quantity = soup.find("span", class_="stock-quantity_success").text
    print(quantity)
    
    #price
    product_price = soup.find("span", class_="autocalc-product-price").text.replace(" грн.", "")
    print(product_price)
    
    #text
    text = soup.find("div", class_="text-opis").text
    print(text)
    
    #image
    list_image = set()
    main_image = soup.find("a", class_="main-image thumbnail")
    if main_image:
        list_image.add(main_image.get("href"))
    else:
        print("Not main image")
        
    images = soup.find_all("a", class_="thumbnail dop-img")
    if images:
        for image in images:
            list_image.add(image.get("href"))
    else:
        print("Not dop images")
    list_images = list(list_image)[:10]   
    print(list_images)
    
    return {
        "id": cod_text,
        "name": name,
        "quantity": quantity,
        "images": list_images,
        "price": product_price,
        "text": text,
        "url": url,
        "category_id": categorie_id,
    }
    
    
def make_yml(product, categorie, filename="lugi.yml"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append(f'<yml_catalog date ="{now}">')
    xml.append('<shop>')
    xml.append('<name>Lugi</name>')
    xml.append('<company>SuperPuperPrice</company>')
    
    #Categori
    
    xml.append('<categories>')
    
    for key, name_prod in categorie.items():
        xml.append(f'   <category id="{key}">{name_prod}</category>')
    xml.append('</categories>')
    
    #Product
    
    xml.append('<offers>')
    for p in product:
        xml.append(f'   <offer id="{p["id"]}" available="true">')
        xml.append(f'       <url>{p["url"]}</url>')
        xml.append(f'       <price>{p["price"]}</price>')
        xml.append('        <currencyID>UAH</currencyID>')
        xml.append(f'       <categoryID>{p["category_id"]}</categoryID>')
        xml.append(f'       <name>{p["name"]}</name>')
        xml.append(f'       <description><![CDATA[{p["text"]}]]></description>')
        for im in p["images"]:
            xml.append(f'       <picture>{im}</picture>')
        xml.append('    </offer>')
    xml.append('</offers>')
    xml.append('</shop>')
    xml.append('</yml_catalog>')
    
    with open (filename, "w", encoding="utf-8") as f:
        f.write("\n".join(xml))
        
    print(f"YML file {filename} is CREATE at:{now}")
    
    
def auto_push_git(repo_path="."):
    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", "auto update yml"],
        ["git", "push"]
    ]
    
    for cmd in commands:
        subprocess.run(cmd, cwd=repo_path)
    print("YML file update on GIT")
    