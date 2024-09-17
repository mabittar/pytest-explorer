# Multi Stage Python Docker with Poetry and Tests

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/Docker-Multi--stage-informational)
![FastAPI](https://img.shields.io/badge/FastAPI-0.114.0-green)
![Poetry](https://img.shields.io/badge/Poetry-1.8.3-green)
![Pytest](https://img.shields.io/badge/Pytest-8.3.2-green)

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your local machine.
- Python 3.12 if running locally without Docker.

### Building the Docker Image

This project uses a multi-stage Docker build to create a lightweight and efficient Docker image. The main stages are:

1. **Builder Stage**: Installs dependencies using Poetry and creates a virtual environment.
2. **Final Stage**: Copies the virtual environment and application code, and sets up the runtime environment.

#### Multi-Stage Dockerfile Explained

The Dockerfile is structured as follows:

1. **Builder Stage**:
    - Based on `python:3.12.2-slim-bookworm`.
    - Sets up environment variables and installs Poetry.
    - Installs all dependencies into a virtual environment within the `/home/app_user/app` directory.
2. **Final Stage**:
    - Copies the virtual environment from the builder stage.
    - Copies the application code into the image.
    - Configures the container to run the FastAPI app using `uvicorn`.

#### Build the Docker Image

To build the Docker image, run the following command:

```bash
docker build -t fastapi-calculator-api .
```

#### Running the Docker Container

To run the container, use the following command:

```bash
docker run -p 8000:8000 fastapi-calculator-api
```

#### Using with docker-compose

To run the following command, to build the application using docker-compose:

```bash
docker-compose up --build
```

The API will be accessible at `http://localhost:8000`.

## API Endpoints

- GET /docs: Return Swagger with interective documentation
- GET /: Returns the index page.
- GET /health: Health check endpoint.
- POST /api/add/: Adds two numbers.
- POST /api/subtract/: Subtracts the second number from the first.
- POST /api/multiply/: Multiplies two numbers.
- POST /api/divide/: Divides the first number by the second. Returns an error if division by zero is attempted.

## Example Usage

After running the container, you can interact with the API using tools like curl or Postman.

```bash
curl -X POST "http://localhost:8000/api/add/" -H "Content-Type: application/json" -d '{"a": 10, "b": 5}'
```

## Testing

Tests can be executed using pytest. Make sure you installed all test dependencies in the pyproject.toml file.

```shell
pytest
```

Tests also can be executed from docker, using test stage.

```shell
docker build --target test-stage --build-arg TEST_ENV=true -t myapp:test .
```

### Fixtures

#### When use case for fixtures are

- Clients: Database clients, AWS or other cloud clients, API clients which require setup/teardown
- Test Data: Test data in JSON or another format can be easily imported and shared across tests
- Functions: Some commonly used functions can be used as fixtures

#### Available fixture scopes in Pytest

- function: The fixture is created for each test function that uses it and is destroyed at the end of the test function. This is the default scope for fixtures.
- class: The fixture is created once per test class that uses it and is destroyed at the end of the test class.
- module: The fixture is created once per module that uses it and is destroyed at the end of the test session.
- session: The fixture is created once per test session and is destroyed at the end of the test session.
