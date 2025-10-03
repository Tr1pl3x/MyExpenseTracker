from datetime import datetime, timezone, timedelta

def test_create_and_list_expenses_sorted_desc(client, auth_headers, any_category_id):
    now = datetime.now(timezone.utc)
    older = (now - timedelta(days=1)).isoformat()
    newer = (now + timedelta(minutes=5)).isoformat()

    # older
    r1 = client.post("/expenses", headers=auth_headers, json={
        "amount": 10.5, "currency": "AUD", "category_id": any_category_id,
        "note": "older", "spent_at": older
    })
    assert r1.status_code == 201

    # newer
    r2 = client.post("/expenses", headers=auth_headers, json={
        "amount": 12.0, "currency": "AUD", "category_id": any_category_id,
        "note": "newer", "spent_at": newer
    })
    assert r2.status_code == 201

    # list default (DESC)
    r3 = client.get("/expenses", headers=auth_headers)
    assert r3.status_code == 200
    items = r3.json()
    assert len(items) >= 2
    # newest first
    assert items[0]["note"] == "newer"
    assert items[1]["note"] == "older"

def test_expenses_by_category(client, auth_headers, any_category_id):
    # create one in the chosen category
    r1 = client.post("/expenses", headers=auth_headers, json={
        "amount": 5, "currency": "AUD", "category_id": any_category_id, "note": "cat-one"
    })
    assert r1.status_code == 201
    # create another in some other category
    rcat = client.post("/categories", headers=auth_headers, json={"name": "Books"})
    assert rcat.status_code == 201
    other_id = rcat.json()["id"]
    r2 = client.post("/expenses", headers=auth_headers, json={
        "amount": 7, "currency": "AUD", "category_id": other_id, "note": "cat-two"
    })
    assert r2.status_code == 201

    # filter by first category
    r3 = client.get(f"/expenses/by-category/{any_category_id}", headers=auth_headers)
    assert r3.status_code == 200
    notes = [x["note"] for x in r3.json()]
    assert "cat-one" in notes
    assert "cat-two" not in notes
