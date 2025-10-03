from datetime import datetime, timezone, timedelta, date

def _mk(client, headers, amount, category_id, when=None, note=""):
    when = when or datetime.now(timezone.utc)
    r = client.post("/expenses", headers=headers, json={
        "amount": amount, "currency": "AUD", "category_id": category_id,
        "note": note, "spent_at": when.isoformat()
    })
    assert r.status_code == 201

def test_stats_and_report_summary(client, auth_headers, any_category_id):
    now = datetime.now(timezone.utc)
    # ensure some data today
    _mk(client, auth_headers, 3.25, any_category_id, now, "coffee")
    _mk(client, auth_headers, 6.75, any_category_id, now, "lunch")

    # total today via /stats/today
    r1 = client.get("/stats/today", headers=auth_headers)
    assert r1.status_code == 200
    assert r1.json()["total"] >= 10.0 - 1e-9  # float

    # total-by-category (period == today)
    day_str = now.date().isoformat()
    r2 = client.get(f"/stats/total-by-category?start={day_str}&end={day_str}", headers=auth_headers)
    assert r2.status_code == 200
    rows = r2.json()
    assert any(row["category_id"] == any_category_id for row in rows)

    # /reports/summary for current month (no params defaults)
    r3 = client.get("/reports/summary", headers=auth_headers)
    assert r3.status_code == 200
    js = r3.json()
    assert "total" in js and "by_category" in js and "daily" in js
    assert js["currency"] == "AUD"
