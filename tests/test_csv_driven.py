import pytest
from utils.validators import validate_response_fields


@pytest.mark.csv_driven
@pytest.mark.regression
class TestCSVDriven:

    def test_user_fields_match_csv(self, user_client, user_data_csv):
        for i, expected_user in enumerate(user_data_csv, start=1):
            response = user_client.get_user(i)
            assert response.status_code == 200

            actual = response.json()
            mismatches = validate_response_fields(actual, expected_user)

            assert mismatches == [], (
                    f"User {i} mismatches:\n" +
                    "\n".join(f"  {m['field']}: expected={m['expected']}, actual={m['actual']}"
                              for m in mismatches)
            )

    def test_csv_row_count_matches_api(self, user_client, user_data_csv):
        response = user_client.get_all_users()
        assert response.status_code == 200

        api_users = response.json()
        assert len(user_data_csv) <= len(api_users), (
            f"CSV has {len(user_data_csv)} users but API only returned {len(api_users)}"
        )