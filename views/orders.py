import json
from nss_handler import status
from models import Order


class OrdersView():
    def get(self, handler, url):
        """Method for handling GET requests for /metals

        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource

        Returns:
            None
            """
        order_model = Order()

        if url["pk"] != 0:
            serialized_order = json.dumps(order_model.get_single(url["pk"]))
            return handler.response(serialized_order, status.HTTP_200_SUCCESS.value)

        serialized_orders = json.dumps(order_model.get_all())
        handler.response(serialized_orders, status.HTTP_200_SUCCESS.value)

    def post(self, handler, order_data):
        order_model = Order()

        number_of_rows_created = order_model.db_create(order_data)
        if number_of_rows_created > 0:
            return handler.response("", status.HTTP_201_CREATED.value)
        else:
            return handler.response("", status.HTTP_400_BAD_REQUEST.value)

    def update(self, handler, order_data, url):
        order_model = Order()

        number_of_rows_updated = order_model.db_update(order_data, url)
        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_NOT_FOUND.value)
