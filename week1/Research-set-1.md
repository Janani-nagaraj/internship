# Web Application Basics

**1. What is HTTP protocol?**

HTTP stands for HyperText Transfer Protocol. It is a protocol used for communication between a client and a server.

Example: A browser sends a request to a server, and the server sends a response back.

**2. What is a web application?**

A web application is a software application that we use through a web browser.

Examples: Gmail, Instagram, Amazon, Google Docs.

**3. What is a web server?**

A web server receives HTTP requests from clients and sends HTTP responses back.

Examples: Apache, Nginx, IIS.

**4. What is HTTPS and why is it secure?**

HTTPS stands for HyperText Transfer Protocol Secure. It is the secure version of HTTP and uses TLS to encrypt communication between the client and server.

HTTPS provides:

* Encryption
* Data integrity
* Server authentication

**5. What is authentication and authorization?**

Authentication means checking who the user is.

Example: Logging in using an email and password.

Authorization means checking what the user is allowed to do.

Example: An admin can delete users, but a normal user cannot.


**6. How does social login work?**

Social login allows us to log in to an application using an existing account like Google.

Example:

Application → Google Login → Google verifies the user → Google gives the application a token/identity information → User is logged in.

The application does not need to receive the user's Google password.

**7. What is synchronous and asynchronous communication?**

Synchronous communication means the application waits for the response before continuing.

Example:

App → Request → Server → Response → App continues

Asynchronous communication means the application can continue doing other work while waiting for the response.

Example:

App → Request → Server

App continues doing other work


**8. What is REST?**

REST stands for Representational State Transfer.

REST is an architectural style used for designing web APIs. It uses HTTP methods to work with resources.

Common HTTP methods:

* GET → Read data
* POST → Create data
* PUT → Replace data
* PATCH → Update part of data
* DELETE → Delete data

