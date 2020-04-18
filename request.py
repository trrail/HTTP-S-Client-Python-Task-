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
        self.__host = self._url.host
        self.__protocol = self._url.scheme
        self._post = post
        self.__port = self._url.port
        self._reference = reference
        self._verbose = verbose
        self._file = file
        self._cookie = cookie
        self._agent = agent
        self._output = output
        self._headers = headers
        self.request = ''
        self.answer = ''
        self._request_type = "POST" if post or file else "GET"
        if self.__protocol == 'https':
            self.__sock = ssl.wrap_socket(self.__sock)

    def do_request(self):
        self.__sock.connect((self.__host, self.__port))
        if self.__protocol == 'https':
            self.__sock.do_handshake()
        self.__sock.sendall(self.request.encode('utf-8'))
        while True:
            data = self.__sock.recv(2056)
            if not data:
                break
            self.answer += data.decode()
        self.__sock.close()

    def print_answer(self):
        if self._verbose:
            print('> ' + self.request + '\r\n' + '< ' + self.answer)
        elif self._output:
            f = open(self._output, 'w')
            f.write(self.answer)
            f.close()
        else:
            print(self.answer)

    def make_request(self):
        if self._request_type == "GET":
            self.request = 'GET ' + str(self._url.path) + ' HTTP/1.1\r\n' \
                                                          'Host: ' + self.__host + '\r\n' \
                                                                                   'Connection: close\r\n'
        else:
            self.request = 'POST ' + str(self._url.path) + ' HTTP/1.1\r\n' \
                                                          'Host: ' + self.__host + '\r\n' \
                                                                                   'Connection: close\r\n'
        if self._reference:
            self.request += 'Reference: ' + self._reference + '\r\n'
        if self._cookie:
            self.request += 'Cookie: ' + self._cookie + '\r\n'
        if self._headers:
            for head in self._headers.keys():
                self.request += head + ': ' + self._headers[head] + '\r\n'
        if self._agent:
            self.request += 'User-Agent: ' + self._agent + '\r\n'
        if self._post:
            data = self._post
            self.request += 'Content-Length: ' \
                            + str(len(data) + 5) + '\r\n' \
                                    '\r\n' \
                                            'body=' + data + '\r\n'
        if self._file:
            f = open(self._file, 'r')
            data = f.read()
            self.request += 'Content-Length: ' + str(len(data) + 7) + '\r\n' \
                                            '\r\n' \
                                                    'body=' + data + '\r\n'
        self.request += '\r\n'
        return self.request
