from client.request import Request
from client.httpclient import HttpClient


def test_do_request():
    request = Request.prepare_request(headers={'Host': 'vk.com',
                                               'Connection': 'close'},
                                      data='',
                                      request_type='get',
                                      url='https://vk.com/feed')
    http_client = HttpClient(request, 1000)
    http_client.do_request()
    assert len(http_client.response) > 0
