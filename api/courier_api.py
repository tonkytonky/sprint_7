from http import HTTPStatus

from api import BaseAPI
from config import BASE_URL


class CourierAPI(BaseAPI):
    CODE__CREATE_SUCCESS = HTTPStatus.CREATED
    CODE__CREATE_SAME_LOGIN = HTTPStatus.CONFLICT
    CODE__CREATE_MISSING_PARAMETER = HTTPStatus.BAD_REQUEST
    CODE__LOGIN_SUCCESS = HTTPStatus.OK
    CODE__LOGIN_INCORRECT_DATA = HTTPStatus.NOT_FOUND
    CODE__LOGIN_MISSING_PARAMETER = HTTPStatus.BAD_REQUEST
    BODY__CREATE_SUCCESS = {"ok": True}
    BODY__CREATE_SAME_LOGIN = {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
    BODY__CREATE_MISSING_PARAMETER = {"code": 400, "message": "Недостаточно данных для создания учетной записи"}
    BODY__LOGIN_INCORRECT_DATA = {"code": 404, "message": "Учетная запись не найдена"}
    BODY__LOGIN_MISSING_PARAMETER = {"code": 400, "message": "Недостаточно данных для входа"}

    def create_courier(self, payload, response_code_expected):
        response = self._post(
            url=f"{BASE_URL}/api/v1/courier", json=payload,
            response_code_expected=response_code_expected
        )
        return self._convert_to_json(response)

    def login_courier(self, payload, response_code_expected):
        response = self._post(
            url=f"{BASE_URL}/api/v1/courier/login", json=payload,
            response_code_expected=response_code_expected
        )
        return self._convert_to_json(response)
