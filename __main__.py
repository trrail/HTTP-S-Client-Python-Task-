import os
import socket
from client.request import Request
from client import errors
from client.httpclient import HttpClient
import argparse
import sys

MAX: int = 10

parser = argparse.ArgumentParser(description="HTTP(S) - Client")
parser.add_argument("-d", "--data", type=str, help="data for request")
parser.add_argument("-m", "--method",
                    type=str,
                    help="choose request method:"
                         "GET|"
                         "POST|"
                         "PUT|"
                         "CONNECT|"
                         "PATCH|"
                         "OPTIONS|"
                         "DELETE|"
                         "HEAD|"
                         "TRACE",
                    )
parser.add_argument("-u", "--url", type=str, help="Contains URL")
parser.add_argument("-e", "--reference", type=str, help="add previous URL")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="detailed response")
parser.add_argument("-f", "--file", type=str, help="send data from file")
parser.add_argument("-c", "--cookie", type=str, help="add cookie")
parser.add_argument("-C", "--cookiefile", type=str,
                    help="send cookie from file")
parser.add_argument("-A", "--agent", type=str, help="add your own User_Agent")
parser.add_argument("-O", "--output", type=str, help="print answer in file")
parser.add_argument(
    "-H",
    "--headers",
    type=str,
    nargs="+",
    help="add headers in request",
    dest="my_headers",
)
parser.add_argument(
    "-0", "--bodyignore", action="store_true", help="ignore body of response"
)
parser.add_argument(
    "-1", "--headignore", action="store_true", help="ignore head of response"
)
parser.add_argument("-t", "--timeout", type=str, help="reset timeout")
parser.add_argument("-l", "--host", type=str,
                    help="custom host, default value is None")
parser.add_argument("-s", "--scheme", type=str,
                    help="setup scheme, default is http")
parser.add_argument(
    "-P",
    "--path",
    type=str,
    help="setup path, should start with </>, haven't default path",
)


def prepare_request(arguments) -> Request:
    request = Request()
    if arguments.url is not None:
        request.set_url(arguments.url)
    elif arguments.host is not None:
        request.set_host(arguments.host)
    else:
        raise AttributeError
    if arguments.method:
        request.set_method(arguments.method)
    if arguments.path:
        request.set_path(arguments.path)
    if arguments.scheme:
        request.set_scheme(arguments.scheme)
    if arguments.my_headers:
        headers = {}
        for header in arguments.my_headers:
            separator_ind = header.find(":")
            key = header[0:separator_ind]
            value = header[separator_ind + 1::].strip()
            headers[key] = value
        request.set_headers(headers)
    if arguments.reference:
        request.set_header('Reference', arguments.reference)
    if arguments.cookie:
        request.set_header('Cookie', arguments.cookie)
    if arguments.cookiefile:
        with open(arguments.cookiefile, "r") as file:
            request.set_header('Cookie', file.read())
    if arguments.agent:
        request.set_header('User-Agent', arguments.agent)
    if arguments.data:
        request.set_body(arguments.data)
    if arguments.file:
        with open(arguments.file, 'r') as file:
            request.set_body(file.read())
    return request


def show_response(request, response, args):
    if args.bodyignore:
        sys.stdout.write(bytes(response).decode())
    elif args.headignore:
        sys.stdout.write(response.body)
    elif args.verbose:
        answer = [f"{bytes(request).decode()}", "\r\n",
                  f'{bytes(response).decode()}', '\r\n', response.body]
        sys.stdout.write("\r\n".join(answer))
    elif args.output:
        with open(args.output, 'bw') as file:
            file.write(response.body.encode(response.charset))
    else:
        answer = [f'{bytes(response).decode()}', '\r\n', response.body]
        sys.stdout.write("\r\n".join(answer))


def check_for_exceptions(arguments):
    try:
        if arguments.verbose and \
                (arguments.bodyignore or arguments.headignore):
            raise errors.VerboseException
        if arguments.file and arguments.data:
            raise errors.DataFromFileAndFromString
    except errors.DataFromFileAndFromString as e:
        print(e.message)
        exit(1)
    except errors.VerboseException as e:
        print(e.message)
        exit(1)

    if arguments.file:
        try:
            if not (os.path.exists(arguments.file)):
                raise errors.HTTPSClientException
        except errors.HTTPSClientException:
            print(errors.UnreadableFile.message)
            exit(1)
    if arguments.cookiefile:
        try:
            if not os.path.exists(arguments.file):
                raise errors.HTTPSClientException
        except errors.HTTPSClientException:
            print(errors.UnreadableFile.message)
            exit(1)


args = parser.parse_args()
check_for_exceptions(args)
request = prepare_request(args)
try:
    response = HttpClient().do_request(request, 1000, 10)
    show_response(request, response, args)
except errors.MaxDirectionsError:
    print(errors.MaxDirectionsError.message)
    exit(1)
except errors.HTTPSClientException:
    print(errors.ConnectError.message)
    exit(1)
except socket.gaierror:
    print(errors.ConnectError.message)
    exit(1)
