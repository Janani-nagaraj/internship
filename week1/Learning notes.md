# Week 1 Learning Notes

**1. What is WSL and how is it related to Linux?**

WSL stands for Windows Subsystem for Linux.

-> It is a feature of Windows that allows us to use a Linux environment inside Windows.

-> We can install Linux distributions like Ubuntu and use Linux commands through WSL.

**2. What is the difference between Linux and Unix?**

Linux

-> Open-source operating system.

-> Linux is Unix-like, but it is not Unix itself.

Unix

-> Older family of operating systems.

-> Linux was created later and follows many Unix concepts.

**3. What is an IP address?**

-> An IP address is like an address for a device or network.

-> It helps devices identify each other and communicate over a network.

Public IP

-> Used to communicate with the Internet.

-> Identifies our network to the outside world.

Private IP

-> Used inside a local network like Wi-Fi.

-> Identifies a device inside that network.

Internet → Public IP → Router → Private IP → Laptop/Phone

**4. What is a Web Server and Application Server?**

Web Server

-> Receives web requests from users and sends responses.

-> Example: Nginx.

Application Server

-> Runs the application's code and logic.

-> Example: Uvicorn can run a Python FastAPI application.

Example:

User → Nginx → Uvicorn + FastAPI → Response

**5. What is Open Source?**

-> Open-source software has source code that is available for people to view, modify and share according to its license.

**6. Is Open Source always free?**

-> Not always.

-> The software may be free to use, but services like hosting, support or extra features may cost money.

**7. Does "free" always mean money?**

-> No.

-> Free can also mean freedom to use, modify and share software according to its license.

**8. What is ORM and Hibernate in Java?**

ORM stands for Object Relational Mapping.

-> ORM connects objects in a program with tables in a database.

-> Hibernate is a popular ORM framework used in Java.

**9. What is the equivalent of ORM in Python?**

-> SQLAlchemy and Django ORM are commonly used for ORM in Python.

**10. What is CRUD and how is it related to HTTP?**

CRUD means:

-> Create

-> Read

-> Update

-> Delete

These are commonly mapped to HTTP methods:

Create → POST

Read → GET

Update → PUT/PATCH

Delete → DELETE

**11. What is an API?**

-> API allows different software applications to communicate with each other.

Example:

Application → API → Server

**12. What is a Web API and how is it related to HTTP?**

-> A Web API allows applications to communicate over the web.

-> It usually uses HTTP to send requests and receive responses.

Example:

Application → HTTP Request → Web API → HTTP Response → Application

HTTP = Rules for communication

API = Allows software to communicate

Web API = Allows software to communicate over the web
