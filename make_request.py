from request import Request
import argparse
import re


parser = argparse.ArgumentParser(description='HTTP(S) - Client')
parser.add_argument('-d', '--post', type=str, help='post request')
parser.add_argument('-G', '--get', action='store_true', help='get request')
parser.add_argument('http', type=str, help='Contains URL')
parser.add_argument('-e', '--reference', type=str, help='add previous URL')
parser.add_argument('-v', '--verbose', action='store_true', help='detailed response')
parser.add_argument('-f', '--file', type=str, help='send data from file')
parser.add_argument('-c', '--cookie', type=str, help='add cookie')
args = parser.parse_args()
request = Request(args)
request.make_request()
request.do_request()
request.print_answer()
