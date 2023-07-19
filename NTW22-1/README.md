# HTTP Server

**HTTP server running over TCP IPv4**

**Assignment 1** for **[Computer Networking](https://search.usi.ch/en/courses/35263648/computer-networking)**
course during the Spring Semester 2022 @ [USI Università della Svizzera italiana](https://www.usi.ch).

* Aristeidis Vrazitoulis: [vrazia@usi.ch](mailto:vrazia@usi.ch)
* Marina Papageorgiou: [papagm@usi.ch](mailto:papagm@usi.ch)
* Diego Barreiro Perez: [barred@usi.ch](mailto:barred@usi.ch)

## Usage Instructions

This code has been written in **`Python 3.9`**, so it is guaranteed that no errors will appear there.
However, lower Python versions may work properly.

### Installation

No specific installation instructions are required. Just install a **`Python 3`** version.

### Running

To get the server up and running, just run the following command:

```bash
python server.py
```

By default, it will be running at port `8080`, but it can be changed with the respective flag.
All options are listed here:

```bash
PS C:\Github\NTW22-1> python server.py --help
usage: server.py [-h] [-p [PORT]]

HTTP server based on TCP IPv4 with multithreading support.

optional arguments:
  -h, --help            show this help message and exit
  -p [PORT], --port [PORT]
                        port to use to listen connections
PS C:\Github\NTW22-1>
```

## Tasks

WIP: How job was split. We used git for project management with Github issues, branches and other
stuff as if it were a software engineering project.

|                    | **Aristeidis** | **Marina** | **Diego** |
|:-------------------|:--------------:|:----------:|:---------:|
| Task A             |                |            |     ●     |
| Task B             |       ●        |     ●      |     ●     |
| Task C             |       ●        |            |           |
| Task D             |                |     ●      |           |
| Task E             |       ●        |            |           |
| Task F             |                |     ●      |           |
| Task G             |       ●        |     ●      |           |
| Task H             |                |            |     ●     |
| Task I             |       ●        |     ●      |     ●     |
| Task J             |       ●        |     ●      |     ●     |
| _Optional Task A_  |                |            |     ●     |
| _Optional Task B_  |                |            |     ●     |

### Project Structure

WIP: Websites folder, http module, utils and server and settings.

### HTTP Implementation

WIP: Object oriented programming, based on Django. HttpRequest and HttpResponse. Internal process workflow:
from getting raw socket data to sending raw socket data. Parsing and entity file (custom error content).

#### GET

Since Server receives the request and checks its structure for basic validity,
then proceeds for further checking. After inspecting the first line of the request
and ensures that is a GET method then we check for the file path existence in the server's
filesystem. If the requested file exists then we append its content to the body of the HTTP response
and add the required headers to the HTTP response and 200 as status code. In every other case, we raise the corresponding exception with the corresponding status code and we attach that in the HTTP response.

More specifically:
-If file does not exist: 404 NOT FOUND
In that case we make a special response with a body of the contents of the file 404.html 

-If user does not have permission to access the file: 403 FORBIDDEN
-If the requested resource is not a file: 405 METHOD NOT ALLOWED
#  If the file is   UnsupportedMediaType??



#### PUT
In the PUT method the user gives a path as an input. Then it is happening a check with try - exception with the following conditions:
- if the input path contains at the end "/", it means that is not a file but it is a directory, so it prints the error 405 (HttpMethodNotAllowed)
- If the input path exists then the server opens the file of that path and writes in it. 
- If the input path does not exist then the server creats this path and this file and additionally, it prints the error 403     (HttpResponseForbidden).

// Explain procedure regarding the implementation, logic behind it, assumptions taken, extra features, etc. Finish
// with a list of possible response codes, and their trigger case.

#### DELETE

For the HTTP DELETE method we check first for the file existence. If the file exists then we delete it from the file system
and then check if the folder is empty to remove it as well. Then we recursively check if the parent is empty so as to delete it.
After this procedure, we return a response with the suitable headers and status code 200 OK. Otherwise we raise an exception

-If file does not exist: 404 NOT FOUND
-If user does not have permission to access the file: 403 FORBIDDEN
-If the requested resource is not a file: 405 METHOD NOT ALLOWED


#### NTW22INFO
In this method (NTW22INFO) the client is giving as an input: 
                                      "NTW22INFO / HTTP/1.0
                                      Host: gyuincognito.ch"

The server answers automatically: "HTTP/1.0 200 OK
                                      Date: Wed, 24 Mar 2021 09:30:00 GMT
                                      Server: Guy incognito's Server
                                      Content-Length: 98
                                      Content-Type: text/plain"   
So my job is to write up to this input and the automatic server's answer the following answer: 
                                      "The administrator of guyncognito.ch is Guy incognito.
                                      The on contact him at guy.incognito@usi.ch"                                

// Explain procedure regarding the implementation, logic behind it, assumptions taken, extra features, etc. Finish
// with a list of possible response codes, and their trigger case.
// Mention as well that we also support other paths apart from just /.

## Acknowledgments

- Django
- StackOverflow question about multithread
- RFC's
- TA notes
