from client import request as req
import argparse
import unittest
from client import response as res
import main
from client import errors


class TestHTTPClient(unittest.TestCase):
    parser = argparse.ArgumentParser(description='HTTP(S) - Client')
    parser.add_argument('-d', '--data', type=str, help='data for request')
    parser.add_argument('-r', '--request', type=str, help='choose request '
                                                          'method')
    parser.add_argument('url', type=str, help='Contains URL')
    parser.add_argument('-e', '--reference', type=str, help='add previous URL')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='detailed response')
    parser.add_argument('-f', '--file', type=str,
                        help='send data from file')
    parser.add_argument('-c', '--cookie', type=str, help='add cookie')
    parser.add_argument('-C', '--cookiefile', type=str,
                        help='send cookie from file')
    parser.add_argument('-A', '--agent', type=str, help='add your own '
                                                        'User_Agent')
    parser.add_argument('-O', '--output', type=str,
                        help='print answer in file')
    parser.add_argument('-H', '--headers', type=str, nargs="+",
                        help='add headers in request', dest="my_headers")
    parser.add_argument('-0', '--bodyignore', action='store_true',
                        help='ignore body of response')
    parser.add_argument('-1', '--headignore', action='store_true',
                        help='ignore head of response')
    parser.add_argument('-t', '--timeout', type=str, help='reset '
                                                          'timeout')

    def test_check_get_request(self):
        args = self.parser.parse_args(['http://ptsv2.com'
                                       '/t/lp5td-1586273836/post'])
        data = ''
        request = req.Request(args.url,
                              args.reference,
                              args.cookie,
                              args.agent,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.timeout,
                              data)
        request.make_request()
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n\r\n', request.request)

    def test_check_post_request_text(self):
        args = self.parser.parse_args(['-d', 'Hello, World!',
                                       'http://ptsv2.com/t/lp'
                                       '5td-1586273836/post',
                                       '-r', 'POST'])
        data = main.prepare_data(args)
        request = req.Request(args.url,
                              args.reference,
                              args.cookie,
                              args.agent,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.timeout,
                              data)
        request.make_request()
        self.assertEqual('POST /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Content-Length: 13\r\n\r\n'
                         'Hello, World!', request.request)

    def test_check_post_request_from_file(self):
        args = self.parser.parse_args(['-f', 'test_text.txt',
                                             'http://ptsv2.com/t'
                                             '/lp5td-1586273836/post',
                                             '-r', 'POST'])
        f = open('test_text.txt', 'w')
        f.write("Hello, my name is trail")
        f.close()
        self.assertEqual('Hello, my name is trail',
                         main.prepare_data(args))

    def test_response(self):
        text = 'HTTP/1.1 200 Ok\r\n' \
               'Server: VK\r\n' \
               'Connection: close\r\n' \
               'Content-Type: text/html; charset=UTF-8\r\n\r\nHello'
        new_response = res.Response.prepare_fields(text.encode('utf-8'))
        self.assertEqual(200, new_response.code)
        self.assertEqual({'Server': 'VK', 'Connection': 'close',
                          'Content-Type': 'text/h'
                                          'tml; charset=UTF-8'},
                         new_response.headers)
        self.assertEqual('UTF-8', new_response.charset)
        self.assertEqual('Hello', new_response.message)

    def test_prepare_headers(self):
        args = self.parser.parse_args(['http://ptsv2.com/t/lp5'
                                       'td-1586273836/post',
                                       '-H', 'Content-Length: 30', 'Pory: tau',
                                       '-e', 'https://vk.com/',
                                       '-c', 'income=1',
                                       '-C', 'cookie.txt',
                                       '-A', 'Chrome'])
        f = open('cookie.txt', 'w')
        f.write('hello')
        f.close()
        data = ''
        request = req.Request(args.url,
                              args.reference,
                              args.cookie,
                              args.agent,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.timeout,
                              data)
        request.prepare_headers()
        self.assertEqual({'Content-Length': '30',
                          'Pory': 'tau', 'Reference': 'https://vk.com/',
                          'Cookie': 'hello', 'User-Agent': 'Chrome'},
                         request.headers)

    def test_request(self):
        args = self.parser.parse_args(['http://ptsv2.com'
                                       '/t/lp5td-1586273836/post'])
        request = req.Request(args.url,
                              args.reference,
                              args.cookie,
                              args.agent,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.timeout,
                              '')
        data = request.do_request()
        self.assertNotEqual(None, data[0])
        self.assertNotEqual(None, data[1])


if __name__ == '__main__':
    unittest.main()
