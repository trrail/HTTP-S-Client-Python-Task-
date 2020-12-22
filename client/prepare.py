from yarl import URL


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
