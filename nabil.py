import pandas as pd
import datetime

features = pd.DataFrame()
input_data = {
    "year":2023,
    "day": 15,
    "month": 3,
    "P1": 98.65,
    "P2": 2.36,
    "P3": 1.72,
    "P4": 1.52,
    "P5": 1.60,
    "P6": 61.82,
    "P7": 2.72,
    "P8": 8.92,
    "P9": 0.72,
    "P10": 6.49,
    "P11": 0.07
}

def process(body):
    processed_body = {
        "P1": body["P1"],
        "P2": body["P2"],
        "P3": body["P3"],
        "P4": body["P4"],
        "P5": body["P5"],
        "P6": body["P6"],
        "P7": body["P7"],
        "P8": body["P8"],
        "P9": body["P9"],
        "P10": body["P10"],
        "P11": body["P11"],
        "month1": 0,
        "month2": 0,
        "month3": 0,
        "month4": 0,
        "month5": 0,
        "month6": 0,
        "month7": 0,
        "month8": 0,
        "month9": 0,
        "month10": 0,
        "month11": 0,
        "month12": 0,
        "day0": 0,
        "day1": 0,
        "day2": 0,
        "day3": 0,
        "day4": 0,
        "day5": 0,
        "day6": 0,
    }

    day = datetime.datetime(body["year"], body["month"], body["day"]).weekday()
    processed_body[f"day{day}"] = 1
    processed_body[f"month{body['month']}"] = 1

    return processed_body

processed_input = process(input_data)
print(processed_input)

