import socket
import ssl
import argparse
import re
from yarl import URL


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
                 request=None):
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
        self._input_headers = headers
        self._headers = {}
        self._request_type = request if request else "GET"
        if self._url.scheme == 'https':
            self.__sock = ssl.wrap_socket(self.__sock)

    def do_request(self):
        self.prepare_headers()
        request = self.make_request()
        self.__sock.connect((self._url.host, self._url.port))
        if self._url.scheme == 'https':
            self.__sock.do_handshake()
        self.__sock.sendall(request.encode())
        answer = ''
        while True:
            data = self.__sock.recv(1024)
            if not data:
                break
            answer += data.decode("ISO-8859-1")
        self.__sock.close()
        self.print_answer(answer=answer, request=request)

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
        if self._agent:
            self._headers["User-Agent"] = self._agent

    def print_answer(self, answer, request):
        if self._verbose:
            print('> ' + request + '\r\n' + '< ' + answer)
        elif self._output:
            f = open(self._output, 'w')
            f.write(str(answer.encode("ISO-8859-1")))
            f.close()
        else:
            print(answer)

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
        request = ''.join((request, '\r\n\r\n', body, '\r\n'))
        return request
