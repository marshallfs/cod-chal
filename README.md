# cod-chal
Coding Challenge, use of APIs and endpoints for queries

# FastAPI Application

This is a FastAPI application that provides APIs for uploading CSV files and inserting data into a MySQL database.

## Features

- **Upload CSV files**: The `/upload` endpoint accepts a CSV file, reads the data, and inserts it into a MySQL table. The table name is determined by the filename of the uploaded file.
- **Batch Insert**: The `/batch_insert/{table_destination}` endpoint accepts a list of dictionaries and a table name. The data is converted into a DataFrame and then inserted into the specified table in the MySQL database.
- **Metrics Endpoints**: The application includes several endpoints (`/metrics1-json/{year}`, `/metrics2-json/{year}`, `/metrics1-tab/{year}`, and `/metrics2-json/{year}`) that execute SQL queries on the MySQL database to retrieve some metrics related to the 'hired_employees', 'departments', and 'jobs' tables.

## Installation

1. Clone this repository.
2. Create a `.env` file in the root directory of your project and add your database parameters:

    ```plaintext
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_NAME=your_database_name
    ```

3. Install the required Python packages: `pip install -r requirements.txt`
4. Run the FastAPI application: `uvicorn main:app --host 0.0.0.0 --port 8000`

## Docker

This application can be dockerized. A Dockerfile is included in the repository.

To build the Docker image, run: `docker build -t coding_challenge .`

To run the Docker container, run: `docker run -p 8000:8000 coding_challenge`

## Testing

Automated tests for the `upload` and `batch_insert` endpoints are included in the `coding_challenge_test.py` file. You can run the tests using pytest: `pytest coding_challenge_test.py`

The tests include:

- Uploading CSV files for 'departments', 'jobs', and 'hired_employees'.
- Batch inserting data into 'departments', 'jobs', and 'hired_employees'.
- Retrieving metrics in JSON format.
- Retrieving metrics in CSV format.

## Usage

Here's a guide on how to use each endpoint in this FastAPI application:

1. **Upload CSV files (`/upload` endpoint)**: This is a POST request that accepts a CSV file. The data from the file is inserted into a MySQL table. The table name is determined by the filename of the uploaded file. Here's an example of how to use it with `curl`:

    ```bash
    curl -X POST -F "file=@/path/to/your/file.csv" http://localhost:8000/upload
    ```

2. **Batch Insert (`/batch_insert/{table_destination}` endpoint)**: This is a POST request that accepts a list of dictionaries and a table name. The data is converted into a DataFrame and then inserted into the specified table in the MySQL database. Here's an example of how to use it with `curl`:

    ```bash
    curl -X POST -H "Content-Type: application/json" -d '[{"id": 1, "department": "test"}]' http://localhost:8000/batch_insert/departments
    ```

3. **Retrieve Metrics in JSON format (`/metrics1-json/{year}` and `/metrics2-json/{year}` endpoints)**: These are GET requests that accept a year as a path parameter. They execute SQL queries on the MySQL database to retrieve some metrics related to the 'hired_employees', 'departments', and 'jobs' tables. Here's an example of how to use them with `curl`:

    ```bash
    curl http://localhost:8000/metrics1-json/2021
    curl http://localhost:8000/metrics2-json/2021
    ```

4. **Retrieve Metrics in CSV format (`/metrics1-tab/{year}` and `/metrics2-tab/{year}` endpoints)**: These are GET requests that accept a year as a path parameter. They execute SQL queries on the MySQL database to retrieve some metrics related to the 'hired_employees', 'departments', and 'jobs' tables. The results are returned as a CSV file. Here's an example of how to use them with `curl`:

    ```bash
    curl http://localhost:8000/metrics1-tab/2021
    curl http://localhost:8000/metrics2-tab/2021
    ```

You can also use a client like Postman to use the endpoints.    

Please replace `localhost:8000` with the actual host and port where your FastAPI application is running, and replace `/path/to/your/file.csv` with the actual path to your CSV file.