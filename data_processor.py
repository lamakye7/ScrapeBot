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
