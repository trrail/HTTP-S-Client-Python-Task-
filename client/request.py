import socket
import ssl
from client import response
from client import errors
from yarl import URL
import sys


class Request():
    def __init__(self, url=None,
                 reference=None,
                 data=None,
                 verbose=None,
                 file=None,
                 cookie=None,
                 agent=None,
                 output=None,
                 headers=None,
                 request=None,
                 cookie_file=None,
                 body_ignore=None,
                 head_ignore=None,
                 timeout=None):
        self._url = URL(url)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._data = data
        self._reference = reference
        self._verbose = verbose
        self._file = file
        self._protocol = "HTTP/1.1"
        self._cookie = cookie
        self._agent = agent
        self._output = output
        self._cookie_from_file = cookie_file
        self._input_headers = headers
        self._headers = {}
        self._body_ignore = body_ignore
        self._head_ignore = head_ignore
        self._timeout = timeout if timeout else '1000'
        self._request_type = request if request else "GET"
        try:
            if self._request_type not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]:
                raise errors.IncorrectRequestType()
        except errors.IncorrectRequestType as e:
            print(e.message)
            exit()
        if self._url.scheme == 'https':
            self.__sock = ssl.wrap_socket(self.__sock)

    def do_request(self):
        self.prepare_headers()
        request = self.make_request()
        try:
            self.__sock.connect((self._url.host, self._url.port))
        except BaseException:
            print(errors.ConnectionError.message)
        else:
            self.__sock.settimeout(int(self._timeout))
            if self._url.scheme == 'https':
                self.__sock.do_handshake()
            self.__sock.sendall(request.encode())
            new_response = response.Response()
            while True:
                data = self.__sock.recv(2048)
                if not data:
                    break
                new_response.read_response(data)
            self.__sock.close()
            re = new_response.return_response()
            if not re[4] == '':
                request = Request(re[4],
                                  self._reference,
                                  self._data,
                                  self._verbose,
                                  self._file,
                                  self._cookie,
                                  self._agent,
                                  self._output,
                                  self._headers,
                                  self._request_type,
                                  self._cookie_from_file,
                                  self._body_ignore,
                                  self._head_ignore,
                                  self._timeout)
                request.do_request()
            else:
                self.show_response(request, re)

    def show_response(self, request, prepared_response):
        if self._verbose:
            sys.stdout.write(request + '\r\n')
            sys.stdout.buffer.write(prepared_response[3])
        elif self._body_ignore:
            sys.stdout.write(prepared_response[1])
        elif self._head_ignore:
            sys.stdout.write(prepared_response[2])
        else:
            sys.stdout.write(prepared_response[0])

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

    def prepare_data(self):
        data = ''
        if self._data:
            data = self._data
        if self._file:
            f = open(self._file, 'r')
            data = f.read()
            f.close()
        return data

    def make_request(self):
        request = f'{self._request_type} {self._url.path} {self._protocol}\r\n' \
                    f'Host: {self._url.host}\r\n' \
                    f'Connection: close\r\n'
        for header, value in self._headers.items():
            request = ''.join((request, header, ': ', value, '\r\n'))
        body = self.prepare_data()
        if len(body) != 0:
            request = ''.join((request, 'Content-Length: ', str(len(body)), '\r\n\r\n', body, '\r\n'))
        else:
            request = ''.join((request, '\r\n'))
        return request
