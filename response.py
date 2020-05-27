import argparse


class Response():
    def __init__(self, response=None,
                 request=None,
                 verbose=None,
                 output=None,
                 body_ignore=None):
        self._response = response
        self._request = request
        self._verbose = verbose
        self._output = output
        self._body_ignore = body_ignore

    def handle_response(self):
        if self._verbose:
            response = '> ' + self._request + '\r\n' + '< ' + self._response
            print(response)
            if self._output:
                f = open(self._output, 'w')
                f.write(response)
                f.close()
        if self._output:
            f = open(self._output, 'w')
            f.write(str(self._response.encode("ISO-8859-1")))
            f.close()
        else:
            print(self._response)

    def emit_body(self):
        response = self._response.find(f'\r\n\r\n')
        return response
