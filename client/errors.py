class UncorrectEnter(Exception):
    pass


class UncorrectArguments(Exception):
    pass


class UnreadableFile(Exception):
    pass


def check_for_exceptions(args):
    request_type = args.request if args.request else "GET"
    if args.file and args.data:
        raise UncorrectArguments()
    if not args.file and not args.data:
        if request_type == "PUT" or request_type == "POST" or request_type == "DELETE" or request_type == "PATCH":
            raise UncorrectArguments()

    if args.file:
        f = open(args.file, 'r')
        try:
            f.read()
        except UnreadableFile():
            pass
        finally:
            f.close()
    if args.cookiefile:
        f = open(args.cookiefile, 'r')
        try:
            f.read()
        except UnreadableFile():
            pass
        finally:
            f.close()
    if args.verbose and (args.bodyignore or args.headignore):
        raise UncorrectArguments()