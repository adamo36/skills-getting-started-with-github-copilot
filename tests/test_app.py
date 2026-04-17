import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Original activities data for resetting between tests
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball": {
        "description": "Competitive basketball team and skills development",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis": {
        "description": "Tennis lessons and tournament play",
        "schedule": "Tuesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["jessica@mergington.edu", "ryan@mergington.edu"]
    },
    "Art Club": {
        "description": "Drawing, painting, and sculpture exploration",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["maya@mergington.edu"]
    },
    "Music Band": {
        "description": "Learn and perform various musical instruments",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["david@mergington.edu", "grace@mergington.edu"]
    },
    "Debate Team": {
        "description": "Participate in competitive debates and develop speaking skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["chris@mergington.edu"]
    },
    "Math Club": {
        "description": "Advanced mathematics, problem solving, and competitions",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    }
}


@pytest.fixture
def client():
    # Reset activities to original state before each test
    activities.clear()
    activities.update(ORIGINAL_ACTIVITIES)
    return TestClient(app)


def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code == 200  # TestClient serves the static file after redirect
    assert "html" in response.text.lower()  # Check if it's HTML content


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert data == ORIGINAL_ACTIVITIES


def test_signup_success(client):
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up newstudent@mergington.edu for Chess Club"
    # Check that the participant was added
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_already_signed_up(client):
    response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found(client):
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_success(client):
    response = client.delete("/activities/Chess Club/unregister", params={"email": "michael@mergington.edu"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"
    # Check that the participant was removed
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_not_signed_up(client):
    response = client.delete("/activities/Chess Club/unregister", params={"email": "notsignedup@mergington.edu"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up for this activity"


def test_unregister_activity_not_found(client):
    response = client.delete("/activities/Nonexistent Activity/unregister", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"