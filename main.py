import os
import requests
import zipfile

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

def download_and_extract_file(uri):
    filename = uri.split("/")[-1]

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    response = requests.get(uri)
    with open(os.path.join("downloads", filename), "wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(os.path.join("downloads", filename), "r") as zip_ref:
        csv_file = [f for f in zip_ref.namelist() if f.lower().endswith('.csv')][0]
        zip_ref.extract(csv_file, path="downloads")

    os.remove(os.path.join("downloads", filename))

    with zipfile.ZipFile("all_downloaded_data.zip", "a") as archive:
        archive.write(os.path.join("downloads", csv_file), arcname=csv_file)

def main():
    for uri in download_uris:
        download_and_extract_file(uri)

if __name__ == "__main__":
    main()
