from http import HTTPStatus

from assertpy import assert_that

from api import BaseAPI
from config import BASE_URL


class OrderAPI(BaseAPI):
    CODE__CREATE_SUCCESS = HTTPStatus.CREATED
    CODE__ACCEPT_SUCCESS = HTTPStatus.OK
    CODE__GET_SUCCESS = HTTPStatus.OK

    def create_order(self, payload, response_code_expected):
        response = self._post(
            url=f"{BASE_URL}/api/v1/orders", json=payload,
            response_code_expected=response_code_expected
        )
        return self._convert_to_json(response)

    def accept_order(self, order_track, params, response_code_expected):
        response = self._put(
            url=f'{BASE_URL}/api/v1/orders/accept/{order_track}',
            params=params,
            response_code_expected=response_code_expected
        )
        return self._convert_to_json(response)

    def get_orders(self, params, response_code_expected):
        response = self._get(
            url=f'{BASE_URL}/api/v1/orders',
            params=params,
            response_code_expected=response_code_expected
        )
        return self._convert_to_json(response)
