import re


class Response():
    def __init__(self):
        self._byte_array = bytearray()
        self._response = ''
        self._charset = ''
        self._re_code = ''
        self._head_response = ''
        self._body_response = ''
        self._location = ''
        self._prepared_response = []

    def read_response(self, data):
        if len(self._byte_array) == 0:
            self.head_of_response(data)
        else:
            self._byte_array.extend(data)

    def head_of_response(self, data):
        response = data.decode("ISO-8859-1")
        splited_head = response.split('\r\n')
        self._re_code = splited_head[0].split(' ')[1]
        for i in splited_head:
            if i[:8:] == 'Location' or i[:8:] == 'location':
                self._location = i.split(': ')[1]
            if i[:12:] == 'Content-Type' or i[:12:] == 'content-type':
                self._charset = i.split(': ')[1].split('; ')
                if len(self._charset) == 1:
                    self._charset = 'UTF-8'
                else:
                    self._charset = self._charset[1][8::]
        self._byte_array.extend(data)

    def return_response(self):
        self._response = self._byte_array.decode(self._charset)
        self._head_response = re.split(r'\r\n\r\n', self._response)[0]
        self._body_response = re.split(r'\r\n\r\n', self._response)[1]
        self._prepared_response.append(self._response)
        self._prepared_response.append(self._head_response)
        self._prepared_response.append(self._body_response)
        self._prepared_response.append(self._byte_array)
        self._prepared_response.append(self._location)
        return self._prepared_response

