import pytest
from assertpy import assert_that

from api.courier_api import CourierAPI


@pytest.mark.usefixtures("courier_api")
class TestCourier:

    def test_create_courier_success(self, courier_data):
        courier = self.courier_api.create_courier(
            payload=courier_data,
            response_code_expected=self.courier_api.CODE__CREATE_SUCCESS
        )

        description = "Тело ответа не соответствует ожидаемому"
        assert_that(courier, description=description).is_equal_to(self.courier_api.BODY__CREATE_SUCCESS)

    def test_create_two_same_couriers_fail(self, courier_data):
        self.courier_api.create_courier(
            payload=courier_data,
            response_code_expected=self.courier_api.CODE__CREATE_SUCCESS
        )
        courier = self.courier_api.create_courier(
            payload=courier_data,
            response_code_expected=self.courier_api.CODE__CREATE_SAME_LOGIN
        )

        description = "Тело ответа не соответствует ожидаемому"
        assert_that(courier, description=description).is_equal_to(self.courier_api.BODY__CREATE_SAME_LOGIN)

    @pytest.mark.parametrize("missing_parameter", ["login", "password"])
    def test_create_courier_with_missing_required_parameter_fail(self, courier_data, missing_parameter):
        del courier_data[missing_parameter]

        courier = self.courier_api.create_courier(
            payload=courier_data,
            response_code_expected=self.courier_api.CODE__CREATE_MISSING_PARAMETER
        )

        description = "Тело ответа не соответствует ожидаемому"
        assert_that(courier, description=description).is_equal_to(self.courier_api.BODY__CREATE_MISSING_PARAMETER)

    def test_login_courier_success(self, courier_data):
        self.courier_api.create_courier(
            payload=courier_data,
            response_code_expected=self.courier_api.CODE__CREATE_SUCCESS
        )
        del courier_data["firstName"]

        login = self.courier_api.login_courier(
            payload=courier_data,
            response_code_expected=self.courier_api.CODE__LOGIN_SUCCESS
        )

        description = 'Тело ответа не содержит ключ "id"'
        assert_that(login, description=description).contains_key("id")
        description = 'Ключ "id" неверного типа'
        assert_that(login["id"], description=description).is_positive()

    @pytest.mark.parametrize("invalid_parameter", ["login", "password"])
    def test_login_with_invalid_data_fail(self, courier_data, invalid_parameter):
        self.courier_api.create_courier(
            payload=courier_data,
            response_code_expected=self.courier_api.CODE__CREATE_SUCCESS
        )
        courier_data[invalid_parameter] = "_"

        login = self.courier_api.login_courier(
            payload=courier_data,
            response_code_expected=self.courier_api.CODE__LOGIN_INCORRECT_DATA
        )
        description = "Тело ответа не соответствует ожидаемому"
        assert_that(login, description=description).is_equal_to(self.courier_api.BODY__LOGIN_INCORRECT_DATA)
