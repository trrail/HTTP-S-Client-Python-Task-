from client import request as req
import argparse
from client import errors
from client import response as res
import sys


parser = argparse.ArgumentParser(description='HTTP(S) - Client')
parser.add_argument('-d', '--data', type=str, help='data for request')
parser.add_argument('-r', '--request', type=str, help='choose request method:'
                                                      'GET|'
                                                      'POST|'
                                                      'PUT|'
                                                      'CONNECT|'
                                                      'PATCH|'
                                                      'OPTIONS|'
                                                      'DELETE|'
                                                      'HEAD|'
                                                      'TRACE')
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


def make_request():
    args = parser.parse_args()
    errors.check_for_exceptions(args)
    data = prepare_data(args)
    request = req.Request(args.url,
                      args.reference,
                      args.cookie,
                      args.agent,
                      args.my_headers,
                      args.request,
                      args.cookiefile,
                      args.timeout,
                          data)
    answer = request.do_request()
    show_response(answer[0], answer[1], args)


def show_response(request, response, args):
    if args.bodyignore:
        answer = [f'{response.response.decode(response.charset)[:15]}']
        for header, value in response.headers.items():
            answer.append(f'{header}: {value}')
        sys.stdout.write('\r\n'.join(answer))
    elif args.headignore:
        sys.stdout.write(response.message)
    elif args.verbose:
        sys.stdout.write(f'{request} \r\n{response.response.decode(response.charset)}')
    elif args.output:
        f = open(args.output, 'bw')
        f.write(response.message.encode(response.charset))
        f.close()
    else:
        sys.stdout.write(response.response.decode(response.charset))


def prepare_data(args):
    data = ''
    if args.data:
        data = args.data
    if args.file:
        f = open(args.file)
        data = f.read()
        f.close()
    return data


if __name__ == '__main__':
    make_request()