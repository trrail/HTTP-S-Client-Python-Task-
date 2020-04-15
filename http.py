import socket
import ssl
import argparse
import re
import unittest

pattern_host = re.compile(r'//[\w\.]+/')
pattern_protocol = re.compile(r'https*:')

parser = argparse.ArgumentParser(description='HTTP(S) - Client')
parser.add_argument('-d', '--post', type=str, help='post request')
parser.add_argument('-G', '--get', action='store_true', help='get request')
parser.add_argument('http', type=str, help='Contains URL')
parser.add_argument('-e', '--reference', type=str, help='previous URL')
parser.add_argument('-I', '--headonly', action='store_true', help='return only HTTP heading')
parser.add_argument('-v', '--verbose', action='store_true', help='detailed response')
parser.add_argument('-f', '--file', type=str, help='send data from file')
args = parser.parse_args()


def make_request(args):
    host = (re.findall(pattern_host, args.http))[0][2:][:-1]
    protocol = re.findall(pattern_protocol, args.http)
    request = ''
    if args.post:
        request = post_request(host)
    if args.file:
        request = post_request(host)
    else:
        request = get_request(host)

    if protocol == 'https':
        https_request = RequestHttps()
        https_request.do_request(request=request, host=host)
    else:
        http_request = RequestHttp()
        http_request.do_request(request=request, host=host)


class RequestHttp():
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def do_request(self, request='', host=''):
        self.__sock.connect((host, 80))
        self.__sock.send(request.encode('utf-8'))
        answer = self.__sock.recv(1024)
        self.__sock.close()
        print_answer(answer, request=request)


class RequestHttps():
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__ssl_sock = ssl.wrap_socket(self.__sock)
        pass

    def do_request(self, request='', host=''):
        self.__ssl_sock.connect((host, 443))
        self.__ssl_sock.send(request.encode('utf-8'))
        answer = self.__ssl_sock.recv(1024)
        self.__ssl_sock.close()
        print_answer(answer, request=request)


def print_answer(answer, request=''):
    if args.verbose:
        print('> ' + request + '\r\n' + '< ' + answer.decode())
    else:
        print(answer.decode())


def get_request(host=''):
    request = 'GET ' + args.http + ' HTTP/1.1\r\n' \
            'Host: ' + host + '\r\n' \
            'Accept: application/x-www-urlencoded\r\n'
    if args.reference:
        request += 'Reference: ' + args.reference + '\r\n'
    if args.post:
        data = args.post
        request += 'Content-Length: ' + str(len(data)) + '\r\n' \
                    '\r\n\r\n' \
                    'body=' + data + '\r\n'
    request += '\r\n'
    return request


def post_request(host=''):
    request = 'POST ' + args.http + ' HTTP/1.1\r\n' \
            'Host: ' + host + '\r\n' \
            'Accept: application/x-www-urlencoded\r\n' \
            'Cookie: income=1\r\n'
    if args.reference:
        request += 'Reference: ' + args.reference + '\r\n'
    if args.post:
        data = args.post
        request += 'Content-Length: ' + str(len(data) + 7) + '\r\n' \
                '\r\n\r\n' \
                'body=' + data + '\r\n'
    if args.file:
        f = open(args.file, 'r')
        data = f.read()
        request += 'Content-Length: ' + str(len(data) + 7) + '\r\n' \
                                                        '\r\n\r\n' \
                                                         'body=' + data + '\r\n'
    request += '\r\n'
    return request


make_request(args)
