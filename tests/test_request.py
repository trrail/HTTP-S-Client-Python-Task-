from client import request
from yarl import URL


def test_make_request():
    prepared_request = request.make_request("POST",
                                            URL('https://vk.com/feed'),
                                            {'Host': 'vk.com',
                                             'Connection': 'close'},
                                            'hello, World')
    expected_request = 'POST /feed HTTP/1.1\r\n' \
                       'Host: vk.com\r\n' \
                       'Connection: close\r\n' \
                       'Content-Length: 12\r\n\r\n' \
                       'hello, World'
    assert expected_request == prepared_request


def test_identify_request_type():
    req_type = request.identify_request_type('delete')
    assert req_type == 'DELETE'


def test_prepare_url():
    assert URL('https://vk.com') == request.prepare_url(url='https://vk.com')
    assert URL('https://vk.com') == request.prepare_url(scheme='https',
                                                        host='vk.com',
                                                        path='')


def test_prepare_request():
    req = request.Request.prepare_request(headers={'Host': 'vk.com',
                                                   'Connection': 'close'},
                                          data='hello',
                                          request_type='get',
                                          url='https://vk.com/feed')
    assert req.url == URL('https://vk.com/feed')
    assert len(req.request) > 0
