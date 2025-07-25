import pandas as pd
import urllib.parse
import time
import os

def crime_data_pipeline():
    base_url = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
    query = "date between '2020-01-01T00:00:00' and '2022-12-31T23:59:59'"

    limit = 100000  # API max limit per request
    offset = 0
    all_data = []

    while True:
        params = {
            "$where": query,
            "$limit": limit,
            "$offset": offset
        }
        query_string = urllib.parse.urlencode(params)
        paginated_url = f"{base_url}?{query_string}"

        try:
            chunk = pd.read_json(paginated_url)
        except Exception as e:
            print(f"Error reading JSON from API: {e}")
            break

        if chunk.empty:
            break

        all_data.append(chunk)
        offset += limit
        time.sleep(0.5)  # Avoid hitting API rate limits

    if all_data:
        df = pd.concat(all_data, ignore_index=True)

        cols_to_keep = ['date', 'year', 'primary_type', 'description',
                        'location_description', 'community_area', 'arrest', 'domestic']

        df = df[cols_to_keep].copy()
        df["date"] = pd.to_datetime(df["date"])

        df.dropna(inplace=True)

        os.makedirs("data", exist_ok=True)
        output_path = "data/crimes_chicago.csv"
        df.to_csv(output_path, index=False)
        print(f"Data downloaded and saved to {output_path}")
    else:
        print("No data was downloaded.")

if __name__ == "__main__":
    crime_data_pipeline()