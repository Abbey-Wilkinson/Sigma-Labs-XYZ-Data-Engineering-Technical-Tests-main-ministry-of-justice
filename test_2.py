# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type

import pandas as pd
import requests

BASE_POSTCODE_REQUEST = "https://www.find-court-tribunal.service.gov.uk/search/results.json?postcode="


def load_people_csv(csv_file) -> list[dict]:
    people = pd.read_csv(csv_file)

    people = people.to_dict('records')

    return people


def get_tribunal_info_from_postcode(person: dict) -> list[dict]:

    postcode = person["home_postcode"]

    response = requests.get(
        f'{BASE_POSTCODE_REQUEST}{postcode.upper()}')

    data = response.json()

    return data


def find_wanted_court_type(person: dict, courts: list[dict]) -> list[dict]:

    wanted_type = person["looking_for_court_type"]

    potential_courts = []

    for court in courts:
        type = court["types"]

        if type == []:
            continue

        else:
            new_type = type[0]

        if new_type == wanted_type:
            potential_courts.append(court)

    return potential_courts


def get_minimum_distance_of_potential_courts(potential_courts: list[dict]):

    min_distance_court = min(
        potential_courts, key=lambda court: court['distance'])

    return min_distance_court


def main():

    people = load_people_csv("people.csv")

    names = []
    desired_court = []
    home_postcode = []

    for person in people:
        postcode = person["home_postcode"]
        wanted_court = person["looking_for_court_type"]
        tribunal_info = get_tribunal_info_from_postcode(person)
        potential_courts = find_wanted_court_type(person, tribunal_info)
        min_distance_court = get_minimum_distance_of_potential_courts(
            potential_courts)


if __name__ == "__main__":
    # [TODO]: write your answer here
    people = load_people_csv("people.csv")

    tribunal_info = get_tribunal_info_from_postcode(people[0])

    potential_courts = find_wanted_court_type(people[0], tribunal_info)
    print(potential_courts)

    min_distance_court = get_minimum_distance_of_potential_courts(
        potential_courts)
    print(min_distance_court)
