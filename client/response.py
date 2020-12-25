import re
from dataclasses import dataclass, field


@dataclass
class Response:
    body: str = ''
    charset: str = 'utf-8'
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
        charset = ""
        headers = {}
        location = ""
        for i in response.split("\r\n\r\n")[0].split("\r\n"):
            s = re.search(
                r"(?P<header>[a-zA-Z-]*): " r"(?P<value>[0-9\s\w,.;=/:-]*)", i
            )
            if s is not None:
                headers[s.group("header")] = s.group("value")
                if (
                    s.group("header") == "Content-Type"
                    or s.group("header") == "content-type"
                ):
                    f = re.search(
                        r"[a-zA-z/]*; " r"charset=(?P<charset>" r"[\w\d-]*)",
                        s.group("value"),
                    )
                    if f is not None:
                        charset = f.group("charset")
                    else:
                        charset = "utf-8"
                if s.group("header") == "Location" \
                        or s.group("header") == "location":
                    location = s.group("value")
        return cls(body=body, charset=charset,
                   code=int(code), location=location,
                   protocol=float(protocol), headers=headers)
