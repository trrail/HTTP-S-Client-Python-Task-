
# HTTP(S) - Client 

## Program can:
* Send POST requests and get answer
* Send GET requests and get answer
* Send data from file by post request
* Save answer in file
* You can add: cookie, user-agent, headers and reference 
-----------------------------------------------------------------------------------------------------------------------------------  
## How it works:
* You should print in terminal: python main.py url args
-----------------------------------------------------------------------------------------------------------------------------------

| Argument |                 Action              |                               Using Examples                     | 
|----------|-------------------------------------|------------------------------------------------------------------|
|    -d    |            Send data                | -d "Hello, World!"                                               |
|    -f    |         Send data from file         | -f "test.txt"                                                    |
|    -e    |       Add reference in request      | -e "https://github.com/trrail/python-tasks/edit/master/README.md"|
|    -O    |         Write answer in file        | -O "test.txt"   (function is temporarily unavailable)            |
|    -A    |       Add User-Agent in request     | -A "Mozilla/5.0"                                                 |
|    -c    |         Add cookie in request       | -c "income=1"                                                    |
|    -H    |         Add headers(Split by $)     | -H "Accept: */* Authorization: YWxhZGRpbjpvcGVuc2VzYW1l"         |                            
|    -v    |        Print request + answer       | -v                                                               |
|    -C    |         Add cookie from file        | -c "cookie.txt"                                                  |
|    -r    |         Choose request method       | -r "POST|PUNCH|CONNECT|DELETE|OPTION|PUT| etc"                   |
|    -0    |         Ignore body of response     | -0                                                               |
|    -1    |         Ignore head of response     | -1                                                               |
|    -t    |            Set timeout              | -t 3000                                                          |

## Developer
  Was created by Meshcheryakov G. known as trrail

