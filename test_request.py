from client import request as req
import argparse
import unittest
from client import errors as er
from client import response as res

class TestHTTPClient(unittest.TestCase):
    parser = argparse.ArgumentParser(description='HTTP(S) - Client')
    parser.add_argument('-d', '--data', type=str, help='data for request')
    parser.add_argument('-r', '--request', type=str, help='choose request method')
    parser.add_argument('url', type=str, help='Contains URL')
    parser.add_argument('-e', '--reference', type=str, help='add previous URL')
    parser.add_argument('-v', '--verbose', action='store_true', help='detailed response')
    parser.add_argument('-f', '--file', type=str, help='send data from file')
    parser.add_argument('-c', '--cookie', type=str, help='add cookie')
    parser.add_argument('-C', '--cookiefile', type=str, help='send cookie from file')
    parser.add_argument('-A', '--agent', type=str, help='add your own User_Agent')
    parser.add_argument('-O', '--output', type=str, help='print answer in file')
    parser.add_argument('-H', '--headers', type=str, nargs="+", help='add headers in request', dest="my_headers")
    parser.add_argument('-0', '--bodyignore', action='store_true', help='ignore body of response')
    parser.add_argument('-1', '--headignore', action='store_true', help='ignore head of response')
    parser.add_argument('-t', '--timeout', type=str, help='reset timeout')

    def test_check_get_request(self):
        args = self.parser.parse_args(['http://ptsv2.com/t/lp5td-1586273836/post'])
        request = req.Request(args.url,
                              args.reference,
                              args.data,
                              args.verbose,
                              args.file,
                              args.cookie,
                              args.agent,
                              args.output,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.bodyignore,
                              args.headignore,
                              args.timeout)
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n\r\n', request.make_request())

    def test_check_post_request_text(self):
        args = self.parser.parse_args(['-d', 'Hello, World!',
                                            'http://ptsv2.com/t/lp5td-1586273836/post',
                                            '-r', 'POST'])
        request = req.Request(args.url,
                              args.reference,
                              args.data,
                              args.verbose,
                              args.file,
                              args.cookie,
                              args.agent,
                              args.output,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.bodyignore,
                              args.headignore,
                              args.timeout)
        self.assertEqual('POST /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Content-Length: 13\r\n\r\n'
                         'Hello, World!\r\n', request.make_request())

    def test_check_get_request_with_reference(self):
        args = self.parser.parse_args(['-e', 'http://ptsv2.com/t/lp5td-1586273836',
                                            'http://ptsv2.com/t/lp5td-1586273836/post'])
        request = req.Request(args.url,
                              args.reference,
                              args.data,
                              args.verbose,
                              args.file,
                              args.cookie,
                              args.agent,
                              args.output,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.bodyignore,
                              args.headignore,
                              args.timeout)
        request.prepare_headers()
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Reference: http://ptsv2.com/t/lp5td-1586273836\r\n\r\n', request.make_request())

    def test_check_post_request_from_file(self):
        args = self.parser.parse_args(['-f', 'test_text.txt',
                                            'http://ptsv2.com/t/lp5td-1586273836/post',
                                            '-r', 'POST'])
        f = open('test_text.txt', 'w')
        f.write("Hello, my name is trail")
        f.close()
        request = req.Request(args.url,
                              args.reference,
                              args.data,
                              args.verbose,
                              args.file,
                              args.cookie,
                              args.agent,
                              args.output,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.bodyignore,
                              args.headignore,
                              args.timeout)
        self.assertEqual('POST /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Content-Length: 23\r\n\r\n'
                         'Hello, my name is trail\r\n', request.make_request())

    def test_check_get_request_with_user_agent(self):
        args = self.parser.parse_args(['http://ptsv2.com/t/lp5td-1586273836/post',
                                            '-A', 'Mozilla/5.0'])
        request = req.Request(args.url,
                              args.reference,
                              args.data,
                              args.verbose,
                              args.file,
                              args.cookie,
                              args.agent,
                              args.output,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.bodyignore,
                              args.headignore,
                              args.timeout)
        request.prepare_headers()
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'User-Agent: Mozilla/5.0\r\n\r\n', request.make_request())

    def test_check_get_request_with_cookie_and_user_agent(self):
        args = self.parser.parse_args(['http://ptsv2.com/t/lp5td-1586273836/post',
                                            '-A', 'Mozilla/5.0',
                                            '-c', 'income=1'])
        request = req.Request(args.url,
                              args.reference,
                              args.data,
                              args.verbose,
                              args.file,
                              args.cookie,
                              args.agent,
                              args.output,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.bodyignore,
                              args.headignore,
                              args.timeout)
        request.prepare_headers()
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Cookie: income=1\r\n'
                         'User-Agent: Mozilla/5.0\r\n\r\n', request.make_request())

    def test_connection_error(self):
        args = self.parser.parse_args(['tralala',
                                       '-v', '-1'])
        request = req.Request(args.url,
                              args.reference,
                              args.data,
                              args.verbose,
                              args.file,
                              args.cookie,
                              args.agent,
                              args.output,
                              args.my_headers,
                              args.request,
                              args.cookiefile,
                              args.bodyignore,
                              args.headignore,
                              args.timeout)
        self.assertRaises(er.ConnectionError, request.do_request())

    def test_response(self):
        text = 'HTTP/1.1 200 Ok\r\n' \
               'Server: VK\r\n' \
               'Connection: close\r\n' \
               'Content-Type: text/html; charset=UTF-8\r\n\r\nHello'
        response = res.Response()
        response.read_response(text.encode('utf-8'))
        re = response.return_response()
        self.assertEqual(re[0], text)
        self.assertEqual(re[1], text.split('\r\n\r\n')[0])
        self.assertEqual(re[2], text.split('\r\n\r\n')[1])
        self.assertEqual(re[3], text.encode('utf-8'))
        self.assertEqual(re[4], '')


if __name__ == '__main__':
    unittest.main()