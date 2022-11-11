import json


def test_create_summary(test_app_with_db):
    resp = post_db(test_app_with_db)

    assert resp.status_code == 201
    assert resp.json()["url"] == "https://foo.bar"


def test_create_summaries_invalid_json(test_app):
    resp = test_app.post("/summaries/", data=json.dumps({}))
    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def post_db(test_app_with_db):
    return test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )


def test_read_summary(test_app_with_db):
    resp = post_db(test_app_with_db)
    summary_id = resp.json()["id"]

    resp = test_app_with_db.get(f"/summaries/{summary_id}")
    assert resp.status_code == 200

    resp_dict = resp.json()
    assert resp_dict["id"] == summary_id
    assert resp_dict["url"] == "https://foo.bar"
    assert resp_dict["summary"]
    assert resp_dict["created_at"]


def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app_with_db):
    response = test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "https://foo.bar"})
    )
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1
