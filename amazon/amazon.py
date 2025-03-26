import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Function to get Amazon Price
def get_amazon_price(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Scraping the price element (you may need to inspect the page to get the correct class or ID)
    price = soup.find("span", {"id": "priceblock_ourprice"})
    
    if price:
        return float(price.text.replace("₹", "").replace(",", "").strip())
    else:
        return None

# Function to get Myntra Price
def get_myntra_price(product_url):
    # Using Selenium to handle JavaScript-rendered pages
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    driver.get(product_url)
    time.sleep(3)  # Wait for page to load

    try:
        price = driver.find_element(By.CLASS_NAME, "pdp-price")
        price = price.text.strip().replace("₹", "").replace(",", "")
        driver.quit()
        return float(price)
    except Exception as e:
        driver.quit()
        return None

# Function to compare prices
def compare_prices(amazon_url, myntra_url):
    amazon_price = get_amazon_price(amazon_url)
    myntra_price = get_myntra_price(myntra_url)
    
    print(f"Amazon Price: ₹{amazon_price if amazon_price else 'Not available'}")
    print(f"Myntra Price: ₹{myntra_price if myntra_price else 'Not available'}")
    
    if amazon_price and myntra_price:
        if amazon_price < myntra_price:
            print("Amazon has a better price!")
        elif myntra_price < amazon_price:
            print("Myntra has a better price!")
        else:
            print("Both websites have the same price.")
    else:
        print("Could not fetch price from one or both websites.")

# Example usage:
amazon_product_url = "https://www.amazon.in/dp/B08J6F174Z"  # Replace with your desired product URL
myntra_product_url = "https://www.myntra.com/shoes"  # Replace with your desired product URL

compare_prices(amazon_product_url, myntra_product_url)
