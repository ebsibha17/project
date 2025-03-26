from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Function to initialize the Selenium WebDriver
def init_driver():
    options = Options()
    options.headless = True  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(options=options)
    return driver

# Function to scrape Amazon
def scrape_amazon(search_term):
    url = f"https://www.amazon.in/s?k={search_term.replace(' ', '+')}"
    
    driver = init_driver()
    driver.get(url)
    
    # Wait for the product list to load with an extended timeout (20 seconds)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".a-size-medium.a-color-base.a-text-normal")))
    except Exception as e:
        print("Timeout waiting for Amazon page to load", e)
        driver.quit()
        return [], []

    # Get product names and prices
    products = driver.find_elements(By.CSS_SELECTOR, ".a-size-medium.a-color-base.a-text-normal")
    prices = driver.find_elements(By.CSS_SELECTOR, ".a-price-whole")
    
    amazon_products = [product.text.strip() for product in products]
    amazon_prices = [price.text.strip().replace(",", "") for price in prices]

    driver.quit()
    
    return amazon_products, amazon_prices

# Function to scrape Flipkart
def scrape_flipkart(search_term):
    url = f"https://www.flipkart.com/search?q={search_term.replace(' ', '%20')}"
    
    driver = init_driver()
    driver.get(url)
    
    # Wait for the product list to load with an extended timeout (20 seconds)
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.IRpwTa")))
    except Exception as e:
        print("Timeout waiting for Flipkart page to load", e)
        driver.quit()
        return [], []

    # Get product names and prices
    products = driver.find_elements(By.CSS_SELECTOR, "a.IRpwTa")
    prices = driver.find_elements(By.CSS_SELECTOR, "div._30jeq3")
    
    flipkart_products = [product.text.strip() for product in products]
    flipkart_prices = [price.text.strip().replace(",", "") for price in prices]
    
    driver.quit()
    
    return flipkart_products, flipkart_prices

# Compare products from Amazon and Flipkart and save data in a single Excel file with separate sheets
def compare_prices(search_term):
    # Scrape data from Amazon
    amazon_products, amazon_prices = scrape_amazon(search_term)

    # Scrape data from Flipkart
    flipkart_products, flipkart_prices = scrape_flipkart(search_term)

    # If either Amazon or Flipkart data is empty, print a message and exit
    if not amazon_products or not flipkart_products:
        print(f"No data found for {search_term}.")
        return

    # Create DataFrame for Amazon
    amazon_df = pd.DataFrame({
        'Amazon Product': amazon_products,
        'Amazon Price (INR)': amazon_prices
    })

    # Create DataFrame for Flipkart
    flipkart_df = pd.DataFrame({
        'Flipkart Product': flipkart_products,
        'Flipkart Price (INR)': flipkart_prices
    })

    # Save both DataFrames to a single Excel file with separate sheets
    with pd.ExcelWriter(f"price_comparison_{search_term}.xlsx") as writer:
        amazon_df.to_excel(writer, sheet_name="Amazon", index=False)
        flipkart_df.to_excel(writer, sheet_name="Flipkart", index=False)

    print(f"Data saved to price_comparison_{search_term}.xlsx with separate sheets for Amazon and Flipkart.")

# Example: Compare "laptop"
search_term = "laptop"
compare_prices(search_term)
