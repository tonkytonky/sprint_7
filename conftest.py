import random
import string

import pytest

from api.courier_api import CourierAPI


@pytest.fixture(scope="class")
def courier_api(request):
    request.cls.courier_api = CourierAPI()


@pytest.fixture(scope="function")
def courier_data():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    courier_data = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    return courier_data
