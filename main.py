from client.request import Request
from client.httpclient import HttpClient
from client.response import Response
import argparse
from yarl import URL
from client import errors
import sys

max = 10

parser = argparse.ArgumentParser(description="HTTP(S) - Client")
parser.add_argument("-d", "--data", type=str, help="data for request")
parser.add_argument(
    "-r",
    "--request",
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
    errors.check_for_exceptions(args)
    data = prepare_data(args)
    location = None
    for i in range(max):
        headers = prepare_headers(args, location)
        request = Request.prepare_request(
            headers=headers,
            data=data,
            request_type=args.request,
            url=args.url if location is None else location,
            scheme=args.scheme if args.scheme is not None else "http",
            host=args.host,
            path=args.path if args.path is not None else "",
        )
        http_client = HttpClient(request,
                                 int(args.timeout) if args.timeout
                                 else 1000)
        http_client.do_request()
        response = Response.prepare_fields(http_client.response)
        if response.code // 100 == 3:
            location = response.location
        else:
            show_response(request.request, response, args)
            break


def show_response(request, response, args):
    if args.bodyignore:
        answer = [f"HTTP/{response.protocol} {response.code} OK"]
        for header, value in response.headers.items():
            answer.append(f"{header}: {value}")
        sys.stdout.write("\r\n".join(answer))
    elif args.headignore:
        sys.stdout.write(response.message)
    elif args.verbose:
        answer = [f"{request}", "\r\n",
                  f"HTTP/{response.protocol} {response.code} OK"]
        for header, value in response.headers.items():
            answer.append(f"{header}: {value}")
        answer.append("\r\n")
        answer.append(response.message)
        sys.stdout.write("\r\n".join(answer))
    elif args.output:
        f = open(args.output, "bw")
        f.write(response.message.encode(response.charset))
        f.close()
    else:
        answer = [f"HTTP/{response.protocol} {response.code} OK"]
        for header, value in response.headers.items():
            answer.append(f"{header}: {value}")
        answer.append("\r\n")
        answer.append(response.message)
        sys.stdout.write("\r\n".join(answer))


def prepare_headers(args, location: str = None) -> dict:
    if location is not None:
        host = URL(location).host
    elif args.url is not None:
        host = URL(args.url).host
    elif args.host is not None:
        host = args.host
    else:
        raise AttributeError
    headers = {"Host": host, "Connection": "close"}
    if args.my_headers:
        for header in args.my_headers:
            separator_ind = header.find(":")
            key = header[0:separator_ind]
            value = header[separator_ind + 1::].strip()
            headers[key] = value
    if args.reference:
        headers["Reference"] = args.reference
    if args.cookie:
        headers["Cookie"] = args.cookie
    if args.cookiefile:
        with open(args.cookiefile, "r") as f:
            headers["Cookie"] = f.read()
    if args.agent:
        headers["User-Agent"] = args.agent
    return headers


def prepare_data(args):
    data = ""
    if args.data:
        data = args.data
    if args.file:
        f = open(args.file)
        data = f.read()
        f.close()
    return data


if __name__ == "__main__":
    make_request()
