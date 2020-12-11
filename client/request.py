import socket
import ssl
from client import response as res
from client import errors
from yarl import URL


class Request():
    def __init__(self, url=None,
                 reference=None,
                 cookie=None,
                 agent=None,
                 headers=None,
                 request=None,
                 cookie_file=None,
                 timeout=None,
                 data=''):
        self._url = URL(url)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._reference = reference
        self._protocol = "HTTP/1.1"
        self._cookie = cookie
        self._agent = agent
        self._cookie_from_file = cookie_file
        self._input_headers = headers
        self._headers = {}
        self._timeout = timeout if timeout else '1000'
        self._request_type = request if request else "GET"
        self._request = ''
        self._response = bytearray()
        self._data = data
        try:
            if self._request_type not in ["GET",
                                          "POST",
                                          "PUT",
                                          "DELETE",
                                          "PATCH",
                                          "HEAD",
                                          "OPTIONS",
                                          "CONNECT",
                                          "TRACE"]:
                raise errors.IncorrectRequestType()
        except errors.IncorrectRequestType as e:
            print(e.message)
            exit(1)
        if self._url.scheme == 'https':
            self.__sock = ssl.wrap_socket(self.__sock)

    def do_request(self):
        self.prepare_headers()
        self.make_request()
        try:
            self.__sock.connect((self._url.host, self._url.port))
        except Exception:
            print(errors.ConnectionError.message)
            exit(1)
        self.__sock.settimeout(int(self._timeout))
        if self._url.scheme == 'https':
            self.__sock.do_handshake()
        self.__sock.sendall(self._request.encode())
        while True:
            data = self.__sock.recv(1024)
            if not data:
                break
            self._response.extend(data)
        self.__sock.close()
        response = res.Response.prepare_fields(self._response)
        if not response.location == '':
            request = Request(response.location,
                              self._reference,
                              self._cookie,
                              self._agent,
                              self._headers,
                              self._request_type,
                              self._cookie_from_file,
                              self._timeout)
            return request.do_request()
        else:
            return [self._request, response]

    def prepare_headers(self):
        if self._input_headers:
            for header in self._input_headers:
                separator_ind = header.find(':')
                key = header[0:separator_ind]
                value = header[separator_ind + 1:].strip()
                self._headers[key] = value
        if self._reference:
            self._headers["Reference"] = self._reference
        if self._cookie:
            self._headers["Cookie"] = self._cookie
        if self._cookie_from_file:
            f = open(self._cookie_from_file, 'r')
            self._headers['Cookie'] = f.read()
            f.close()
        if self._agent:
            self._headers["User-Agent"] = self._agent

    def make_request(self):
        request = [f'{self._request_type} {self._url.path} {self._protocol}',
                   f'Host: {self._url.host}',
                   f'Connection: close']
        for header, value in self._headers.items():
            request.append(f'{header}: {value}')
        if len(self._data) != 0:
            request.append(f'Content-Length: {len(self._data)}')
        request.append('')
        request.append(f'{self._data}')
        self._request = '\r\n'.join(request)

    @property
    def request(self):
        return self._request

    @property
    def headers(self):
        return self._headers
