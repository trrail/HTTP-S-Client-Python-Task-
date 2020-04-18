
# HTTP(S) - Client 

## Program can:
* Send post request and get answer
* Send get request and get answer
* Send data from file by post request
* Save answer in file
* You can add: cookie, user-agent, headers and reference 
  
## How it works:
* You should print in terminal: python make_request.py url args

| Argument |                 Action              |                               Example                            | 
|----------|-------------------------------------|------------------------------------------------------------------|
|    -d    |       Send data by POST request     | -d "Hello, World!"                                               |
|    -f    | Send data from file by POST request | -f "test.txt"                                                    |
|    -e    |       Add reference in request      | -e "https://github.com/trrail/python-tasks/edit/master/README.md"|
|    -O    |         Write answer in file        | -O "test.txt"                                                    |
|    -A    |       Add User-Agent in request     | -A "Mozilla/5.0"                                                 |
|    -c    |         Add cookie in request       | -c "income=1"                                                    |
|    -H    |         Add headers(Split by $)     | -H "Accept: */*$Authorization: Basic YWxhZGRpbjpvcGVuc2VzYW1l"   |                                  |
