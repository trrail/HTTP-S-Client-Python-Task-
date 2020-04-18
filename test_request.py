from request import Request
import argparse
import unittest


class TestHTTPClient(unittest.TestCase):
    parser = argparse.ArgumentParser(description='HTTP(S) - Client')
    parser.add_argument('-d', '--post', type=str, help='post request')
    parser.add_argument('-G', '--get', action='store_true', help='get request')
    parser.add_argument('url', type=str, help='Contains URL')
    parser.add_argument('-e', '--reference', type=str, help='add previous URL')
    parser.add_argument('-v', '--verbose', action='store_true', help='detailed response')
    parser.add_argument('-f', '--file', type=str, help='send data from file')
    parser.add_argument('-c', '--cookie', type=str, help='add cookie')
    parser.add_argument('-A', '--agent', type=str, help='add your own User_Agent')
    parser.add_argument('-O', '--output', type=str, help='print answer in file')

    def test_check_get_request(self):
        self.args = self.parser.parse_args(['http://ptsv2.com/t/lp5td-1586273836/post'])
        request = Request(self.args.url,
                      self.args.reference,
                      self.args.post,
                      self.args.verbose,
                      self.args.file,
                      self.args.cookie,
                      self.args.agent,
                      self.args.output,
                          headers={})
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n\r\n', request.make_request())

    def test_check_post_request_text(self):
        self.args = self.parser.parse_args(['-d "Hello, World!"', 'http://ptsv2.com/t/lp5td-1586273836/post'])
        request = Request(self.args.url,
                      self.args.reference,
                      self.args.post,
                      self.args.verbose,
                      self.args.file,
                      self.args.cookie,
                      self.args.agent,
                      self.args.output,
                          headers={})
        self.assertEqual('POST /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Content-Length: 21\r\n\r\n'
                         'body= "Hello, World!"\r\n\r\n', request.make_request())

    def test_check_get_request_with_reference(self):
        self.args = self.parser.parse_args(['-e', 'http://ptsv2.com/t/lp5td-1586273836', 'http://ptsv2.com/t/lp5td-1586273836/post'])
        request = Request(self.args.url,
                      self.args.reference,
                      self.args.post,
                      self.args.verbose,
                      self.args.file,
                      self.args.cookie,
                      self.args.agent,
                      self.args.output,
                          headers={})
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Reference: http://ptsv2.com/t/lp5td-1586273836\r\n\r\n', request.make_request())

    def test_check_post_request_from_file(self):
        self.args = self.parser.parse_args(['-f', 'test_text.txt', 'http://ptsv2.com/t/lp5td-1586273836/post'])
        request = Request(self.args.url,
                      self.args.reference,
                      self.args.post,
                      self.args.verbose,
                      self.args.file,
                      self.args.cookie,
                      self.args.agent,
                      self.args.output,
                          headers={})
        self.assertEqual('POST /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Content-Length: 32\r\n\r\n'
                         'body="Hello, my name is trail"\r\n\r\n', request.make_request())

    def test_check_get_request_with_user_agent(self):
        self.args = self.parser.parse_args(['http://ptsv2.com/t/lp5td-1586273836/post', '-A', 'Mozilla/5.0'])
        request = Request(self.args.url,
                      self.args.reference,
                      self.args.post,
                      self.args.verbose,
                      self.args.file,
                      self.args.cookie,
                      self.args.agent,
                      self.args.output,
                          headers={})
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'User-Agent: Mozilla/5.0\r\n\r\n', request.make_request())

    def test_check_get_request_with_cookie_and_user_agent(self):
        self.args = self.parser.parse_args(['http://ptsv2.com/t/lp5td-1586273836/post', '-A', 'Mozilla/5.0', '-c', 'income=1'])
        request = Request(self.args.url,
                      self.args.reference,
                      self.args.post,
                      self.args.verbose,
                      self.args.file,
                      self.args.cookie,
                      self.args.agent,
                      self.args.output,
                          headers={})
        self.assertEqual('GET /t/lp5td-1586273836/post HTTP/1.1\r\n'
                         'Host: ptsv2.com\r\n'
                         'Connection: close\r\n'
                         'Cookie: income=1\r\n'
                         'User-Agent: Mozilla/5.0\r\n\r\n', request.make_request())


if __name__ == '__main__':
    unittest.main()