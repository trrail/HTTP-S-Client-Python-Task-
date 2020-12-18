from client import errors
from client.request import Request
import socket
import ssl


class HttpClient:
    def __init__(self, request: Request, timeout: int):
        self.request = request
        self.timeout = timeout
        self.response = bytearray()

    def do_request(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.request.url.scheme == "https":
            sock = ssl.wrap_socket(sock)
        try:
            sock.connect((self.request.url.host, self.request.url.port))
        except Exception:
            print(errors.ConnectionError.message)
            exit(1)
        sock.settimeout(self.timeout)
        if self.request.url.scheme == "https":
            sock.do_handshake()
        sock.sendall(self.request.request.encode())
        while True:
            data = sock.recv(1024)
            if not data:
                break
            self.response.extend(data)
        sock.close()
