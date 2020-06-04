class DataFromFileAndFromString(BaseException):
    message = 'Невозможно отправить данные из файла и из строки одновременно'


class NoDataToSend(BaseException):
    message = 'Нет данных для отправки'


class UnreadableFile(BaseException):
    message = 'Файл не существует или поверждён'


class VerboseException(BaseException):
    message = 'Ключ -v нельзя совмещать с ключами -1 и -0'


class ConnectionError(BaseException):
    message = "Не смог подсоединиться к серверу. Проверьте URL-ссылку"


class IncorrectRequestType(BaseException):
    message = "Введённый тип запроса не существует. Посмотрите help"


def check_for_exceptions(args):
    request_type = args.request if args.request else "GET"
    try:
        if args.verbose and (args.bodyignore or args.headignore):
            raise VerboseException
        if args.file and args.data:
            raise DataFromFileAndFromString
        if not args.file and not args.data:
            if request_type == "PUT" or request_type == "POST" or request_type == "DELETE" or request_type == "PATCH":
                raise NoDataToSend
    except DataFromFileAndFromString:
        print(DataFromFileAndFromString.message)
        exit()
    except NoDataToSend:
        print(NoDataToSend.message)
        exit()
    except VerboseException:
        print(VerboseException.message)
        exit()

    if args.file:
        try:
            f = open(args.file, 'r')
            f.read()
            f.close()
        except BaseException:
            print(UnreadableFile.message)
            exit()
    if args.cookiefile:
        try:
            f = open(args.cookiefile, 'r')
            f.read()
            f.close()
        except BaseException:
            print(UnreadableFile.message)
            exit()