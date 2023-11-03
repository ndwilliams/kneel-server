import json
from nss_handler import status
from models import Metal


class MetalsView():
    def get(self, handler, url):
        """Method for handling GET requests for /metals

        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource

        Returns:
            None
            """
        metal_model = Metal()

        if url["pk"] != 0:
            serialized_metal = json.dumps(metal_model.get_single(url["pk"]))
            return handler.response(serialized_metal, status.HTTP_200_SUCCESS.value)

        serialized_metal = json.dumps(metal_model.get_all())
        handler.response(serialized_metal, status.HTTP_200_SUCCESS.value)

    def post(self, handler, metal_data):
        metal_model = Metal()

        number_of_rows_created = metal_model.db_create(metal_data)
        if number_of_rows_created > 0:
            return handler.response("", status.HTTP_201_CREATED.value)
        else:
            return handler.response("", status.HTTP_400_BAD_REQUEST.value)
