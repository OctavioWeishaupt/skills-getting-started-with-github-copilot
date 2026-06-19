def test_get_activities(client):
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    activity = "Programming Class"
    email = "duplicate@mergington.edu"

    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r1.status_code == 200

    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r2.status_code == 400

    data = client.get("/activities").json()
    participants = data[activity]["participants"]
    assert participants.count(email) == 1


def test_delete_participant(client):
    activity = "Gym Class"
    email = "toremove@mergington.edu"

    client.post(f"/activities/{activity}/signup", params={"email": email})
    r = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200

    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_delete_nonexistent_returns_404(client):
    activity = "Gym Class"
    email = "notfound@mergington.edu"

    r = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 404
