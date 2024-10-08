def test_add_question(client):
    # Simulate adding a question with a POST request
    response = client.post(
        "/questions",
        json={
            "question": "What is the capital of France?",
            "answer": "Paris",
            "choices": ["Paris", "Berlin", "Madrid", "Rome"],
            "level": "grade1",
            "difficulty": "easy",
            "category": "geography",
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Question added successfully"


def test_add_question_invalid_data(client):
    # Test missing fields in the request data
    response = client.post(
        "/questions",
        json={
            "question": "What is the capital of France?",
            "answer": "Paris",
            "choices": ["Paris", "Berlin", "Madrid", "Rome"],
            "difficulty": "easy",
            "category": "geography",
        },
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Missing fields in the request"


def test_get_random_question(client):
    # Add a question first
    client.post(
        "/questions",
        json={
            "question": "What is the capital of France?",
            "answer": "Paris",
            "choices": ["Paris", "Berlin", "Madrid", "Rome"],
            "level": "grade1",
            "difficulty": "easy",
            "category": "geography",
        },
    )

    # Now test fetching a random question
    response = client.get("/questions")
    assert response.status_code == 200
    data = response.get_json()
    assert data["question"] == "What is the capital of France?"
    assert len(data["choices"]) == 4
    assert "Paris" in data["choices"]


def test_get_question_no_match(client):
    # Test fetching a question when no match is found
    response = client.get("/questions?level=grade5")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "No question found"
