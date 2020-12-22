import pytest
import argparse
from client import prepare
import os


@pytest.fixture()
def parser():
    parser = argparse.ArgumentParser(description="HTTP(S) - Client")
    parser.add_argument("-d", "--data", type=str, help="data for request")
    parser.add_argument(
        "-r",
        "--request",
        type=str,
        help="choose request method:"
             "GET|"
             "POST|"
             "PUT|"
             "CONNECT|"
             "PATCH|"
             "OPTIONS|"
             "DELETE|"
             "HEAD|"
             "TRACE",
    )
    parser.add_argument("-u", "--url", type=str, help="Contains URL")
    parser.add_argument("-e", "--reference", type=str, help="add previous URL")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="detailed response")
    parser.add_argument("-f", "--file", type=str, help="send data from file")
    parser.add_argument("-c", "--cookie", type=str, help="add cookie")
    parser.add_argument("-C", "--cookiefile", type=str,
                        help="send cookie from file")
    parser.add_argument("-A", "--agent", type=str,
                        help="add your own User_Agent")
    parser.add_argument("-O", "--output", type=str,
                        help="print answer in file")
    parser.add_argument(
        "-H",
        "--headers",
        type=str,
        nargs="+",
        help="add headers in request",
        dest="my_headers",
    )
    parser.add_argument(
        "-0", "--bodyignore", action="store_true",
        help="ignore body of response"
    )
    parser.add_argument(
        "-1", "--headignore", action="store_true",
        help="ignore head of response"
    )
    parser.add_argument("-t", "--timeout", type=str, help="reset timeout")
    parser.add_argument("-l", "--host", type=str,
                        help="custom host, default value is None")
    parser.add_argument("-s", "--scheme", type=str,
                        help="setup scheme, default is http")
    parser.add_argument(
        "-P",
        "--path",
        type=str,
        help="setup path, should start with </>, haven't default path",
    )
    return parser


def test_prepare_headers(parser):
    args = parser.parse_args(['-u', 'https://vk.com',
                              '-e', 'https://vk.com/feed',
                              '-c', 'qwerty',
                              '-A', 'Yandex',
                              '-H', 'qwerty: 1', 'asdfg: 2'])
    expected_dict = {'Host': 'vk.com',
                     'Connection': 'close',
                     'qwerty': '1',
                     'asdfg': '2',
                     'Reference': 'https://vk.com/feed',
                     'Cookie': 'qwerty',
                     'User-Agent': 'Yandex'}
    real_dict = prepare.prepare_headers(args)
    for header in expected_dict.keys():
        assert real_dict.get(header) == expected_dict.get(header)


def test_cookie_from_file_to_headers(parser):
    with open("cookie.txt", 'w') as file:
        file.write('qwerty')
    args = parser.parse_args(['-u', 'https://vk.com',
                              '-C', 'cookie.txt'])
    expected_dict = {'Host': 'vk.com',
                     'Connection': 'close',
                     'Cookie': 'qwerty'}
    real_dict = prepare.prepare_headers(args)
    for header in expected_dict.keys():
        assert real_dict.get(header) == expected_dict.get(header)
    os.remove('cookie.txt')


def test_prepare_data(parser):
    args = parser.parse_args(['-d', 'Hello, world'])
    expected_data = 'Hello, world'
    data = prepare.prepare_data(args)
    assert data == expected_data
    with open('hello_world.txt', 'w') as file:
        file.write('Hello, world')
    args = parser.parse_args(['-f', 'hello_world.txt'])
    data = prepare.prepare_data(args)
    assert data == expected_data
    os.remove('hello_world.txt')
