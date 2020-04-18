from request import Request
import argparse
import re


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
parser.add_argument('-H', '--headers', type=str, help='add headers in request')


def make_request():
    args = parser.parse_args()
    headers = {}
    if args.headers:
        parsed_headers = args.headers.split('$')
        for header in parsed_headers:
            head = re.findall(r'[a-zA-Z]+:', header)
            value = re.findall(r': [a-zA-z0-9\:\-/\.\*]+', header)
            headers[head[0][:-1]] = value[0][2:]
    request = Request(args.url,
                      args.reference,
                      args.post,
                      args.verbose,
                      args.file,
                      args.cookie,
                      args.agent,
                      args.output,
                      headers)
    request.make_request()
    request.do_request()
    request.print_answer()


if __name__ == '__main__':
    make_request()
