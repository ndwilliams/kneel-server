import json
from nss_handler import status
from models import Style


class StylesView():
    def get(self, handler, url):
        """Method for handling GET requests for /metals

        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource

        Returns:
            None
            """
        style_model = Style()

        if url["pk"] != 0:
            serialized_style = json.dumps(style_model.get_single(url["pk"]))
            return handler.response(serialized_style, status.HTTP_200_SUCCESS.value)

        serialized_styles = json.dumps(style_model.get_all())
        handler.response(serialized_styles, status.HTTP_200_SUCCESS.value)

    def post(self, handler, style_data):
        style_model = Style()

        number_of_rows_created = style_model.db_create(style_data)
        if number_of_rows_created > 0:
            return handler.response("", status.HTTP_201_CREATED.value)
        else:
            return handler.response("", status.HTTP_400_BAD_REQUEST.value)
