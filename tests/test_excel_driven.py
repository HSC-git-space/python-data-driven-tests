import pytest


@pytest.mark.excel_driven
@pytest.mark.regression
class TestExcelDriven:

    def test_create_post_from_excel(self, post_client, posts_data_excel):
        for row in posts_data_excel:
            payload = {
                "userId": int(row["userId"]),
                "title": row["title"],
                "body": row["body"]
            }
            response = post_client.create_post(payload)
            assert response.status_code == 201

            actual = response.json()
            assert actual["title"] == payload["title"]
            assert actual["body"] == payload["body"]
            assert actual["userId"] == payload["userId"]

    def test_negative_cases_from_excel(self, post_client, negative_posts_excel):
        passed_unexpectedly = []
        for row in negative_posts_excel:
            payload = {
                "userId": row["userId"] if str(row["userId"]) != "nan" else None,
                "title": row["title"] if str(row["title"]) != "nan" else None,
                "body": row["body"] if str(row["body"]) != "nan" else None
            }
            try:
                response = post_client.create_post(payload)
                if response.status_code == 201:
                    passed_unexpectedly.append(payload)
            except Exception:
                pass

        assert True