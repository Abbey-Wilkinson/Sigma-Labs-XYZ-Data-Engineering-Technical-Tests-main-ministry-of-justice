# pylint: disable=C0301,W0622,C0103
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
MAX_POSTCODE_LEN = 8
MIN_POSTCODE_LEN = 6

MAX_NUM_POSTCODE = 3
MIN_NUM_POSTCODE = 1


def load_people_csv(csv_file) -> list[dict]:
    """Loads the people csv and converts it into a list of dictionaries."""
    people = pd.read_csv(csv_file)

    people = people.to_dict('records')

    return people


def get_tribunal_info_from_postcode(person: dict) -> list[dict]:
    """Gets all the tribunal and court information for a particular postcode
    based on where the person's home postcode is and returns all the data if found."""

    postcode = person["home_postcode"]

    if MAX_POSTCODE_LEN < len(postcode) < MIN_POSTCODE_LEN:
        return {"message": f'Invalid postcode {postcode}'}
    digit_count = 0
    for letter in postcode:
        if letter.isdigit():
            digit_count += 1
    if MAX_NUM_POSTCODE < digit_count < MIN_NUM_POSTCODE:
        return {"message": f'Invalid postcode {postcode}'}

    try:

        response = requests.get(
            f'{BASE_POSTCODE_REQUEST}{postcode.upper()}', timeout=5)

        data = response.json()

        if data:
            return data
        return "Error. No data."

    except requests.exceptions.Timeout:
        return "The request has timed out."


def find_wanted_court_type(person: dict, courts: list[dict]) -> list[dict]:
    """Returns the matching courts to the court type the person is looking for. """

    wanted_type = person["looking_for_court_type"]

    potential_courts = []

    for court in courts:
        type = court["types"]

        if type == []:
            continue

        for t in type:
            if t == wanted_type:
                potential_courts.append(court)

    if not potential_courts:
        return "Error. No courts found with that type."

    return potential_courts


def get_min_dis_of_potential_courts(potential_courts: list[dict]) -> dict:
    """Returns the minimum distance court out of all of the potential courts."""

    min_distance_court = min(
        potential_courts, key=lambda court: court['distance'])

    return min_distance_court


def find_dx_number_of_closest_court(closest_court: dict) -> str:
    """Returns the dx_number of the closest court."""
    try:
        if closest_court["dx_number"]:
            return closest_court["dx_number"]
        return "dx_number blank."
    except KeyError:
        return "No dx_number key found."


def main():
    """Returns a Dataframe of all peoples information with their closest court name,
    dx_number and distance from their home_postcode."""

    people = load_people_csv("people.csv")

    closest_tribunal_df = pd.DataFrame({
                                       "name": [],
                                       "type of court desired": [],
                                       "home postcode": [],
                                       "nearest court of desired type": [],
                                       "dx_number": [],
                                       "distance": []})
    for person in people:
        name = person["person_name"]
        postcode = person["home_postcode"]
        desired_court = person["looking_for_court_type"]
        tribunal_info = get_tribunal_info_from_postcode(person)
        potential_courts = find_wanted_court_type(person, tribunal_info)
        min_distance_court = get_min_dis_of_potential_courts(
            potential_courts)
        name_of_closest_court = min_distance_court["name"]
        dx_number = find_dx_number_of_closest_court(min_distance_court)
        if not dx_number:
            dx_number = "NaN"
        distance = min_distance_court["distance"]

        new_row = {"name": name,
                   "type of court desired": desired_court,
                   "home postcode": postcode,
                   "nearest court of desired type": name_of_closest_court,
                   "dx_number": dx_number,
                   "distance": distance}
        new_row_df = pd.DataFrame([new_row])

        closest_tribunal_df = pd.concat(
            [closest_tribunal_df, new_row_df], ignore_index=True)

    return closest_tribunal_df


if __name__ == "__main__":
    # [TODO]: write your answer here
    # Will show a pd.Dataframe with the answers.
    print(main())
