import pytest
from utils.fake_data import generate_user, generate_post


@pytest.mark.faker_driven
@pytest.mark.smoke
class TestFakerDriven:

    def test_create_user_with_faker(self, user_client):
        payload = generate_user()
        response = user_client.create_user(payload)
        assert response.status_code == 201

        actual = response.json()
        assert actual["name"] == payload["name"]
        assert actual["email"] == payload["email"]

    def test_create_multiple_users_with_faker(self, user_client):
        users_created = []
        for _ in range(5):
            payload = generate_user()
            response = user_client.create_user(payload)
            assert response.status_code == 201
            users_created.append(response.json())

        assert len(users_created) == 5
        names = [u["name"] for u in users_created]
        assert len(set(names)) == 5, "Expected all generated users to have unique names"

    def test_create_post_with_faker(self, post_client):
        payload = generate_post(user_id=1)
        response = post_client.create_post(payload)
        assert response.status_code == 201

        actual = response.json()
        assert actual["title"] == payload["title"]
        assert actual["body"] == payload["body"]
        assert actual["userId"] == payload["userId"]