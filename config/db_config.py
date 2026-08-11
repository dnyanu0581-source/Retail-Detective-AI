import os

import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


def get_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "retail_detective_ai"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", "5433")
        )

        return connection

    except Error as e:
        print(f"Database Connection Error: {e}")
        return None