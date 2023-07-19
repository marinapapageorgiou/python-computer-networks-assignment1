from __future__ import annotations

from typing import List, Dict

from http.enums import HttpMethod, HttpVersion
from http.header import HttpHeader, HEADER_CONTENT_LENGTH, HEADER_HOST
from http.response import HttpResponseBadRequest, HttpResponseNotImplemented, HttpResponseHttpVersionNotSupported, \
    HttpResponseForbidden, HttpResponseNotFound
from settings import HTTP_ENCODING
from utils.vhosts import Vhost


class HttpRequest:
    """
    HTTP Request class. Contains information regarding the requested method, path, HTTP version, headers
    and body (if present).
    Constructing the class will throw HttpResponseError with further information on why the request is not
    valid.
    """
    # Note this lines variable is only used internally
    __lines = None
    __method, __path, __http_version = None, None, None
    __headers = {}
    __body = None
    __vhost = None

    def __init__(self, raw_bytes: bytes):
        """
        Given an array of bytes, tries to parse the request.
        :param raw_bytes:
        """
        if not raw_bytes:
            raise HttpResponseBadRequest(content="No data found to be parsed")

        raw_data = raw_bytes.decode(HTTP_ENCODING)
        self.__lines = raw_data.split("\r\n")
        if len(self.__lines) == 0:
            raise HttpResponseBadRequest(content="No data found")

        # First we parse the request-line
        self.__init_parse_requestline(self.__lines)

        # NOTE: To generate the HttpRequest object, only the request-line is needed. Once finished
        #       generating the object, we can proceed to parse the rest of the request.
        #       This is done as such so, in case of errors in the headers or when generating the response,
        #       we can appropiately indicate headers and other HTTP data at a later stage.

        # Reset the rest of the fields
        self.__headers = {}
        self.__body = None
        self.__vhost = None

    def __init_parse_requestline(self, lines):
        """
        Given an array of lines, get the first one and parse it with the request-line format
        :param lines: list of lines in the request
        :return: None
        """
        first_line_data = lines[0].split(" ")
        if len(first_line_data) != 3:
            # If we split the first line by the space, and does not have 3 elements, request is malformed
            raise HttpResponseBadRequest(content="Invalid request-line")
        method, path, http_version = first_line_data

        for avail_method in HttpMethod:
            # Method is case sensitive, so no .upper()
            if str(avail_method) == method:
                method = avail_method
                break
        if isinstance(method, str):
            # If we are not able to get the HttpMethod object from it, it is because we do not support
            # the request method
            raise HttpResponseNotImplemented(content="Method {} is not available".format(method))
        self.__method = method

        # Check that path is an absolute URL (proxy-URL is not supported)
        if path[0] != "/":
            raise HttpResponseBadRequest(content="Path must be absolute, starting with /")
        # Confirm that path is secure (does not try to access outside of host's folder scope)
        if not Vhost.is_secure_path(path):
            raise HttpResponseForbidden(content="Trying to access a folder outside the host root")
        # Remove the starting /, and remove the query string as well
        self.__path = path[1:].split("?")[0]

        # Now, try to parse the HTTP version
        http = http_version.split("/")
        if len(http) != 2:
            # It has to have two parts: HTTP SLASH VERSION
            raise HttpResponseBadRequest(content="Could not parse HTTP version")
        version = http[1].split(".")
        if len(version) != 2:
            # Make sure the VERSION part has a major and minor version
            raise HttpResponseBadRequest(content="Invalid HTTP version number")
        try:
            # And check that these values are numbers and not negative
            p1 = int(version[0])
            p2 = int(version[1])
            if p1 < 0 or p2 < 0:
                raise ValueError()
        except ValueError:
            raise HttpResponseBadRequest(content="Could not parse HTTP version number")

        for avail_version in HttpVersion:
            # HTTP version is case-sensitive, so we cannot either apply .upper()
            if str(avail_version) == http_version:
                http_version = avail_version
                break
        if isinstance(http_version, str):
            # If http_version is still a string, we do not support such version
            raise HttpResponseHttpVersionNotSupported(content="HTTP version {} is not available".format(http_version))
        self.__http_version = http_version

    def parse_request(self, hosts: Dict[str, Vhost]):
        """
        Method that finishes parsing the raw request. Can only be invoked once, and must be invoked right after
        constructing the object. It will get the remaining lines to be parsed, and extract both headers and
        request body.
        :param hosts: dictionary of available hosts in the server
        """
        # If lines is None, we have already parsed the request
        if self.__lines is None:
            return

        # Then we parse the header lines (which follow right after the request-line)
        c_headers = self.__init_parse_headers(self.__lines[1:])

        # For HTTP/1.0, if no Host header is present, add it with the first entry (dictionaries in Python 3.6+
        # are ordered)
        if self.__http_version == HttpVersion.HTTP_10 and not self.has_header(HEADER_HOST):
            try:
                default_hostname = next(iter(hosts))
            except StopIteration:
                # If no hosts in the file, then error
                raise HttpResponseNotFound(content='No hosts availables')
            self.__headers[HEADER_HOST.lower()] = HttpHeader(HEADER_HOST, default_hostname)

        # Try to access the host
        host = self.get_header(HEADER_HOST)
        if not host:
            # Host is missing (HTTP/1.1)
            raise HttpResponseBadRequest(content='Mising Host header')
        # Remove port from Host header
        host.value = host.value.split(":")[0]
        if host.value.lower() not in hosts:
            # Host is not available
            raise HttpResponseNotFound(content='Host {} is not found'.format(host.value))
        self.__vhost = hosts[host.value.lower()]

        # And finally, we parse the body (or we make sure that such body is not present)
        self.__init_parse_body(self.__lines[(1 + c_headers + 1):])

        # And indicate that request has been parsed already
        self.__lines = None

    def __init_parse_headers(self, lines):
        """
        Given a list of lines after removing the request-lines, parses lines which are headers.
        :param lines: list of lines to be checked
        :return: number of parsed headers
        """
        count = 0
        found_crlf = False
        for line in lines:
            # If line is "blank", it is because it CRLF, so end of headers
            if line == '':
                found_crlf = True
                break
            # Try to parse header with format ': SPACE'
            header = line.split(": ")
            if len(header) != 2:
                # Malformed header
                raise HttpResponseBadRequest(content="Header '{}' is not a valid header format".format(line))
            self.__headers[header[0].lower()] = HttpHeader(header[0], header[1])
            count += 1

        if not found_crlf:
            # We finished parsing headers, but make sure we found the CRLF regarding the last header
            # (the CRLF that ends the request will be checked in the next function)
            raise HttpResponseBadRequest(content="Could not find CRLF after headers parsing")
        return count

    def __init_parse_body(self, lines):
        """
        Function that given the remaining lines of the request, will check for the body if needed.
        :param lines: "body" part
        :return:
        """
        if not self.has_header(HEADER_CONTENT_LENGTH):
            # If no Content-Length header is present, it means that we can NOT receive any body. Thus, the remaining
            # lines has to be an empty one (the CRLF that ends the request)
            if len(lines) != 1 or lines[0] != '':
                raise HttpResponseBadRequest(content="Expecting no request body, but found")
            return

        # Note that PUT method does not strictly require to have a body, nor GET or DELETE are forbidden to
        # contain such body.
        # https://stackoverflow.com/questions/1233372/is-an-http-put-request-required-to-include-a-body

        # If Content-Length is present, we check if the length of the remaining data matches the specified
        # Content-Length value
        body = "\r\n".join(lines)
        actual_length = len(body)
        try:
            val = self.get_header(HEADER_CONTENT_LENGTH)
            if val is None:
                raise ValueError
            # If the value of the header is not an integer, then it is malformed
            expected_length = int(val.value)
        except ValueError:
            raise HttpResponseBadRequest(content="Could not parse Content-Length")

        if expected_length != actual_length:
            raise HttpResponseBadRequest(content="Request body differs from the specified Content-Length value")
        # And save the body data
        self.__body = body

    def get_method(self) -> HttpMethod:
        return self.__method

    def get_path(self) -> str:
        return self.__path

    def get_http_version(self) -> HttpVersion:
        return self.__http_version

    def get_headers(self) -> List[HttpHeader]:
        return list(self.__headers.values())

    def get_vhost(self) -> Vhost:
        return self.__vhost

    def get_body(self) -> str | None:
        return self.__body

    def has_header(self, name: str):
        return name.lower() in self.__headers

    __contains__ = has_header

    def get_header(self, name: str) -> HttpHeader | None:
        if not self.has_header(name):
            return None
        return self.__headers[name.lower()]

    __getitem__ = get_header
