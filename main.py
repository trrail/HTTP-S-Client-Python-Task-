from request import Request
import argparse
import re
import errors


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


def make_request():
    args = parser.parse_args()
    errors.check_for_exceptions(args)
    request = Request(args.url,
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
                      args.headignore)
    request.do_request()


if __name__ == '__main__':
    make_request()
