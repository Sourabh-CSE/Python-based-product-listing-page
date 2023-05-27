import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_listings(url, num_pages):
    base_url = url.split('pg_')[0] + 'pg_{}'  # URL pattern for pagination

    all_products = []
    for page in range(1, num_pages + 1):
        page_url = base_url.format(page)
        print("Scraping page:", page_url)
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        for product in products:
            product_url = product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
            product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
            product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
            rating_element = product.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.text.strip() if rating_element else 'N/A'
            reviews_element = product.find('span', {'class': 'a-size-base'})
            reviews = reviews_element.text.strip() if reviews_element else 'N/A'

            all_products.append({
                'Product URL': 'https://www.amazon.in' + product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': rating,
                'Number of reviews': reviews
            })

    return all_products

def scrape_product_details(products):
    for product in products:
        product_url = product['Product URL']
        print("Scraping product:", product_url)
        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        asin_element = soup.find('th', text='ASIN')
        asin = asin_element.find_next('td').text.strip() if asin_element else 'N/A'
        description_element = soup.find('div', {'id': 'productDescription'})
        description = description_element.text.strip() if description_element else 'N/A'
        manufacturer_element = soup.find('div', {'id': 'bylineInfo'})
        manufacturer = manufacturer_element.text.strip() if manufacturer_element else 'N/A'

        product['Description'] = description
        product['ASIN'] = asin
        product['Product Description'] = description
        product['Manufacturer'] = manufacturer

    return products

def export_to_csv(data, filename):
    keys = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Set the URL and number of pages to scrape
url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
num_pages = 20

# Scrape product listings
products = scrape_product_listings(url, num_pages)

# Scrape product details
products_with_details = scrape_product_details(products)

# Export data to CSV file
filename = 'product_data.csv'
export_to_csv(products_with_details, filename)

print("Data exported to", filename)
