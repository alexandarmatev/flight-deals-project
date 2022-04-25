from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from datetime import datetime, timedelta

flight_search = FlightSearch()
data_manager = DataManager()
response_sheety_data = data_manager.get_sheety_data()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "LON"

for index in range(len(response_sheety_data)):
    if response_sheety_data[index]["iataCode"] == "":
        for row in response_sheety_data:
            row["iataCode"] = flight_search.get_destination_code(row["city"])
        print(f"sheet_data:\n {response_sheety_data}")

        data_manager.destination_data = response_sheety_data
        data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=180)
formatted_tomorrow = tomorrow.strftime("%d/%m/%Y")
formatted_six_months = six_month_from_today.strftime("%d/%m/%Y")

for destination in response_sheety_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=formatted_tomorrow,
        to_time=formatted_six_months
    )
    try:
        if flight.price < destination["lowestPrice"]:
            data_manager.update_price(flight.price, destination["id"])
            for data in range(len(data_manager.users_data)):
                emails = data_manager.users_data[data]['email']
                message = f"Hello {data_manager.users_data[data]['firstName']},\n\n" \
                          f"This is the Google flight link for a flight from {flight.origin_airport} to " \
                          f"{flight.destination_airport} from {flight.out_date} to {flight.return_date}."
                if flight.stop_overs > 0:
                    message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
                link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}." \
                       f"{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}." \
                       f"{flight.origin_airport}.{flight.return_date}"
                notification_manager.send_emails(emails=emails, message=message, link=link)

    except AttributeError:
        pass

    # notification_manager.send_sms(
    #     message=f"Low price alert! Only £{flight.price} to fly from "
    #             f"{flight.origin_city}-{flight.origin_airport} "
    #             f"to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} "
    #             f"to {flight.return_date}"
    # )
