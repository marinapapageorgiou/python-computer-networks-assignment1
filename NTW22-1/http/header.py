HEADER_HOST = 'Host'
HEADER_CONNECTION = 'Connection'
HEADER_CONNECTION_CLOSE = 'close'
HEADER_CONTENT_LENGTH = 'Content-Length'
HEADER_CONTENT_LOCATION = 'Content-Location'
HEADER_CONTENT_TYPE = 'Content-Type'
HEADER_CONTENT_TYPE_TEXT_PLAIN = 'text/plain'
HEADER_DATE = 'Date'
HEADER_SERVER = 'Server'


class HttpHeader:
    """
    Defines a new HTTP header, with the given name and value.
    """
    name = None
    value = None

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __eq__(self, other):
        """
        Checks if two HttpHeader items are equal. It is considered equal if the name are the same.
        :return: True if both HttpHeader name are the same
        """
        if not isinstance(other, HttpHeader):
            return False
        return self.name == other.name

    def __hash__(self):
        """
        Specifies to use only the name as the hashing key for HttpHeader.
        :return: hash(name)
        """
        return hash(self.name)

    def __str__(self) -> str:
        """
        Formats the HTTP header based on the RFC format.
        :return: "Name: Value"
        """
        return "{}: {}".format(self.name, self.value)
