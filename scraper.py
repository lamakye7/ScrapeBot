import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from data_processor import convert_mileage, process_data

BASE_URL = "https://autochek.africa/gh/cars-for-sale?page_number={}"

# Function to extract total pages
def get_total_pages(soup):
    pagination = soup.select('.MuiPagination-ul button[aria-label^="Go to page"]')
    return int(pagination[-1].text) if pagination else 1

# Function to scrape a single page
# def scrape_page(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     cars = []
#     for listing in soup.select('.MuiStack-root.css-huyd7c'):  # Main container for car listings
#         # Extract Car Name
#         car_name = listing.find("h6", class_="MuiTypography-root MuiTypography-h6 css-1g399u0")
#         car_name = car_name.get_text(strip=False) if car_name else "N/A"

#         # Extract Condition, Mileage, Engine Type
#         attributes = [span.get_text(strip=True) for span in listing.find_all("span", class_="MuiChip-label MuiChip-labelSmall css-1pjtbja")]
#         condition = attributes[0] if len(attributes) > 0 else "N/A"
#         mileage = attributes[1] if len(attributes) > 1 else "N/A"
#         engine_type = attributes[2] if len(attributes) > 2 else "N/A"

#         # Extract Price
#         price = listing.find("p", class_="MuiTypography-root MuiTypography-body1 css-1bztvjj")
#         price = price.get_text(strip=True) if price else "N/A"

    #     # Extract Location
    #     location = listing.find("span", class_="MuiTypography-root MuiTypography-caption css-umr6w4")
    #     location = location.get_text(strip=True) if location else "N/A"

    #     # Store data
    #     cars.append({
    #         'Car Name': car_name,
    #         'Condition': condition,
    #         'Mileage': mileage,
    #         'Engine Type': engine_type,
    #         'Price': price,
    #         'Location': location
    #     })

    # return cars

def scrape_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    car_blocks = soup.select("div.MuiStack-root.css-1ljw75u")
    listings = []

    for block in car_blocks:
        name_tag = block.select_one("h6.MuiTypography-root.MuiTypography-h6.css-1g399u0")
        tags = block.select("span.MuiChip-label")
        rating_tag = block.select_one("div.MuiChip-root.css-1ac0wpd span.MuiChip-label")
        price_tag = block.select_one("p.MuiTypography-root.css-1bztvjj")
        location_tag = block.select_one("span.MuiTypography-root.css-umr6w4")

        listing = {
            "Car Name": name_tag.text.strip() if name_tag else "",
            "Condition": tags[0].text.strip() if len(tags) > 0 else "",
            "Mileage": tags[1].text.strip() if len(tags) > 1 else "",
            "Engine Type": tags[2].text.strip() if len(tags) > 2 else "",
            "Rating": rating_tag.text.strip() if rating_tag else "",
            "Price": price_tag.text.strip() if price_tag else "",
            "Location": location_tag.text.strip() if location_tag else "",
        }

        listings.append(listing)
    
    return listings
    
# Get the first page and extract total pages
first_page_url = BASE_URL.format(1)
response = requests.get(first_page_url)
soup = BeautifulSoup(response.text, 'html.parser')
total_pages = get_total_pages(soup)

# Scrape all pages
all_cars = []
for page in range(1, total_pages + 1):
    print(f"Scraping page {page}/{total_pages}...")
    page_url = BASE_URL.format(page)
    all_cars.extend(scrape_page(page_url))
    time.sleep(2)  # Avoid getting blocked

# call the funtion
process_data(all_cars)

