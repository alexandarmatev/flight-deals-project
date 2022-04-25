import requests

SHEETY_API_ENDPOINT = "https://api.sheety.co/a057ac7fa91d0db35220cba2a65b96b6/flightdeals/prices"
SHEETY_API_USERS_ENDPOINT = "https://api.sheety.co/a057ac7fa91d0db35220cba2a65b96b6/flightdeals/users"


class DataManager:
    def __init__(self):
        self.destination_data = {}
        self.users_data = requests.get(url=SHEETY_API_USERS_ENDPOINT).json()['users']

    def get_sheety_data(self):
        search_result = requests.get(url=SHEETY_API_ENDPOINT)
        data = search_result.json()
        self.destination_data = data['prices']
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            requests.put(
                url=f"{SHEETY_API_ENDPOINT}/{city['id']}",
                json=new_data
            )

    def update_price(self, new_price, identifier):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        requests.put(
            url=f"{SHEETY_API_ENDPOINT}/{identifier}",
            json=new_data
        )

