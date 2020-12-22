from client.response import Response
from client.request import Request
from client.httpclient import HttpClient
import pytest


@pytest.fixture()
def data() -> bytearray:
    request = Request.prepare_request(headers={'Host': 'vk.com',
                                               'Connection': 'close'},
                                      data='hello',
                                      request_type='post',
                                      url='https://vk.com/feed')
    http_client = HttpClient(request, 1000)
    http_client.do_request()
    return http_client.response


def test_prepare_response_fields(data):
    response = Response.prepare_fields(data)
    assert response.code == 302
    assert response.location == 'https://login.vk.com/'
    assert response.charset == 'windows-1251'
    assert response.protocol == 1.1
