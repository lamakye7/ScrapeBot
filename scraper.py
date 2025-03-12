import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = "https://autochek.africa/ng/cars-for-sale?page_number={}"

# Function to extract total pages
def get_total_pages(soup):
    pagination = soup.select('.MuiPagination-ul button[aria-label^="Go to page"]')
    return int(pagination[-1].text) if pagination else 1

# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    cars = []
    for listing in soup.select('.MuiStack-root.css-huyd7c'):  # Main container for car listings
        # Extract Car Name
        car_name = listing.find("h6", class_="MuiTypography-root MuiTypography-h6 css-1g399u0")
        car_name = car_name.get_text(strip=False) if car_name else "N/A"

        # Extract Condition, Mileage, Engine Type
        attributes = [span.get_text(strip=True) for span in listing.find_all("span", class_="MuiChip-label MuiChip-labelSmall css-1pjtbja")]
        condition = attributes[0] if len(attributes) > 0 else "N/A"
        mileage = attributes[1] if len(attributes) > 1 else "N/A"
        engine_type = attributes[2] if len(attributes) > 2 else "N/A"

        # Extract Price
        price = listing.find("p", class_="MuiTypography-root MuiTypography-body1 css-1bztvjj")
        price = price.get_text(strip=True) if price else "N/A"

        # Extract Location
        location = listing.find("span", class_="MuiTypography-root MuiTypography-caption css-umr6w4")
        location = location.get_text(strip=True) if location else "N/A"

        # Store data
        cars.append({
            'Car Name': car_name,
            'Condition': condition,
            'Mileage': mileage,
            'Engine Type': engine_type,
            'Price': price,
            'Location': location
        })

    return cars

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


# Convert Mileage to Miles (Remove 'K' and convert kms to miles)
def convert_mileage(mileage):
    parts = mileage.split()
    # Ensure there is at least one part (value)
    if len(parts) == 2:
        value, unit = parts
    elif len(parts) == 1:
        value, unit = parts[0], "miles"  # Assume miles if the unit is missing
    else:
        return None  # Handle unexpected cases
    # Handle non-numeric values
    if not value.replace("K", "").replace(".", "").isdigit():
        return None  # Return None for non-numeric values like 'local'

    value = float(value.replace("K", "")) * 1000  # Convert K to number
    if unit == "kms":
        value *= 0.621371  # Convert km to miles
    return int(value)


def process_data(all_cars):
    df = pd.DataFrame(all_cars)
    # Extract Year from Car Name
    df["Year"] = df["Car Name"].str.split().str[0].astype(int)
    # Convert Price to Integer
    df["Price"] = df["Price"].str.replace("₦", "").str.replace(",", "").astype(int)
    # convert to miles
    df["Mileage"] = df["Mileage"].apply(convert_mileage)
    # Reorder Columns
    df = df[["Year", "Car Name", "Condition", "Mileage", "Engine Type", "Price", "Location"]]
    # Display DataFrame
    df.to_csv('autochek_cars.csv', index=False)
# call the funtion
process_data(all_cars)
print(f"Scraped {len(all_cars)} cars. Data saved to 'autochek_cars.csv'")
