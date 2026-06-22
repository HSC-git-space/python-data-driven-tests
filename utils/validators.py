import pandas as pd


def validate_response_fields(response_data: dict, expected: dict):
    mismatches = []
    for key, expected_value in expected.items():
        actual_value = response_data.get(key)
        if str(actual_value) != str(expected_value):
            mismatches.append({
                "field": key,
                "expected": expected_value,
                "actual": actual_value
            })
    return mismatches


def validate_bulk_responses(response_list: list, expected_df: pd.DataFrame):
    expected_records = expected_df.to_dict(orient="records")
    all_mismatches = []

    for i, (actual, expected) in enumerate(zip(response_list, expected_records)):
        mismatches = validate_response_fields(actual, expected)
        if mismatches:
            all_mismatches.append({
                "record_index": i,
                "mismatches": mismatches
            })

    return all_mismatches