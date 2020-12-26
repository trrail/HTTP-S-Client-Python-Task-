import os


class HTTPSClientException(Exception):
    pass


class DataFromFileAndFromString(HTTPSClientException):
    message = "Невозможно отправить данные из файла и из строки одновременно"


class UnreadableFile(HTTPSClientException):
    message = "Файл не существует или поверждён"


class VerboseException(HTTPSClientException):
    message = "Ключ -v нельзя совмещать с ключами -1 и -0"


class ConnectError(HTTPSClientException):
    message = "Не смог подсоединиться к серверу. Проверьте URL-ссылку"


class MaxDirectionsError(HTTPSClientException):
    message = "Закончились попытки на переадресацию"


class IncorrectMethodType(HTTPSClientException):
    message = "Введённый тип запроса не существует. Посмотрите help"


def check_for_exceptions(args):
    try:
        if args.verbose and (args.bodyignore or args.headignore):
            raise VerboseException
        if args.file and args.data:
            raise DataFromFileAndFromString
    except DataFromFileAndFromString as e:
        print(e.message)
        exit(1)
    except VerboseException as e:
        print(e.message)
        exit(1)

    if args.file:
        try:
            if not (os.path.exists(args.file)):
                raise HTTPSClientException
        except HTTPSClientException:
            print(UnreadableFile.message)
            exit(1)
    if args.cookiefile:
        try:
            if not os.path.exists(args.file):
                raise HTTPSClientException
        except HTTPSClientException:
            print(UnreadableFile.message)
            exit(1)
