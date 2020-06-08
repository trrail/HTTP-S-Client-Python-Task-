import re
from client import errors as er


class Response():
    def __init__(self, response=None):
        self._response = response
        self._charset = "utf-8"
        self._code = ''
        self._message = ''
        self._location = ''
        self._headers = {}
        self.prepare_headers(response)

    def prepare_headers(self, data):
        response = data.decode('ISO-8859-1')
        self._code = (re.search(r' [\d]* ', response)).group(0)
        self._message = response.split('\r\n\r\n')[1]
        for i in response.split('\r\n'):
            s = re.search(r'(?P<header>[a-zA-Z-]*): (?P<value>[0-9\s\w,.;=/:-]*)', i)
            if s is not None:
                self._headers[s.group('header')] = s.group('value')
                if s.group('header') == 'Content-Type' or s.group('header') == 'content-type':
                    f = re.search(r'[a-zA-z/]*; charset=(?P<charset>[\w\d-]*)', s.group('value'))
                    if f is not None:
                        self._charset = f.group('charset')
                if s.group('header') == 'Location' or s.group('header') == 'location':
                    self._location = s.group('value')

    @property
    def response(self):
        return self._response

    @property
    def message(self):
        return self._message

    @property
    def headers(self):
        return self._headers

    @property
    def code(self):
        return self._code

    @property
    def charset(self):
        return self._charset

    @property
    def location(self):
        return self._location
