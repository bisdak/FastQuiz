import io

import pandas as pd


def test_upload_questions(client):
    # Create a mock Excel file in memory
    data = {
        "question": ["What is the capital of France?", "What is 2 + 2?"],
        "answer": ["Paris", "4"],
        "choices": ["Paris,Berlin,Madrid,Rome", "3,4,5,6"],
        "level": ["grade1", "grade1"],
        "difficulty": ["easy", "easy"],
        "category": ["geography", "math"],
    }

    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, engine="openpyxl")
    excel_file.seek(0)

    # Simulate uploading the file using the Flask test client
    response = client.post(
        "/upload",
        content_type="multipart/form-data",
        data={"file": (excel_file, "questions.xlsx")},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "File uploaded and data inserted successfully"


def test_upload_missing_file(client):
    # Test uploading with no file
    response = client.post("/upload", content_type="multipart/form-data")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No file part in the request"


def test_upload_invalid_columns(client):
    # Create a mock Excel file with missing columns
    data = {
        "question": ["What is the capital of France?"],
        "choices": ["Paris,Berlin,Madrid,Rome"],
        "level": ["grade1"],
        "difficulty": ["easy"],
        "category": ["geography"],
    }  # Missing 'answer' column

    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, engine="openpyxl")
    excel_file.seek(0)

    # Simulate uploading the file using the Flask test client
    response = client.post(
        "/upload",
        content_type="multipart/form-data",
        data={"file": (excel_file, "questions.xlsx")},
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "Missing one or more required columns" in data["error"]
