def test_default_categories_seeded(client, auth_headers):
    r = client.get("/categories", headers=auth_headers)
    assert r.status_code == 200
    names = [c["name"].lower() for c in r.json()]
    for expected in ["bills", "food", "entertainment", "transportation", "shopping", "subscriptions"]:
        assert expected in names

def test_create_duplicate_category_rejected(client, auth_headers):
    r1 = client.post("/categories", json={"name": "Gym"}, headers=auth_headers)
    assert r1.status_code == 201
    r2 = client.post("/categories", json={"name": "gym"}, headers=auth_headers)
    assert r2.status_code == 409  # duplicate (case-insensitive)
