
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
|    -d    |            Set data                 | -d "Hello, World!"                                               |
|    -f    |         Set data from file          | -f "test.txt"                                                    |
|    -e    |       Add reference in request      | -e "https://github.com/trrail/python-tasks/edit/master/README.md"|
|    -O    |         Write response in file      | -O "test.txt                                                     |
|    -A    |       Add User-Agent in request     | -A "Mozilla/5.0"                                                 |
|    -c    |         Add cookie in request       | -c "income=1"                                                    |
|    -H    |         Add headers(Split by $)     | -H "Accept: */* Authorization: YWxhZGRpbjpvcGVuc2VzYW1l"         |                            
|    -v    |        Print request + response     | -v                                                               |
|    -C    |         Add cookie from file        | -c "cookie.txt"                                                  |
|    -m    |         Choose request method       | -m POST|PUNCH|CONNECT|DELETE|OPTION|PUT| etc                     |
|    -0    |         Ignore body of response     | -0                                                               |
|    -1    |         Ignore head of response     | -1                                                               |
|    -t    |            Set timeout              | -t 3000                                                          |
|    -u    |              Set URL                | -m https://vk.com/feed                                           |
|    -l    |              Set host               | -l youtube.com                                                   |
|    -s    |             Set scheme              | -s http                                                          |
|    -P    |              Set path               | -P /feed                                                         |

## Developer
  Was created by Meshcheryakov G.

