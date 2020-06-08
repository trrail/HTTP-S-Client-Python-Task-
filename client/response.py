import re


class Response():
    def __init__(self, message, charset, code, location, protocol, headers):
        self._charset = charset
        self._code = int(code)
        self._message = message
        self._location = location
        self._headers = headers
        self._protocol = float(protocol)

    @classmethod
    def prepare_headers(cls, data):
        response = data.decode('ISO-8859-1')
        code = (re.search(r' [\d]* ', response)).group(0)
        protocol = (re.search(r'[\d\.\d]* ', response)).group(0)
        message = response.split('\r\n\r\n')[1]
        charset = ''
        headers = {}
        location = ''
        for i in response.split('\r\n\r\n')[0].split('\r\n'):
            s = re.search(r'(?P<header>[a-zA-Z-]*): (?P<value>[0-9\s\w,.;=/:-]*)', i)
            if s is not None:
                headers[s.group('header')] = s.group('value')
                if s.group('header') == 'Content-Type' or s.group('header') == 'content-type':
                    f = re.search(r'[a-zA-z/]*; charset=(?P<charset>[\w\d-]*)', s.group('value'))
                    if f is not None:
                        charset = f.group('charset')
                    else:
                        charset = 'utf-8'
                if s.group('header') == 'Location' or s.group('header') == 'location':
                    location = s.group('value')
        return cls(message, charset, code, location, protocol, headers)

    @property
    def message(self):
        return self._message

    @property
    def protocol(self):
        return self._protocol

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
