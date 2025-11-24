from scraping import get_html, pars_product_page, auto_push_git, make_yml
from product_list import PRODUCT_LIST, CATEGORY_ID
#url = "https://lugi.com.ua/girlyanda-shtora-hvojnaya-lapa-svetodiodnaya-400-led-3h2-m-zhovtyj/"

def main():
    product = []
    for url, categ in PRODUCT_LIST:
        try:
            p = pars_product_page(url, categ)
            product.append(p)
            print(f'OK append {p["name"]}')
        except Exception as e:
            print("Error:", e)
            
    make_yml(product, CATEGORY_ID)
    
    auto_push_git()
            
if __name__ == "__main__":
    main()