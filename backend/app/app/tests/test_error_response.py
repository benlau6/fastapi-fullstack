def test_validation_error_envelope(client, superuser_token_headers):
    r = client.post("/v1/students", json={}, headers=superuser_token_headers)
    assert r.status_code == 422
    body = r.json()
    assert set(body.keys()) == {"code", "message", "data"}
    assert body["code"] == 100422
    assert body["message"] == "validation_error"
    assert "errors" in body["data"]


def test_not_found_error_envelope(client, superuser_token_headers):
    r = client.get("/v1/students/999999", headers=superuser_token_headers)
    assert r.status_code == 404
    body = r.json()
    assert set(body.keys()) == {"code", "message", "data"}
    assert body["code"] == 100404
