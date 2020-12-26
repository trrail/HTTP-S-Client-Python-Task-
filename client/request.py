from dataclasses import field, dataclass
from enum import Enum
from client import errors
from yarl import URL


class MethodType(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"
    TRACE = "TRACE"


def identify_request_type(method) -> MethodType:
    try:
        for req_type in MethodType:
            if req_type.value.lower() == method:
                return req_type
        raise errors.IncorrectMethodType()
    except errors.IncorrectMethodType as e:
        print(e.message)
        exit(1)


@dataclass
class Request:
    method: MethodType = MethodType.GET
    scheme: str = 'https'
    url: URL = URL('')
    path: str = '/'
    protocol: str = 'HTTP/1.1'
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b''

    def __post_init__(self):
        self.headers["Host"] = URL(self.url).host
        if "Connection" not in self.headers:
            self.headers["Connection"] = "close"
        if "Content-Length" not in self.headers:
            self.headers["Content-Length"] = str(len(self.body))

    def set_host(self, host: str) -> None:
        self.url = URL(f'{self.scheme}://{host}{self.path}')
        self.headers["Host"] = host

    def set_url(self, url: str) -> None:
        self.url = URL(url)
        self.headers["Host"] = URL(url).host
        self.scheme = URL(url).scheme
        self.path = URL(url).path

    def set_headers(self, headers: dict[str, str]) -> None:
        for header in headers.keys():
            self.headers[header] = headers.get(header)

    def set_header(self, header: str, value: str) -> None:
        self.headers[header] = value

    def set_body(self, body: str) -> None:
        self.body = body.encode()
        self.headers['Content-Length'] = str(len(body))

    def set_scheme(self, scheme: str) -> None:
        self.scheme = scheme

    def set_path(self, path: str) -> None:
        self.path = path

    def set_protocol(self, protocol: str):
        self.protocol = protocol

    def set_method(self, method: str):
        self.method = identify_request_type(method)

    def __bytes__(self):
        request = [f"{self.method.value} {self.path} {self.protocol}".encode()]
        for header, value in self.headers.items():
            request.append(f"{header}: {value}".encode())
        request.append(b"")
        request.append(self.body)
        return b"\r\n".join(request)

    @property
    def host(self):
        return self.url.host
