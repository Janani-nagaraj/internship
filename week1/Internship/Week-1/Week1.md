# Week 1 Lab

## 1. GET with Full Response Headers

### Command

```bash
curl -i https://api.github.com/users/torvalds
```

### Observation

**Status Code:** `200 OK`

### Three Response Headers

* **Content-Type:** Tells us that the response data is in JSON format.
* **Cache-Control:** Gives instructions about how the response can be cached.
* **ETag:** A value used to check whether the resource has changed.

### Response Body

The response body contains information about the GitHub user `torvalds`.

It includes details such as:

* Username
* Name
* GitHub profile URL
* Followers
* Following
* Public repositories

---

## 2. GET with Verbose Output

### Command

```bash
curl -v https://httpbin.org/get
```

### Observation

**Status Code:** `200 OK`

The `-v` option shows detailed information about the connection, request, response, and TLS/HTTPS communication.

### Three Response Headers

* **Content-Type:** Shows that the response is JSON.
* **Content-Length:** Shows the size of the response body.
* **Server:** Shows information about the server handling the request.

### Response Body

The response body contains information about the request.

It includes:

* Request headers
* Request URL
* Origin IP address
* Arguments

---

## 3. POST with a JSON Body

### Command

```bash
curl -i -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name":"your-name","week":1}'
```

### Observation

**Status Code:** `200 OK`

### Three Response Headers

* **Content-Type:** Shows that the response is JSON.
* **Content-Length:** Shows the size of the response.
* **Server:** Shows information about the server.

### Response Body

The JSON data sent in the request was returned by httpbin.

The data appears under the `json` section:

```json
{
  "name": "Jan",
  "week": 1
}
```

This shows that httpbin received and echoed the JSON data.

---

## 4. Query Parameters

### Command

```bash
curl -i "https://httpbin.org/get?role=assosiate&track=Bgc"
```

### Observation

**Status Code:** `200 OK`

### Three Response Headers

* **Content-Type:** Shows that the response is JSON.
* **Content-Length:** Shows the size of the response.
* **Server:** Shows information about the server.

### Response Body

The query parameters are returned under the `args` section.

```json
{
  "role": "assosiate",
  "track": "Bgc"
}
```

So:

* `role` = `assosiate`
* `track` = `Bgc`

---

## 5. Request for a User That Does Not Exist

### Command

```bash
curl -i https://api.github.com/users/this-user-does-not-exist-99999
```

### Observation

**Status Code:** `404 Not Found`

### Three Response Headers

* **Content-Type:** Shows that the response is JSON.
* **Cache-Control:** Gives caching instructions for the response.
* **X-GitHub-Request-Id:** Identifies the GitHub API request.

### Response Body

The response contains an error message indicating that the requested user was not found.

```json
{
  "message": "Not Found"
}
```

The GitHub API returned **404 Not Found** because the requested username does not exist.

---

# Postman Testing

## Call 1 – GET Request

I repeated Call 1 using Postman.

**URL:**

```text
https://api.github.com/users/torvalds
```

**Method:** GET

**Status Code:** `200 OK`

The response was successful and contained the same GitHub user information as the cURL request.

---

## Call 3 – POST Request

I repeated Call 3 using Postman.

**URL:**

```text
https://httpbin.org/post
```

**Method:** POST

**Header:**

```text
Content-Type: application/json
```

**Body:**

```json
{
  "name": "Jan",
  "week": 1
}
```

**Status Code:** `200 OK`
