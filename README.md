# FastAPI Application

This is a FastAPI application that provides a simple API for managing users, posts, and votes. The application uses SQLAlchemy for database interactions and Pydantic for data validation.

## Features

- User registration and authentication
- Create, read, update, and delete posts
- Vote on posts
- Token-based authentication using JWT

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Passlib
- Python-Jose
- Uvicorn

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/fastapi-app.git
    cd fastapi-app
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your environment variables:

    ```env
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=5432
    DATABASE_NAME=fastapi_db
    DATABASE_USERNAME=yourusername
    DATABASE_PASSWORD=yourpassword
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRATON_MINUTES=30
    ```

5. Run the application:

    ```sh
    uvicorn apps.main:app --reload
    ```

6. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

## Project Structure

```
fastapi-app/
├── apps/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
```

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License.