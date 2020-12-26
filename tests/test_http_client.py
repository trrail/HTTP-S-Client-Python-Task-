from client.request import Request
from client.httpclient import HttpClient


def test_do_request():
    http_client = HttpClient()
    request = Request()
    request.set_host('vk.com')
    response = http_client.do_request(request, 1000, 10)
    assert response.code == 200
    assert response.protocol == 1.1
