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
        self._request = ''
        try:
            if self._request_type not in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]:
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
        new_response = response.Response()
        data = self.__sock.recv(2048)
        new_response.prepare_headers(data)
        if new_response.content_length - 2048 > 0:
            data = self.__sock.recv(new_response.content_length - 2048)
            new_response.response = data
        self.__sock.close()
        if not new_response.location == '':
            request = Request(new_response.location,
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
            self.show_response(new_response)

    def show_response(self,new_response):
        if self._body_ignore:
            response = [f'{new_response.response[:15]}']
            for header, value in new_response.headers.items():
                response.append(f'{header}: {value}')
            sys.stdout.write('\r\n'.join(response))
        elif self._head_ignore:
            sys.stdout.write(new_response.response.split('\r\n\r\n')[1])
        elif self._verbose:
            sys.stdout.write(f'{self._request} \r\n{new_response.response}')
        else:
            if new_response.response:
                sys.stdout.write(new_response.response)

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
        request = [f'{self._request_type} {self._url.path} {self._protocol}']
        request.append(f'Host: {self._url.host}')
        request.append(f'Connection: close')
        for header, value in self._headers.items():
            request.append(f'{header}: {value}')
        body = self.prepare_data()
        if len(body) != 0:
            request.append(f'Content-Length: {len(body)}')
        request.append('')
        request.append(f'{body}')
        self._request = '\r\n'.join(request)
