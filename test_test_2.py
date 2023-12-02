"""Test's for test_2 file."""
# pylint: disable=C0116, W0611, W0621
import requests_mock
import requests
from test_2 import get_tribunal_info_from_postcode, find_wanted_court_type
from test_2 import get_min_dis_of_potential_courts, find_dx_number_of_closest_court
from test_2 import BASE_POSTCODE_REQUEST


def test_get_tribunal_info_from_postcode(requests_mock):

    output = {"name": "example_court",
              "lat": "random", "lon": "random2"}

    requests_mock.get(
        f'{BASE_POSTCODE_REQUEST}CW81RD', status_code=200, json=output)

    person = {"name": "example_name", "home_postcode": "CW81RD"}
    response = get_tribunal_info_from_postcode(person)

    print(response)
    name = response["name"]

    assert name == "example_court"


def test_get_tribunal_info_from_postcode_2(requests_mock):

    output = {"name": "example_court",
              "lat": "random", "lon": "random2"}

    requests_mock.get(
        f'{BASE_POSTCODE_REQUEST}CW81RD', status_code=200, json=output)

    person = {"name": "example_name", "home_postcode": "CW81RD"}
    get_tribunal_info_from_postcode(person)

    assert requests_mock.called
    assert requests_mock.call_count == 1
    assert requests_mock.last_request.method == "GET"


def test_get_tribunal_info_from_postcode_too_many_numbers():
    person = {"name": "example_name", "home_postcode": "C8541RD"}

    assert get_tribunal_info_from_postcode(
        person) == {'message': 'Invalid postcode: C8541RD'}


def test_get_tribunal_info_from_postcode_too_short():
    person = {"name": "example_name", "home_postcode": "C8"}

    assert get_tribunal_info_from_postcode(
        person) == {'message': 'Invalid postcode: C8'}


def test_get_tribunal_info_from_postcode_too_long():
    person = {"name": "example_name", "home_postcode": "CW81RRD"}

    assert get_tribunal_info_from_postcode(
        person) == {'message': 'Invalid postcode: CW81RRD'}


def test_find_wanted_court_type_no_courts_found():

    person = {"name": "example_name", "home_postcode": "CW81RRD",
              "looking_for_court_type": "example"}

    courts = [{"types": "not_real"}, {"types": "Magistrates' Court"}]

    assert find_wanted_court_type(
        person, courts) == 'Error. No courts found with that type.'


def test_find_wanted_court_type_successful():

    person = {"name": "example_name", "home_postcode": "CW81RRD",
              "looking_for_court_type": "example"}

    courts = [{"types": ["example"]}, {"types": ["Magistrates' Court"]}]

    assert find_wanted_court_type(
        person, courts) == [{"types": ["example"]}]


def test_find_wanted_court_type_successful_multiple_found():

    person = {"name": "example_name", "home_postcode": "CW81RRD",
              "looking_for_court_type": "example"}

    courts = [{"types": ["example"]}, {
        "types": ["Magistrates' Court"]}, {"types": ["example"]}, {"types": ["example"]}]

    assert find_wanted_court_type(
        person, courts) == [{"types": ["example"]}, {"types": ["example"]}, {"types": ["example"]}]


def test_get_min_dis_of_potential_courts_successful():

    potential_courts = [{"name": "example", "distance": 2.5},
                        {"name": "wrong", "distance": 4.5}]
    assert get_min_dis_of_potential_courts(potential_courts) == {
        "name": "example", "distance": 2.5}


def test_find_dx_number_of_closest_court_present():
    assert find_dx_number_of_closest_court(
        {"name": "example", "distance": 2.5, "dx_number": "3edffc"}) == "3edffc"


def test_find_dx_number_of_closest_court_no_key():
    assert find_dx_number_of_closest_court(
        {"name": "example", "distance": 2.5}) == "No dx_number key found."


def test_find_dx_number_of_closest_court_value_empty():
    assert find_dx_number_of_closest_court(
        {"name": "example", "distance": 2.5, "dx_number": ""}) == "dx_number blank."
