Client–Server Model

The web works on a simple request–response cycle.
 A client sends an HTTP request.
 A server receives the request, processes it, and sends back an HTTP response.
The client always initiates the communication; the server only responds.

What is a Client?

A client is any application or device that can send HTTP requests to a server.

Examples:

Browser (Chrome, Firefox):Requests web pages and displays them.
curl: Sends HTTP requests from the command line and prints the raw response.
Postman: A GUI tool for testing and inspecting HTTP requests and responses.
Mobile App:Communicates with its backend server to fetch or send data (e.g., Instagram loading your feed).
Although these clients look different, they all perform the same job: sending HTTP requests

The Shape of a Real System

In a real system, a request usually does not go directly from the client to one server. It passes through different components like DNS, load balancer, app servers, database and object storage.

DNS converts a domain name into an IP address. For example, `api.example.com` can be converted into an IP address like `93.184.216.34`.
After DNS, the request reaches the load balancer. The load balancer is the main entry point for the application. It receives requests and sends them to one of the available app servers. If one server is not working, the load balancer stops sending requests to that server.

App servers run the actual application code. There can be multiple app servers, and they are usually identical. This helps the system handle more users and requests.

The database is used to store structured information such as users, products and orders. Data is usually stored in tables containing rows and columns.

Object storage is used for storing large files such as images, videos, documents and backups. Examples are Amazon S3 and Azure Blob Storage.

**HTTP, Line by Line**

HTTP is the language used by clients and servers to communicate. The client sends a request and the server sends a response.

Request
An HTTP request has a request line, headers and an optional body.

text
POST /api/users HTTP/1.1
Host: example.com
Content-Type: application/json


The request line contains the method, path and HTTP version. Headers contain extra information about the request. The body contains the data being sent.

**Response**
A response contains a status line, headers and an optional body.

text
HTTP/1.1 201 Created
Content-Type: application/json
The status code tells what happened. `201 Created` means the resource was successfully created.

**Stateless**

HTTP is stateless, which means the server does not automatically remember previous requests. Each request must contain the information needed to process it.

**HTTP Methods**

HTTP methods tell the server what action the client wants to perform.

**GET**

Used to read or get data. It does not change the server.

Example: Get user details.

**POST**

Used to create new data or perform an action.

Example: Create a new user.

**PUT**

Used to replace an entire resource.

Example: Replace all details of a user.

**PATCH**

Used to update only part of a resource.

Example: Change only the user's email.

**DELETE**

Used to remove data.

Example: Delete a user.

**HEAD / OPTIONS**

`HEAD` gets only the headers without the response body. `OPTIONS` asks the server what methods or actions are allowed.

**Safe**

A safe method does not modify data on the server. `GET`, `HEAD`, and `OPTIONS` are safe.

**Idempotent**

Idempotent means performing the same request multiple times has the same final effect as performing it once.

For example, deleting user 42 five times still results in user 42 being deleted. `POST` is not idempotent because sending the same create request five times can create five resources.

**URLs: Path vs Query**

A URL tells the client where to send a request and what information is needed.

Example:
text
https://api.example.com/users/42/orders?status=open&limit=10

**Path**

The path identifies which resource we want.

text
/users/42/orders
42 is a path parameter and represents a specific user.

**Query**

The query comes after `?` and is used to filter or control the result.
text
?status=open&limit=10
status=open` filters for open orders and `limit=10` asks for only 10 results.

**HTTPS and TLS**

HTTPS is HTTP with security provided by TLS.

TLS provides three main things:

* **Confidentiality** – encrypts data so others cannot read it.
* **Integrity** – prevents data from being secretly changed.
* **Authentication** – helps confirm that we are talking to the real website.

A **certificate** is used to prove the website's identity and is verified by a trusted Certificate Authority (CA).

**TLS Handshake**

Before communication starts, the client and server establish a secure connection and a shared secret key. After that, the data is encrypted.
**Ports**

A port is a number used to identify a specific service running on a computer.

The **IP address** identifies the computer, while the **port number** identifies the service.

Example:

text
192.168.1.10:443

192.168.1.10 → Computer

443 → HTTPS service

Common ports:

* 80 → HTTP
* 443 → HTTPS
* 22 → SSH
* 3306 → MySQL
* 5432 → PostgreSQL
