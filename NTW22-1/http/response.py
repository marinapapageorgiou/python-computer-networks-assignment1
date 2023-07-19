from __future__ import annotations

from http.enums import HttpResponseCode
from http.header import HttpHeader
from settings import HTTP_ENCODING


class HttpResponse:
    """
    Base class for a HTTP response object. Contains the response code (status), the headers and the content
    (if any).
    This class can be treated as a dictionary, where the keys are header names and the values are HttpHeader
    objects.
    """
    __status = None
    __headers = {}
    __content = None

    def __init__(self,
                 status: HttpResponseCode = HttpResponseCode.OK,
                 content: str | bytes | None = None):
        # Saves the basic data (inmutable) to the class attributes
        self.__status = status
        self.__content = content
        self.__headers = {}

    def get_status_code(self):
        # Returns the status code
        return self.__status

    def has_header(self, name: str):
        # Check if a given header is present
        return name.lower() in self.__headers

    # Treats the "in" keyword as has_header function with objects of HttpResponse
    __contains__ = has_header

    def add_header(self, key: str, header: HttpHeader):
        # Saves the specified header into the dictionary of headers
        self.__headers[key.lower()] = header

    # Treats the HttpResponse[HEADER] = VALUE as add_header function with objects of HttpResponse
    __setitem__ = add_header

    def get_header(self, name: str) -> HttpHeader | None:
        # If no header found, return None
        if not self.has_header(name):
            return None
        # Else return the HttpHeader object
        return self.__headers[name.lower()]

    # Treats the HttpResponse[HEADER] as get_header function with objects of HttpResponse
    __getitem__ = get_header

    def del_header(self, name: str):
        # Do nothing if the header is not present
        if not self.has_header(name):
            return
        # Else delete the header
        self.__headers.pop(name.lower())

    # Treats the "del" keyword as has_header function with objects of HttpResponse
    __delitem__ = del_header

    def get_content(self) -> str | bytes | None:
        return self.__content

    def serialize_headers(self):
        if len(self.__headers) == 0:
            # If no headers are present, just return an empty string
            return ''
        # Else, concatenate all of them with the HTTP format and append \r\n to the last one (join only adds it
        # in between)
        return '\r\n'.join("{}: {}".format(h.name, h.value) for h in self.__headers.values()) + '\r\n'

    def serialize(self):
        # Convert to string headers with content (if present)
        return self.serialize_headers() + '\r\n' + (str(self.__content) if self.__content is not None else '')

    def __bytes__(self):
        out = (self.serialize_headers() + '\r\n').encode(HTTP_ENCODING)
        if self.__content is not None:
            content = self.__content
            if isinstance(self.__content, str):
                content = content.encode(HTTP_ENCODING)
            out += content
        return out


class HttpResponseError(HttpResponse, RuntimeError):
    """
    Specific subclass of HttpResponse which indicates an error has been catched. It extends RuntimeError,
    so it can be thrown (specifically during the HttpRequest object construction while parsing the
    request).
    Then other sub-classes are defined for other response codes.
    """
    def __init__(self, *args, **kwargs):
        # If no status is given, use 500 by default
        if 'status' not in kwargs:
            kwargs['status'] = HttpResponseCode.INTERNAL_SERVER_ERROR
        # If no content is given, get the reason explanation for the code
        if 'content' not in kwargs:
            kwargs['content'] = kwargs['status'].get_reason()
        super(HttpResponseError, self).__init__(*args, **kwargs)


# 400
class HttpResponseBadRequest(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseBadRequest, self).__init__(status=HttpResponseCode.BAD_REQUEST,
                                                     *args, **kwargs)


# 403
class HttpResponseForbidden(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseForbidden, self).__init__(status=HttpResponseCode.FORBIDDEN,
                                                    *args, **kwargs)


# 404
class HttpResponseNotFound(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseNotFound, self).__init__(status=HttpResponseCode.NOT_FOUND,
                                                   *args, **kwargs)


# 405
class HttpResponseMethodNotAllowed(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseMethodNotAllowed, self).__init__(status=HttpResponseCode.METHOD_NOT_ALLOWED,
                                                           *args, **kwargs)


# 415
class HttpResponseUnsupportedMediaType(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseUnsupportedMediaType, self).__init__(status=HttpResponseCode.UNSUPPORTED_MEDIA_TYPE,
                                                               *args, **kwargs)


# 501
class HttpResponseNotImplemented(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseNotImplemented, self).__init__(status=HttpResponseCode.NOT_IMPLEMENTED,
                                                         *args, **kwargs)


# 505
class HttpResponseHttpVersionNotSupported(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseHttpVersionNotSupported, self).__init__(status=HttpResponseCode.HTTP_VERSION_NOT_SUPPORTED,
                                                                  *args, **kwargs)
