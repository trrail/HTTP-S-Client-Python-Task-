from client import errors
from client.request import Request
import socket
import ssl
from client.response import Response


class HttpClient:
    @staticmethod
    def do_request(request: Request, timeout: int = 1000,
                   max_iterations: int = 10) -> Response:
        try:
            while max_iterations >= 0:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if request.scheme == "https":
                    sock = ssl.wrap_socket(sock)
                sock.settimeout(timeout)
                max_iterations -= 1
                try:
                    sock.connect((request.host,
                                  80 if request.scheme == 'http' else 443))
                except errors.HTTPSClientException:
                    print(errors.ConnectError.message)
                    exit(1)
                if request.scheme == "https":
                    sock.do_handshake()
                sock.sendall(bytes(request))
                obtained_data = b''
                while True:
                    data = sock.recv(1024)
                    if not data:
                        break
                    obtained_data += data
                sock.close()
                response = Response.parse(obtained_data)
                if 300 <= response.code < 400:
                    request.set_url(response.location)
                else:
                    return response
            raise errors.MaxDirectionsError()
        except errors.MaxDirectionsError:
            print(errors.MaxDirectionsError.message)
            exit(1)
