2. FastAPI – First Run

FastAPI is a Python framework used to build APIs. We first create a virtual environment and install FastAPI. Then we create a FastAPI() application and define routes such as @app.get("/"). We run the application using Uvicorn, and the API becomes available on a local address such as http://127.0.0.1:8000. The --reload option automatically restarts the server whenever we make changes to the code.

3. Decorator

A decorator adds extra behaviour to a function without changing the function's actual code. In FastAPI, @app.get("/") tells FastAPI that the root() function should handle a GET request to /. So when a client sends a GET request to /, FastAPI calls the root() function.

4. Swagger UI and OpenAPI

FastAPI automatically provides an interactive API documentation page at /docs. This page is called Swagger UI, and we can use it to test our API directly from the browser. OpenAPI is the specification that describes the API, including routes, parameters, and responses. FastAPI automatically generates this information at /openapi.json, and Swagger UI uses it to display the API in an interactive way.

5. APIRouter

APIRouter helps us organise a large FastAPI project. Instead of putting every route inside app.py, we can create a separate file such as tasks.py and put all task-related routes there. We create an APIRouter, define the routes using it, and then connect it to the main application using app.include_router(router). This keeps the project clean and organised.

6. Routes

A route tells FastAPI which function should run when a particular HTTP request is received. For example, @app.get("/tasks") means that the function below it handles a GET request to /tasks. Different HTTP methods such as GET, POST, PUT, and DELETE are used for different operations in a CRUD API.

7. Path Parameters

A path parameter is a value that is directly included in the URL. For example, /tasks/{task_id} contains task_id as a path parameter. If we request /tasks/7, FastAPI takes 7 and passes it to the function. If we define it as task_id: int, FastAPI also checks that the value is an integer.

8. Query Parameters

A query parameter is placed after ? in the URL. It is generally used for filtering or controlling the returned data. For example, /tasks?done=true&limit=5 uses done and limit as query parameters. Query parameters can have default values, which makes them optional.

9. Request Bodies with Pydantic

A Pydantic model defines the structure of JSON data that the API accepts. For example, a TaskIn model can require a title as a string and have done as a Boolean with a default value of False. FastAPI automatically reads the request body and validates it against the Pydantic model before passing it to the function.

10. 422 Validation Error

If the client sends data that does not match the Pydantic model, FastAPI automatically returns a 422 Unprocessable Entity response. For example, if the required title field is missing or has an invalid type, FastAPI tells us which field has the problem and why. We don't need to manually write this validation logic.

11. Status Codes and Errors

HTTP status codes tell the client what happened to its request. In a CRUD API, 201 means a resource was successfully created, 204 means the operation succeeded but there is no response body, 404 means the requested resource does not exist, and 422 means the request body failed validation. FastAPI allows us to manually return errors using HTTPException.

12. HTTPException

HTTPException is used when we want FastAPI to return a specific error response. For example, when a user requests /tasks/7 but task 7 does not exist, we can raise HTTPException(status_code=404, detail="task not found"). FastAPI then sends a proper 404 response to the client.

13. Storing Data

At first, we can store our API data in a simple Python dictionary instead of using a database. For example, _tasks can store tasks using their IDs. Functions such as save(), find(), and all_tasks() can be used to save, find, and return tasks. This lets us make the API work before introducing a real database.

14. Separation of Concerns

Separation of Concerns means each part of the application should have one clear responsibility. The routes should deal with HTTP requests, while the storage layer should deal with storing and retrieving data. Because these responsibilities are separated, we can replace the dictionary with a real database later without changing the routes.

15. Dependency Injection

Dependency Injection means giving a function the object or resource it needs from outside instead of creating it inside the function. In FastAPI, Depends() is used for this. For example, db = Depends(get_db) tells FastAPI to call get_db() and provide the result to the route. This makes the code easier to test and change.

16. SQL

SQL is the language used to communicate with a relational database. The main CRUD SQL commands are INSERT for creating data, SELECT for reading data, UPDATE for changing data, and DELETE for removing data. These commands allow our FastAPI application to store and manage information in a database.

17. Primary Key

A primary key is a value that uniquely identifies each row in a database table. For example, in a tasks table, the id column can be the primary key. This means two tasks should not have the same ID.

18. Foreign Key

A foreign key is used to connect data between two database tables. For example, a comments table can contain a task_id that refers to the id of a task in the tasks table. This creates a relationship between the two tables.

19. SQLite

SQLite is a lightweight database that Python can use directly through its built-in sqlite3 module. Instead of running a separate database server, SQLite stores the database in a file such as app.db. We can create tables and execute SQL commands directly from Python.

20. Parameterised Queries

When sending values to SQL, we should use parameterised queries instead of putting Python variables directly into an SQL string. In SQLite, we use ? as a placeholder and pass the actual value separately. This keeps user input separate from the SQL command and prevents dangerous SQL from being inserted into the query.

21. SQL Injection

SQL injection is a security attack where a malicious user tries to insert SQL commands through an input field. For example, directly putting user input into an f-string SQL query can allow someone to manipulate the query. Using parameterised queries with placeholders such as ? prevents this problem because the database treats the value as data instead of SQL code.

22. SQLite to PostgreSQL

PostgreSQL is a more powerful relational database that can be used when the application grows. The application can use a DATABASE_URL environment variable to store the PostgreSQL connection details. This means the database configuration stays outside the Python code and can easily be changed between environments.

23. ORM

An ORM (Object-Relational Mapper) allows us to work with database data using Python objects instead of writing SQL for every operation. In Python, SQLAlchemy is a common ORM, and SQLModel combines ideas from SQLAlchemy and Pydantic. The ORM converts operations on Python objects into SQL queries that the database understands.

24. CORS

CORS (Cross-Origin Resource Sharing) controls whether a browser is allowed to make requests from one origin to another. For example, if your frontend runs on localhost:3000 and your FastAPI backend runs on localhost:8000, you need to configure CORS to allow the frontend to call the backend. CORS is a browser rule, so tools such as Postman and curl are not affected by it.

25. Environment Variables

Environment variables are used to store configuration values outside the Python source code. Things such as database URLs, ports, secrets, and debug settings should not normally be hardcoded. Python can read environment variables using os.getenv(). During local development, these values can also be kept in a .env file that is excluded from Git.

26. Pydantic Settings

Pydantic Settings provides a structured way to read configuration from environment variables. We can create a Settings class containing values such as database_url and debug. Pydantic then validates these values when the application starts. This is useful when a project has several configuration settings because incorrect values can be detected early
