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
