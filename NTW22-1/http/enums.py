from enum import Enum

# This file defines several enums that are used by the HTTP server in order to build a cleaner implementation of
# the HTTP protocol.


class HttpVersion(Enum):
    """
    Currently supported HTTP versions in the server.
    """
    HTTP_10 = "HTTP/1.0"
    HTTP_11 = "HTTP/1.1"

    def __str__(self):
        """
        Returns a valid HTTP version based on the RFC.
        :return: "HTTP/X.X"
        """
        return self.value


class HttpMethod(Enum):
    """
    HTTP methods supported by the server.
    """
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    NTW22INFO = "NTW22INFO"

    def __str__(self):
        """
        Returns a string based on the Enum value.
        :return: "METHOD"
        """
        return self.value


class HttpResponseCode(Enum):
    """
    HTTP response codes used by the server.
    """
    OK = 200, "OK"
    CREATED = 201, "Created"

    BAD_REQUEST = 400, "Bad Request"
    FORBIDDEN = 403, "Forbidden"
    NOT_FOUND = 404, "Not Found"
    METHOD_NOT_ALLOWED = 405, "Method Not Allowed"
    UNSUPPORTED_MEDIA_TYPE = 415, "Unsupported Media Type"

    INTERNAL_SERVER_ERROR = 500, "Internal Server Error"
    NOT_IMPLEMENTED = 501, "Not Implemented"
    HTTP_VERSION_NOT_SUPPORTED = 505, "HTTP Version Not Supported"

    def get_code(self) -> int:
        return self.value[0]

    def get_reason(self) -> str:
        return self.value[1]

    def __str__(self) -> str:
        """
        Given the Enum value, generates a valid HTTP output string based on the RFC.
        :return: "CODE Reason-Phrase"
        """
        return "{} {}".format(self.value[0], self.value[1])
