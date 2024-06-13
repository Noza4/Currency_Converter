import requests


def fetch_data(w):
    endpoint = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_IM8aPddlOYmuj7D2ix8scF6jeo8WZYSrpHYN9el9"

    response = requests.get(endpoint)

    if response.status_code == 200:  # 200 is OK
        data = response.json()
        return data["data"][w]

    else:
        return print(f"Failed to fetch data: {response.status_code}")

