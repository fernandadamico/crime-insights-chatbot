import pandas as pd
import urllib.parse
import time
import os

def download_crime_data():
    base_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    query = "date between '2020-01-01T00:00:00' and '2022-12-31T23:59:59'"

    limit = 1000  # API max limit per request
    offset = 0
    all_data = []

    while True:
        # Build URL with query parameters properly
        params = {
            "$where": query,
            "$limit": limit,
            "$offset": offset
        }
        query_string = urllib.parse.urlencode(params)
        paginated_url = f"{base_url}?{query_string}"

        print(f"Downloading data with offset {offset}...")

        try:
            chunk = pd.read_json(paginated_url)
        except Exception as e:
            print(f"Error reading JSON from API: {e}")
            break

        if chunk.empty:
            print("No more data to download.")
            break

        all_data.append(chunk)
        offset += limit
        time.sleep(0.5)  # Sleep to avoid overloading the API

    if all_data:
        df = pd.concat(all_data, ignore_index=True)

        cols_to_keep = ['date', 'year', 'primary_type', 'description',
                        'location_description', 'community_area', 'arrest', 'domestic']

        df = df[cols_to_keep].copy()
        df["date"] = pd.to_datetime(df["date"])

        # Create 'data' folder if it doesn't exist
        os.makedirs("data", exist_ok=True)
        output_path = "data/crimes_chicago.csv"
        df.to_csv(output_path, index=False)
        print(f"Data downloaded and saved to {output_path}")
    else:
        print("No data was downloaded.")

if __name__ == "__main__":
    download_crime_data()
