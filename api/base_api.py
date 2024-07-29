import requests
from assertpy import assert_that


class BaseAPI:

    @staticmethod
    def _convert_to_json(courier_response):
        return courier_response.json()

    @staticmethod
    def _check_response_status_code(expected, actual):
        description = "Код ответа не совпадает с ожидаемым"
        assert_that(expected, description=description).is_equal_to(actual)

    def _post(self, url, response_code_expected, json=None):
        if json is None:
            json = {}

        response = requests.post(url=url, json=json)
        self._check_response_status_code(expected=response_code_expected, actual=response.status_code)
        return response

    def _put(self, url, response_code_expected, params=None):
        response = requests.put(url=url, params=params)
        self._check_response_status_code(expected=response_code_expected, actual=response.status_code)
        return response

    def _get(self, url, response_code_expected, params=None):
        response = requests.get(url=url, params=params)
        self._check_response_status_code(expected=response_code_expected, actual=response.status_code)
        return response
