import allure
import pytest
from assertpy import assert_that


@pytest.mark.usefixtures("courier_api", "order_api")
class TestOrder:

    @allure.title("Создать заказ с различными вариантами указания цвета")
    @pytest.mark.parametrize(
        "color",
        [
            pytest.param(["BLACK", "GREY"], id="black-grey"),
            pytest.param(["BLACK"], id="black"),
            pytest.param(["GREY"], id="grey"),
            pytest.param([], id="no-color"),
        ]
    )
    def test_create_order_success(self, order_data, color):
        order_data["color"] = color

        order = self.order_api.create_order(
            payload=order_data, response_code_expected=self.order_api.CODE__CREATE_SUCCESS)

        description = 'Тело ответа не содержит ключ "track"'
        assert_that(order, description=description).contains_key("track")
        description = 'Ключ "track" неверного типа'
        assert_that(order["track"], description=description).is_positive()

    @allure.title("Получить список заказов")
    def test_get_order_list_success(self, courier_logged_in, order):
        self.order_api.accept_order(
            order_track=order["track"],
            params={"courierId": courier_logged_in["id"]},
            response_code_expected=self.order_api.CODE__ACCEPT_SUCCESS
        )

        orders = self.order_api.get_orders(
            params={"courierId": courier_logged_in["id"]},
            response_code_expected=self.order_api.CODE__GET_SUCCESS
        )
        description = "Тело ответа не содержит списка заказов"
        assert_that(orders["orders"], description=description).is_instance_of(list)
