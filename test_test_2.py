"""Test's for test_2 file."""
import requests_mock
import requests
from test_2 import get_tribunal_info_from_postcode, find_wanted_court_type
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


def test_find_wanted_court_type_successful():
    pass


def test_find_wanted_court_type_no_courts_found():
    pass
