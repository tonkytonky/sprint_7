import random
import string
from datetime import datetime, timedelta

import pytest
from faker import Faker

from api import CourierAPI
from api import OrderAPI


@pytest.fixture(scope="class")
def courier_api(request):
    request.cls.courier_api = CourierAPI()


@pytest.fixture(scope="class")
def order_api(request):
    request.cls.order_api = OrderAPI()


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


@pytest.fixture(scope="function")
def courier(request, courier_data):
    request.cls.courier_api.create_courier(
        payload=courier_data,
        response_code_expected=request.cls.courier_api.CODE__CREATE_SUCCESS
    )
    return courier_data


@pytest.fixture(scope="function")
def courier_logged_in(request, courier):
    del courier["firstName"]

    login = request.cls.courier_api.login_courier(
        payload=courier,
        response_code_expected=request.cls.courier_api.CODE__LOGIN_SUCCESS
    )
    return login


@pytest.fixture(scope="function")
def order_data():
    faker = Faker("ru_RU")

    first_name = faker.first_name()
    last_name = faker.last_name()
    street_address = faker.street_address().replace("/", "")
    metro_station = str(random.choice(range(1, 101)))
    phone_number = faker.phone_number()
    for forbidden_char in (" ", "-", "(", ")"):
        phone_number = phone_number.replace(forbidden_char, "")
    rent_time = random.choice(range(1, 8))
    delivery_date = faker.date_between(datetime.now(), timedelta(days=14)).strftime("%Y-%m-%d")
    comment = faker.text(max_nb_chars=80)
    color = [random.choice(("BLACK", "GREY"))]

    return {
        "firstName": first_name,
        "lastName": last_name,
        "address": street_address,
        "metroStation": metro_station,
        "phone": phone_number,
        "rentTime": rent_time,
        "deliveryDate": delivery_date,
        "comment": comment,
        "color": color
    }


@pytest.fixture(scope="function")
def order(request, order_data):
    order = request.cls.order_api.create_order(
        payload=order_data,
        response_code_expected=request.cls.order_api.CODE__CREATE_SUCCESS
    )
    return order
