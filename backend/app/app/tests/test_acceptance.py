def test_duplicate_student_no_returns_409(client, superuser_token_headers):
    payload = {"student_no": "S3001", "name": "王五"}
    assert client.post("/v1/students", json=payload, headers=superuser_token_headers).status_code == 201
    r = client.post("/v1/students", json=payload, headers=superuser_token_headers)
    assert r.status_code == 409
    assert set(r.json().keys()) == {"code", "message", "data"}


def test_delete_restricted_teacher_returns_409_resource_in_use(client, superuser_token_headers):
    t = client.post(
        "/v1/teachers",
        json={"teacher_no": "T9001", "name": "王老师"},
        headers=superuser_token_headers,
    ).json()["data"]
    client.post(
        "/v1/courses",
        json={"course_code": "C9001", "course_name": "语文", "teacher_id": t["id"]},
        headers=superuser_token_headers,
    )
    r = client.delete(f"/v1/teachers/{t['id']}", headers=superuser_token_headers)
    assert r.status_code == 409
    assert r.json()["message"] == "resource_in_use"


def test_error_matrix_envelope(client, superuser_token_headers):
    r401 = client.get("/v1/students")
    assert r401.status_code == 401
    assert set(r401.json().keys()) == {"code", "message", "data"}

    payload = {"student_no": "S3999", "name": "矩阵"}
    client.post("/v1/students", json=payload, headers=superuser_token_headers)
    r409 = client.post("/v1/students", json=payload, headers=superuser_token_headers)
    assert r409.status_code == 409
    assert set(r409.json().keys()) == {"code", "message", "data"}

    r422 = client.post("/v1/students", json={}, headers=superuser_token_headers)
    assert r422.status_code == 422
    assert r422.json()["code"] == 100422
    assert r422.json()["message"] == "validation_error"
