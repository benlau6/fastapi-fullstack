def test_health_envelope(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"code", "message", "data"}
    assert body["code"] == 0
    assert body["data"]["status"] == "ok"
