def test_students_crud_flow(client, superuser_token_headers):
    c = client.post(
        "/v1/students",
        json={"student_no": "S1001", "name": "张三"},
        headers=superuser_token_headers,
    )
    assert c.status_code == 201
    sid = c.json()["data"]["id"]
    assert client.get("/v1/students", headers=superuser_token_headers).status_code == 200
    assert client.get(f"/v1/students/{sid}", headers=superuser_token_headers).status_code == 200
    assert (
        client.put(
            f"/v1/students/{sid}",
            json={"name": "张三丰"},
            headers=superuser_token_headers,
        ).status_code
        == 200
    )
    assert client.delete(f"/v1/students/{sid}", headers=superuser_token_headers).status_code == 200


def test_teachers_crud_flow(client, superuser_token_headers):
    c = client.post(
        "/v1/teachers",
        json={"teacher_no": "T1001", "name": "赵老师"},
        headers=superuser_token_headers,
    )
    assert c.status_code == 201
    tid = c.json()["data"]["id"]
    assert client.get("/v1/teachers", headers=superuser_token_headers).status_code == 200
    assert client.get(f"/v1/teachers/{tid}", headers=superuser_token_headers).status_code == 200
    assert (
        client.put(
            f"/v1/teachers/{tid}",
            json={"name": "赵老师A"},
            headers=superuser_token_headers,
        ).status_code
        == 200
    )
    assert client.delete(f"/v1/teachers/{tid}", headers=superuser_token_headers).status_code == 200


def test_courses_crud_flow(client, superuser_token_headers):
    c = client.post(
        "/v1/courses",
        json={"course_code": "C1001", "course_name": "数学"},
        headers=superuser_token_headers,
    )
    assert c.status_code == 201
    cid = c.json()["data"]["id"]
    assert client.get("/v1/courses", headers=superuser_token_headers).status_code == 200
    assert client.get(f"/v1/courses/{cid}", headers=superuser_token_headers).status_code == 200
    assert (
        client.put(
            f"/v1/courses/{cid}",
            json={"course_name": "数学A"},
            headers=superuser_token_headers,
        ).status_code
        == 200
    )
    assert client.delete(f"/v1/courses/{cid}", headers=superuser_token_headers).status_code == 200


def test_classes_crud_flow(client, superuser_token_headers):
    c = client.post(
        "/v1/classes",
        json={"class_code": "CL1001", "class_name": "一班", "grade": "七年级"},
        headers=superuser_token_headers,
    )
    assert c.status_code == 201
    cid = c.json()["data"]["id"]
    assert client.get("/v1/classes", headers=superuser_token_headers).status_code == 200
    assert client.get(f"/v1/classes/{cid}", headers=superuser_token_headers).status_code == 200
    assert (
        client.put(
            f"/v1/classes/{cid}",
            json={"class_name": "一班A"},
            headers=superuser_token_headers,
        ).status_code
        == 200
    )
    assert client.delete(f"/v1/classes/{cid}", headers=superuser_token_headers).status_code == 200


def test_delete_success_envelope_all_resources(client, superuser_token_headers):
    s = client.post(
        "/v1/students",
        json={"student_no": "SDEL01", "name": "待删学生"},
        headers=superuser_token_headers,
    ).json()["data"]["id"]
    t = client.post(
        "/v1/teachers",
        json={"teacher_no": "TDEL01", "name": "待删教师"},
        headers=superuser_token_headers,
    ).json()["data"]["id"]
    c = client.post(
        "/v1/courses",
        json={"course_code": "CDEL01", "course_name": "待删课程"},
        headers=superuser_token_headers,
    ).json()["data"]["id"]
    cl = client.post(
        "/v1/classes",
        json={"class_code": "CLDEL1", "class_name": "待删班级", "grade": "八年级"},
        headers=superuser_token_headers,
    ).json()["data"]["id"]

    for path in [f"/v1/students/{s}", f"/v1/teachers/{t}", f"/v1/courses/{c}", f"/v1/classes/{cl}"]:
        r = client.delete(path, headers=superuser_token_headers)
        assert r.status_code == 200
        assert r.json() == {"code": 0, "message": "ok", "data": None}


def test_spec_alias_students_works(client, superuser_token_headers):
    r = client.get("/students", headers=superuser_token_headers)
    assert r.status_code == 200


def test_spec_alias_teachers_works(client, superuser_token_headers):
    r = client.get("/teachers", headers=superuser_token_headers)
    assert r.status_code == 200


def test_spec_alias_courses_works(client, superuser_token_headers):
    r = client.get("/courses", headers=superuser_token_headers)
    assert r.status_code == 200


def test_spec_alias_classes_works(client, superuser_token_headers):
    r = client.get("/classes", headers=superuser_token_headers)
    assert r.status_code == 200
