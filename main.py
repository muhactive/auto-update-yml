from scraping import get_html, pars_product_page
from product_list import PRODUCT_LIST, CATEGORY_ID
#url = "https://lugi.com.ua/girlyanda-shtora-hvojnaya-lapa-svetodiodnaya-400-led-3h2-m-zhovtyj/"

def main():
    for category, urls in PRODUCT_LIST.items():
        for url in urls:
            pars_product_page(url)
    
if __name__ == "__main__":

    
    main()