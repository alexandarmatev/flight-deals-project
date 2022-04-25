import requests

SHEETY_ENDPOINT = "https://api.sheety.co/a057ac7fa91d0db35220cba2a65b96b6/flightdeals/users"
response = requests.get(url=SHEETY_ENDPOINT).json()["users"]

try:
    response[0]
except IndexError:
    api_identifier = 2
else:
    for identifier in response:
        if identifier["email"] != "":
            api_identifier = identifier["id"] + 1


def add_user_data():
    params = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        }
    }
    requests.put(url=f"{SHEETY_ENDPOINT}/{api_identifier}", json=params)
    print("Congratulations! Your details have been added successfully.")


first_name = input("What is your first name?\n")
last_name = input("What is your last name?\n")

emails_match = False
while not emails_match:
    email = input("What is your email?\n")
    email_confirmation = input("Type your email again:\n")

    if email == email_confirmation:
        print("You're in the club!")
        add_user_data()
        emails_match = True
    else:
        print("Your emails don't match. Please try again.")