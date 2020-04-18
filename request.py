import socket
import ssl
import argparse
import re
from yarl import URL


class Request():
    def __init__(self, url=None,
                 reference=None,
                 post=None,
                 verbose=None,
                 file=None,
                 cookie=None,
                 agent=None,
                 output=None,
                 headers={}):
        self._url = URL(url)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._post = post
        self._reference = reference
        self._verbose = verbose
        self._file = file
        self._cookie = cookie
        self._agent = agent
        self._output = output
        self._headers = headers
        self._request_type = "POST" if post or file else "GET"
        if self._url.scheme == 'https':
            self.__sock = ssl.wrap_socket(self.__sock)

    def do_request(self):
        request = self.make_request()
        self.__sock.connect((self._url.host, self._url.port))
        if self._url.scheme == 'https':
            self.__sock.do_handshake()
        self.__sock.sendall(request)
        answer = ''
        while True:
            data = self.__sock.recv(2056)
            if not data:
                break
            answer += data.decode()
        self.__sock.close()
        self.print_answer(answer=answer, request=request)

    def print_answer(self, answer, request):
        if self._verbose:
            print('> ' + request.decode('utf-8') + '\r\n' + '< ' + answer)
        elif self._output:
            f = open(self._output, 'w')
            f.write(answer)
            f.close()
        else:
            print(answer)

    def make_request(self):
        request = bytearray(f'{self._request_type} {self._url.path} HTTP/1.1\r\n'
                            f'Host: {self._url.host}\r\n'
                            f'Connection: close\r\n', 'utf-8')
        if self._reference:
            request += ('Reference: ' + self._reference + '\r\n').encode('utf-8')
        if self._cookie:
            request += ('Cookie: ' + self._cookie + '\r\n').encode('utf-8')
        if self._headers:
            for head in self._headers.keys():
                request += (head + ': ' + self._headers[head] + '\r\n').encode('utf-8')
        if self._agent:
            request += ('User-Agent: ' + self._agent + '\r\n').encode('utf-8')
        if self._post:
            data = self._post
            request += ('Content-Length: ' + str(len(data) + 5) + '\r\n\r\n' + 'body=' + data + '\r\n').encode('utf-8')
        if self._file:
            f = open(self._file, 'r')
            data = f.read()
            request += ('Content-Length: ' + str(len(data) + 7) + '\r\n\r\n' + 'body=' + data + '\r\n').encode('utf-8')
        request += '\r\n'.encode('utf-8')
        return request
