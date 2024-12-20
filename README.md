# AwardsBot

## Requirements

- Docker
- Docker Compose

---

## Installation and Run

### Step 1: Preparation

1. Provide a `.env` file in the `ops` folder with the required environment variables. Use the example file provided in the repository as a reference.

### Step 2: Build and Run Containers

1. Build the containers:
    ```bash
    docker compose build
    ```

2. Start the application:
    ```bash
    docker compose up
    ```

---

## Access

- The main API will be available at:
  ```
  http://localhost:8000
  ```

- API documentation will be available at:
  ```
  http://localhost:8000/docs
  ```

- The admin panel will be available at:
  ```
  http://localhost:8000/admin
  ```
