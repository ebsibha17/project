from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def scrape_sathya_product(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36"
    )

    service = Service("C:\\Users\\User\\Downloads\\chromedriver-win64 (2)\\chromedriver-win64\\chromedriver.exe")  # Set your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # 🔹 Locate the parent div that contains the product title
        title_div = soup.find('div', class_='product-right')
        product_name = title_div.find('h2').get_text(strip=True) if title_div else "Title not found"

        # 🔹 Locate the parent div that contains the product price
        price_div = soup.find('div', class_='col-sm-3')
        product_price = price_div.find('h3').get_text(strip=True) if price_div else "Price not found"

        return {"product_name": product_name, "price": product_price}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

    finally:
        driver.quit()


def main():
    url = "https://www.sathya.store/category/computers/laptops/hp-laptop-intel-core-i3-13th-gen-8-gb-512-gb-ssdwindows-11-home-hp15sfd0186tuci3"
    product_details = scrape_sathya_product(url)
    print(product_details)


if __name__ == "__main__":
    main()


