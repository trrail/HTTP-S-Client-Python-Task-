import re
from client import errors as er


class Response():
    def __init__(self):
        self._response = bytearray()
        self._charset = "utf-8"
        self._code = ''
        self._location = ''
        self._headers = {}
        self._content_length = 0
        self._chunk = 0

    def prepare_headers(self, data):
        self._response.extend(data)
        response = data.decode("ISO-8859-1")
        self._code = (re.search(r' [\d]* ', response)).group(0)
        for i in response.split('\r\n'):
            s = re.search(r'(?P<header>[a-zA-Z-]*): (?P<value>[0-9\s\w,.;=/:-]*)', i)
            if s is not None:
                self._headers[s.group('header')] = s.group('value')
                if s.group('header') == 'Content-Length' or s.group('header') == 'content-length':
                    self._content_length = int(s.group('value'))
                if s.group('header') == 'Content-Type' or s.group('header') == 'content-type':
                    f = re.search(r'[a-zA-z/]*; charset=(?P<charset>[\w\d-]*)', s.group('value'))
                    if f is not None:
                        self._charset = f.group('charset')
                if s.group('header') == 'Location' or s.group('header') == 'location':
                    self._location = s.group('value')
                if s.group('header') == 'Transfer-Encoding' or s.group('header') == 'transfer-encoding':
                    self._chunk = 1
        if self._chunk == 1:
            s = re.search(r'\r\n\r\n(?P<chunk>[\w\d]*)\r\n', response)
            self._chunk = int(s.group('chunk'), 16)

    response = property()
    location = property()
    headers = property()

    @headers.getter
    def headers(self):
        return self._headers

    @location.getter
    def location(self):
        return self._location

    @response.getter
    def response(self):
        try:
            return self._response.decode(self._charset)
        except UnicodeDecodeError:
            print(er.ConnectionError.message)

    @response.setter
    def response(self, value):
        self._response.extend(value)

    @property
    def content_length(self):
        return self._content_length

    @property
    def chunk(self):
        return self._chunk
