import pytest
from mongomock import MongoClient

from app.app import create_app


@pytest.fixture(scope="module")
def app():
    """
    This fixture creates a Flask app configured for testing.
    It mocks MongoDB using mongomock for in-memory MongoDB operations.
    """
    # Create a mock MongoDB client using mongomock
    client = MongoClient()
    db = client["test_quiz_db"]  # Use an in-memory MongoDB database for testing

    # Pass the mock MongoDB client and database to the Flask app
    app = create_app(test_config={"client": client, "db": db})
    app.config["TESTING"] = True  # Set Flask to testing mode
    return app


@pytest.fixture(scope="module")
def client(app):
    """
    This fixture provides a Flask test client that can be used to simulate requests to the app.
    """
    return app.test_client()


@pytest.fixture(scope="module")
def init_db(app):
    """
    A fixture that can be used to initialize the mock database if needed.
    This is useful for inserting mock data before running tests.
    """
    with app.app_context():
        # Access the mock MongoDB database and insert sample data if necessary
        db = app.config["db"]
        questions_collection = db["questions"]
        # Add any required initial data
        questions_collection.insert_one(
            {
                "question": "What is the capital of France?",
                "answer": "Paris",
                "choices": ["Paris", "Berlin", "Madrid", "Rome"],
                "level": "grade1",
                "difficulty": "easy",
                "category": "geography",
            }
        )
        yield db
