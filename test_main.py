import pytest
from fastapi.testclient import TestClient
from main import app
import io

# Create test client
client = TestClient(app)


# Test 1: Home route
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Review Bot Running"}
    print("✅ Test 1 Passed: Home route working")


# Test 2: Upload valid file
def test_upload_valid_file():
    fake_code = b"from fastapi import FastAPI\napp = FastAPI()"
    file = io.BytesIO(fake_code)

    response = client.post(
        "/upload/",
        files={"file": ("test.py", file, "text/plain")}
    )
    assert response.status_code == 200
    assert "filename" in response.json()
    assert "preview" in response.json()
    print("✅ Test 2 Passed: Valid file upload working")


# Test 3: Upload empty file
def test_upload_empty_file():
    empty_file = io.BytesIO(b"")

    response = client.post(
        "/upload/",
        files={"file": ("empty.py", empty_file, "text/plain")}
    )
    assert response.status_code == 200
    print("✅ Test 3 Passed: Empty file handled")


# Test 4: Review valid file
def test_review_valid_file():
    good_code = b"""
from fastapi import FastAPI, UploadFile, HTTPException
app = FastAPI()

@app.get("/")
def home():
    try:
        return {"message": "hello"}
    except Exception as e:
        raise HTTPException(status_code=500)
"""
    file = io.BytesIO(good_code)

    response = client.post(
        "/review/",
        files={"file": ("good.py", file, "text/plain")}
    )
    assert response.status_code == 200
    assert "score" in response.json()
    assert "passed" in response.json()
    assert "issues" in response.json()
    print("✅ Test 4 Passed: Review working")


# Test 5: Review bad code (missing everything)
def test_review_bad_code():
    bad_code = b"print('hello world')"
    file = io.BytesIO(bad_code)

    response = client.post(
        "/review/",
        files={"file": ("bad.py", file, "text/plain")}
    )
    result = response.json()
    assert response.status_code == 200
    assert len(result["issues"]) > 0
    print("✅ Test 5 Passed: Bad code detected correctly")


# Test 6: Report generation
def test_report_generation():
    code = b"from fastapi import FastAPI\napp = FastAPI()\n@app.get('/')\ndef home():\n    return {'msg': 'hello'}"
    file = io.BytesIO(code)

    response = client.post(
        "/report/",
        files={"file": ("report_test.py", file, "text/plain")}
    )
    assert response.status_code == 200
    assert "report" in response.json()
    print("✅ Test 6 Passed: Report generation working")


# Test 7: Score check
def test_score_range():
    code = b"from fastapi import FastAPI\napp = FastAPI()\n@app.get('/')\ndef home():\n    return {'msg': 'hello'}"
    file = io.BytesIO(code)

    response = client.post(
        "/review/",
        files={"file": ("score_test.py", file, "text/plain")}
    )
    result = response.json()
    score_value = int(result["score"].split("/")[0])
    assert 0 <= score_value <= 10
    print("✅ Test 7 Passed: Score range is valid")