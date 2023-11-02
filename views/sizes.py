import json
from nss_handler import status
from models import Size


class SizesView():
    def get(self, handler, url):
        """Method for handling GET requests for /metals

        Args:
            handler (object): HTTP request handle to send response
            pk (int): Primary key of request resource

        Returns:
            None
            """
        metal_model = Size()

        if url["pk"] != 0:
            serialized_metal = json.dumps(metal_model.get_single(url["pk"]))
            return handler.response(serialized_metal, status.HTTP_200_SUCCESS)

        serialized_metal = json.dumps(metal_model.get_all())
        handler.response(serialized_metal, status.HTTP_200_SUCCESS)