from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def scrape_poorvika_product(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36"
        )

         
    service = Service("C:\\Users\\User\\Downloads\\chromedriver-win64 (2)\\chromedriver-win64\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        product_name = soup.find('h1', class_= 'center-content_product_name__O9C4s').get_text(strip=True)
        
        price_div = soup.find('div', class_= 'center-content_price_special__LGEjP')
        price = price_div.find('b').get_text(strip=True) if price_div else "Price not available"

        return {"product_name": product_name, "price": price}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

    finally:
        
        driver.quit()


def main():
    
    url = "https://www.poorvika.com/asus-vivobook-16-intel-core-i5-13th-gen-windows-11-home-laptop-x1605va-mb1627ws-transparent-silver-16gb-512gb/p"
    product_details = scrape_poorvika_product(url)
    print(product_details)


if __name__ == "__main__":
    main()