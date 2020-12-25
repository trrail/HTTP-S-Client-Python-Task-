from yarl import URL

from client.request import Request
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


def make_request():
    args = parser.parse_args()
    request = prepare_request(args)
    response = HttpClient().do_request(request, 1000, MAX)
    show_response(request, response, args)


def prepare_request(args) -> Request:
    if args.url is not None:
        request = Request(url=URL(args.url))
    elif args.host is not None:
        request = Request()
        request.set_host(args.host)
    else:
        raise AttributeError
    if args.method:
        request.set_method(args.method)
    if args.path:
        request.set_path(args.path)
    if args.scheme:
        request.set_scheme(args.scheme)
    if args.my_headers:
        headers = {}
        for header in args.my_headers:
            separator_ind = header.find(":")
            key = header[0:separator_ind]
            value = header[separator_ind + 1::].strip()
            headers[key] = value
        request.set_headers(headers)
    if args.reference:
        request.set_header('Reference', args.reference)
    if args.cookie:
        request.set_header('Cookie', args.cookie)
    if args.cookiefile:
        with open(args.cookiefile, "r") as file:
            request.set_header('Cookie', file.read())
    if args.agent:
        request.set_header('User-Agent', args.agent)
    if args.data:
        request.set_body(args.data)
    if args.file:
        with open(args.file, 'r') as file:
            request.set_body(file.read())
    return request


def show_response(request, response, args):
    if args.bodyignore:
        answer = [f"HTTP/{response.protocol} {response.code} OK"]
        for header, value in response.headers.items():
            answer.append(f"{header}: {value}")
        sys.stdout.write("\r\n".join(answer))
    elif args.headignore:
        sys.stdout.write(response.body)
    elif args.verbose:
        answer = [f"{bytes(request).decode()}", "\r\n",
                  f"HTTP/{response.protocol} {response.code} OK"]
        for header, value in response.headers.items():
            answer.append(f"{header}: {value}")
        answer.append("\r\n")
        answer.append(response.body)
        sys.stdout.write("\r\n".join(answer))
    elif args.output:
        with open(args.output, 'bw') as file:
            file.write(response.body.encode(response.charset))
    else:
        answer = [f"HTTP/{response.protocol} {response.code} OK"]
        for header, value in response.headers.items():
            answer.append(f"{header}: {value}")
        answer.append("\r\n")
        answer.append(response.body)
        sys.stdout.write("\r\n".join(answer))


if __name__ == "__main__":
    make_request()
