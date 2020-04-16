import socket
import ssl
import argparse
import re


class Request():
    def __init__(self, args):
        self.args = args
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = (re.findall(r'//[\w\.]+/', args.http))[0][2:][:-1]
        self.__protocol = re.findall(r'https*:', args.http)
        self.__port = 80
        self.request = ''
        self.answer = ''
        self._request_type = "POST" if args.post or args.file else "GET"
        if self.__protocol == 'https':
            self.__sock = ssl.wrap_socket(self.sock)
            self.__port = 443

    def do_request(self):
        self.__sock.connect((self.__host, self.__port))
        self.__sock.send(self.request.encode('utf-8'))
        self.answer = self.__sock.recv(1024)
        self.__sock.close()

    def print_answer(self):
        if self.args.verbose:
            print('> ' + self.request + '\r\n' + '< ' + self.answer.decode('utf-8'))
        elif self.args.infile:
            f = open(self.args.infile, 'w')
            f.write(self.answer.decode())
            f.close()
        else:
            print(self.answer.decode())

    def make_request(self):
        if self._request_type == "GET":
            self.request = 'GET ' + self.args.http + ' HTTP/1.1\r\n' \
                                       'Host: ' + self.__host + '\r\n' \
                                                         'Accept: application/x-www-urlencoded\r\n'
        else:
            self.request = 'POST ' \
                           + self.args.http + ' HTTP/1.1\r\n' \
                                       'Host: ' + self.__host + '\r\n' \
                                                'Accept: application/x-www-urlencoded\r\n'
        if self.args.reference:
            self.request += 'Reference: ' + self.args.reference + '\r\n'
        if self.args.cookie:
            self.request += 'Cookie: ' + self.args.cookie + '\r\n'
        if self.args.agent:
            self.request += 'User-Agent: ' + self.args.agent + '\r\n'
        if self.args.post:
            data = self.args.post
            self.request += 'Content-Length: ' \
                            + str(len(data)) + '\r\n' \
                                    '\r\n' \
                                            'body=' + data + '\r\n'
        if self.args.file:
            f = open(self.args.file, 'r')
            data = f.read()
            self.request += 'Content-Length: ' + str(len(data) + 7) + '\r\n' \
                                            '\r\n' \
                                                    'body=' + data + '\r\n'
        self.request += '\r\n'
        return self.request
