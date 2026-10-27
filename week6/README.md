# Document Verification API

A FastAPI application for document verification using OCR, MinIO object storage, and PDF reports.

## Features

- Document verification using OCR
- MinIO object storage
- PDF report generation
- Docker containerization
- Non-root application user

## Build the Docker Image

```powershell
docker build -t jananinagaraj/document-verification-api:1.0 .
```

## Test the API

```powershell
curl.exe http://localhost:8002/
```

Open the API documentation in your browser:

http://localhost:8002/docs

## Docker Commands

List running containers:

```powershell
docker ps
```

View API logs:

```powershell
docker logs document-api-test
```

Open a shell inside the API container:

```powershell
docker exec -it document-api-test sh
```

Check the application user inside the container:

```sh
whoami
```

## Containers and Networking

The project uses Docker containers for the API, MinIO object storage, and PostgreSQL.

- API container: `document-api-test`
- MinIO container: `minio`
- PostgreSQL container: `capstone-db`
- Docker network: `capstone-net`

Containers communicate over the Docker network using container names.

## PostgreSQL Volume Persistence

The PostgreSQL container uses the named volume `postgres_data` to preserve database files when the container is recreated.

Check volumes:

```powershell
docker volume ls
```

Check the test record:

```powershell
docker exec -it capstone-db psql -U capstoneuser -d capstone_db -c "SELECT * FROM docker_persistence_test;"
```

## Docker Hub

Docker image:

`jananinagaraj/document-verification-api:1.0`

Pull the image:

```powershell
docker pull jananinagaraj/document-verification-api:1.0
```

## Technologies Used

- Python
- FastAPI
- Tesseract OCR
- MinIO
- PostgreSQL
- Docker

```
