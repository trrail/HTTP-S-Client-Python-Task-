from enum import Enum
from client import errors
from yarl import URL


def prepare_url(url: str = None,
                scheme: str = "https",
                host: str = None,
                path: str = "") -> URL:
    return (URL(url) if url is not None
            else URL("{0}://{1}{2}".format(scheme, host, path)))


def make_request(req_type: str, url: URL, headers: dict, data: str) -> str:
    request = [f"{req_type} {url.path} HTTP/1.1"]
    for header, value in headers.items():
        request.append(f"{header}: {value}")
    if len(data) != 0:
        request.append(f"Content-Length: {len(data)}")
    request.append("")
    request.append(f"{data}")
    return "\r\n".join(request)


def identify_request_type(request_type) -> str:
    try:
        for req_type in RequestType:
            if req_type.value.lower() == request_type:
                return req_type.value
        raise errors.IncorrectRequestType()
    except errors.IncorrectRequestType as e:
        print(e.message)
        exit(1)


class RequestType(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"
    TRACE = "TRACE"


class Request:
    def __init__(self, request: str, url: URL):
        self.request = request
        self.url = url

    @classmethod
    def prepare_request(
            cls,
            headers: dict,
            request_type: str,
            data: str = '',
            url: str = None,
            scheme: str = None,
            host: str = None,
            path: str = None):
        scheme = scheme if url is None else URL(url).scheme
        url = prepare_url(url, scheme, host, path)
        return cls(make_request(identify_request_type(request_type),
                                url, headers, data), url)
