import re


class Response():
    def __init__(self):
        self._byte_array = bytearray()
        self._response = ''
        self._charset = ''
        self._re_code = ''
        '''
        self._response_head = re.split(r'\r\n\r\n', response)[0]
        '''

    def read_response(self, data):
        if len(self._byte_array) == 0:
            self.head_of_response(data)
        else:
            self._byte_array.extend(data)

    def head_of_response(self, data):
        response = data.decode("ISO-8859-1")
        spliter = response.split('\r\n')
        self._re_code = spliter[0].split(' ')[1]
        for i in spliter:
            if i[:12:] == 'Content-Type' or i[:12:] == 'content-type':
                self._charset = i.split(': ')[1].split('; ')[1][8::]
        self._byte_array.extend(data)

    def print_response(self):
        print(self._byte_array.decode(self._charset))

