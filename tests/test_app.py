from fastapi import status


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities


def test_signup_for_activity_successful(client):
    # Arrange
    activity_name = "Chess Club"
    payload = {"email": "newstudent@mergington.edu"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=payload)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Signed up {payload['email']} for {activity_name}"}


def test_signup_for_activity_returns_400_when_duplicate(client):
    # Arrange
    activity_name = "Chess Club"
    payload = {"email": "michael@mergington.edu"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=payload)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    payload = {"email": "ghost@mergington.edu"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=payload)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_successful(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{participant_email}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Removed {participant_email} from {activity_name}"}


def test_remove_participant_returns_404_when_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{participant_email}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Participant not found"


def test_remove_participant_returns_404_when_missing_activity(client):
    # Arrange
    activity_name = "Nonexistent Club"
    participant_email = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{participant_email}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"
