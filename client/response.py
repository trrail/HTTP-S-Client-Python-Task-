import re
from dataclasses import dataclass, field


@dataclass
class Response:
    body: str = ''
    charset: str = ''
    code: int = -1
    location: str = None
    headers: dict[str, str] = field(default_factory=dict)
    protocol: float = 1.0

    @classmethod
    def parse(cls, data: bytes):
        response = data.decode("ISO-8859-1")
        code = (re.search(r" [\d]* ", response)).group(0)
        protocol = (re.search(r"[\d\.\d]* ", response)).group(0)
        body = response.split("\r\n\r\n")[1]
        charset = "utf-8"
        headers = {}
        location = ""
        for i in response.split("\r\n\r\n")[0].split("\r\n"):
            search_headers = re.search(r"(?P<header>[a-zA-Z-]*): "
                                       r"" r"(?P<value>[0-9\s\w,.;=/:-]*)", i)
            if search_headers is not None:
                headers[search_headers.group("header")] = \
                    search_headers.group("value")
                if (search_headers.group("header") == "Content-Type" or
                        search_headers.group("header") == "content-type"):
                    search_charset = re.search(r"[a-zA-z/]*; " r"charset="
                                               r"(?P<charset>" r"[\w\d-]*)",
                                               search_headers.group("value"))
                    charset = 'utf-8' if search_charset is None \
                        else search_charset.group("charset")
                if search_headers.group("header") == "Location" \
                        or search_headers.group("header") == "location":
                    location = search_headers.group("value")
        return cls(body=body, charset=charset,
                   code=int(code), location=location,
                   protocol=float(protocol), headers=headers)
