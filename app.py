import requests

def get_coordinates(zip_code):
    url = f"http://api.zippopotam.us/us/{zip_code}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Invalid ZIP code or failed to fetch coordinates.")
    
    data = response.json()
    lat = data['places'][0]['latitude']
    lon = data['places'][0]['longitude']
    return lat, lon

def get_forecast_url(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(url, headers={"User-Agent": "weather-app"})
    if response.status_code != 200:
        raise Exception("Failed to fetch forecast grid data.")
    
    data = response.json()
    return data['properties']['forecast']

def get_forecast(forecast_url):
    response = requests.get(forecast_url, headers={"User-Agent": "weather-app"})
    if response.status_code != 200:
        raise Exception("Failed to fetch forecast data.")
    
    data = response.json()
    today = data['properties']['periods'][0]
    return today['name'], today['temperature'], today['temperatureUnit'], today['detailedForecast']

def main():
    zip_code = input("Enter a US ZIP code: ").strip()
    
    try:
        lat, lon = get_coordinates(zip_code)
        forecast_url = get_forecast_url(lat, lon)
        name, temp, unit, details = get_forecast(forecast_url)

        print(f"\n{name}'s Forecast:")
        print(f"Temperature: {temp}°{unit}")
        print(f"Details: {details}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
