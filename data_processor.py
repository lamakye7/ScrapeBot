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

    # Extract Year from Car Name (first 4-digit number)
    df["Year"] = df["Car Name"].str.extract(r"(\d{4})").astype(float).astype("Int64")

    # Convert Price to Integer
    df["Price"] = pd.to_numeric(
        df["Price"].str.replace("₦", "").str.replace(",", ""), errors="coerce"
    ).astype("Int64")

    # Convert Mileage to miles
    df["Mileage"] = df["Mileage"].apply(convert_mileage)

    # Reorder Columns
    df = df[["Year", "Car Name", "Condition", "Mileage", "Engine Type", "Price", "Location"]]

    # Save to CSV
    df.to_csv('autochek_cars.csv', index=False)

    print(f"Processed and saved {len(df)} car listings.")
