import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import MetalsView, SizesView, StylesView, OrdersView


class JSONServer(HandleRequests):

    def do_GET(self):
        url = self.parse_url(self.path)
        view = self.determine_view(url)
        view.get(self, url)

    def do_POST(self):
        # Parse the URL
        url = self.parse_url(self.path)
        # Determine the correct view needed to handle the requests
        view = self.determine_view(url)
        # Get the request body
        try:
            # Invoke the correct method on the view
            view.post(self, self.get_request_body())
        # Make sure you handle the AttributeError in case the client requested a route that you don't support
        except AttributeError:
            pass

    def do_PUT(self):
        self.response("Unsupported method", status.HTTP_405_UNSUPPORTED)

    def do_DELETE(self):
        self.response("Unsupported method", status.HTTP_405_UNSUPPORTED)

    def determine_view(self, url):
        """Lookup the correct view class to handle the requested route

        Args:
            url (dict): The URL dictionary

        Returns:
            Any: An instance of the matching view class
        """
        try:
            routes = {
                "metals": MetalsView,
                "sizes": SizesView,
                "styles": StylesView,
                "orders": OrdersView
            }

            matching_class = routes[url["requested_resource"]]
            return matching_class()
        except KeyError:
            self.response("No view for that route", status.HTTP_404_NOT_FOUND)


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
