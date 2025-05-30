import requests
from datetime import datetime
import os

GENDER = "Male"
WEIGHT_KG = 50
HEIGHT_CM = 180
AGE = 21

APP_ID = os.environ["NT_app_id"]
API_KEY = os.environ["NT_app_key"]


def main():
    exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    sheet_endpoint = os.environ["sheety_endpoint"]

    exercise_text = input("Tell me which exercises you did: ")

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
    }

    parameters = {
        "query": exercise_text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    response = requests.post(exercise_endpoint, json=parameters, headers=headers)
    result = response.json()

    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    bearer_headers = {
        "Authorization": f"Bearer {os.environ['TOKEN']}"
    }

    for exercise in result["exercise"]:
        sheet_inputs = {
            "workout": {
                "date": today_date,
                "time": now_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

        sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)

        print(sheet_response.text)


if __name__ == "__main__":
    main()
