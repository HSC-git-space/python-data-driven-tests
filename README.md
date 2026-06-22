# Python Data-Driven Test Framework

![CI](https://github.com/HSC-git-space/python-data-driven-tests/actions/workflows/ci.yml/badge.svg)

A production-grade data-driven API test framework built with Python, Pandas, Faker, and pytest.
Tests the JSONPlaceholder REST API across three data strategies — CSV, Excel, and synthetic Faker data.
Designed to reflect real-world QA engineering patterns: external data sources, bulk validation, reproducible test data, and automated CI reporting.

---

## What This Repo Demonstrates

- **CSV-driven testing** — test data loaded from CSV via Pandas, each row becomes a test case, API response validated against expected values field by field
- **Excel-driven testing** — multi-sheet Excel file separates valid and negative test cases into organised sheets, loaded dynamically at runtime
- **Faker-driven testing** — realistic synthetic data generated via Faker with a fixed seed for reproducibility across runs and environments
- **Bulk response validation** — Pandas-based validator compares entire response datasets against expected data, returning structured mismatch reports instead of single field assertions
- **Session-level HTTP retry** — retry logic attached to the HTTP transport layer via `HTTPAdapter` and `urllib3.Retry`, not at the test level — handles transient network failures before the test even sees a response
- **Centralised configuration** — single `config.py` as source of truth for base URL, headers, timeout, and retry settings; supports environment variable override for CI/staging environments
- **Pydantic response models** — API responses validated against typed models before assertion, catching schema violations at the data layer
- **CI/CD pipeline** — GitHub Actions runs the full suite on every push, generates HTML report as downloadable artifact

---

## Stack

| Tool | Purpose |
|---|---|
| pytest | Test runner, fixture management, markers |
| requests | HTTP client |
| Pandas | CSV and Excel data loading, bulk DataFrame validation |
| Faker | Synthetic test data generation with seed support |
| Pydantic | Typed response model validation |
| openpyxl | Excel read/write engine for Pandas |
| pytest-rerunfailures | Test-level retry for genuinely flaky tests |
| pytest-html | HTML test report generation |
| allure-pytest | Allure report integration |
| GitHub Actions | CI pipeline automation |

---

## Project Structure
python-data-driven-tests/

├── api/

│   ├── base_client.py          # Core HTTP session with transport-level retry strategy

│   └── endpoints.py            # UserEndpoints and PostEndpoints inheriting BaseClient

├── config/

│   └── config.py               # Centralised config — BASE_URL, HEADERS, TIMEOUT, RETRY settings

├── data/

│   ├── users.csv               # Expected user data matching JSONPlaceholder /users response

│   └── posts.xlsx              # Multi-sheet: valid_posts and negative_cases

├── models/

│   ├── user_model.py           # Pydantic models — UserModel, Address, Company, CreateUserModel

│   └── post_model.py           # Pydantic models — PostModel, CreatePostModel

├── utils/

│   ├── data_loader.py          # Pandas CSV and Excel loader with null row handling

│   ├── fake_data.py            # Faker factory — generate_user(), generate_post(), set_seed()

│   └── validators.py           # Field-level and bulk Pandas response comparison

├── tests/

│   ├── test_csv_driven.py      # CSV-driven user field validation and row count assertion

│   ├── test_excel_driven.py    # Excel-driven post creation and negative case handling

│   └── test_faker_driven.py    # Faker-driven user and post creation with uniqueness assertion

├── conftest.py                 # Session-scoped fixtures — clients, Faker seed, data loaders

├── pytest.ini                  # Test paths, markers, HTML report config, pythonpath

└── .github/workflows/

└── ci.yml                  # GitHub Actions — Python 3.11, pip install, pytest, artifact upload

---

## Execution Flow
pytest command

└── reads pytest.ini → testpaths, markers, addopts

└── loads conftest.py

├── sets Faker seed = 42 (autouse, session-scoped)

├── creates UserEndpoints (session-scoped)

└── creates PostEndpoints (session-scoped)

└── discovers tests/ folder

├── test_csv_driven.py

│       └── loads data/users.csv via Pandas

│       └── loops rows → GET /users/{id} → validate_response_fields()

├── test_excel_driven.py

│       └── loads data/posts.xlsx (valid_posts sheet) via Pandas

│       └── loops rows → POST /posts → assert echo

│       └── loads negative_cases sheet → POST with bad data → handles gracefully

└── test_faker_driven.py

└── generate_user() → POST /users → assert echo

└── generate_user() x5 → assert all 201, all unique names

└── generate_post() → POST /posts → assert echo

└── generates reports/report.html

---

## How to Run

```bash
# Clone and set up
git clone https://github.com/HSC-git-space/python-data-driven-tests.git
cd python-data-driven-tests
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt

# Run all tests
python -m pytest -v

# Run by data source
python -m pytest -m csv_driven
python -m pytest -m excel_driven
python -m pytest -m faker_driven

# Run by test type
python -m pytest -m smoke
python -m pytest -m regression

# Run with visible seed in output
python -m pytest -v -s
```

---

## Key Design Decisions

**Session-level retry over test-level retry**
Most frameworks implement retry at the test level — if a test fails, rerun it. This is a blunt instrument that reruns setup, teardown, and all assertions. In this framework, retry is configured at the HTTP transport layer via `urllib3.Retry` and `HTTPAdapter`. Transient connection failures (429, 500, 502, 503, 504) are silently retried before a response reaches the test. The test never knows a retry happened. This is a more precise, lower-overhead solution — and a more accurate reflection of where network failures actually occur.

**Seeded Faker for reproducible failures**
Faker generates random data by default — different every run. This makes CI failures hard to reproduce locally. By setting `Faker.seed(42)` at session start via an `autouse` fixture, every run produces the exact same generated data in the same order. If a test fails due to a specific generated value (e.g. a name with a special character), the seed guarantees that value appears on every rerun — locally and in CI.

**Pandas for bulk validation over field assertions**
Repo 1 validated responses field by field — one assert per field. This scales poorly for data-heavy tests. The `validators.py` utility compares entire response datasets against expected DataFrames and returns structured mismatch reports: field name, expected value, actual value. A test with 5 users produces one validation call, not 25 assertions. Failures identify exactly which field on which record failed.

**Multi-sheet Excel for test case organisation**
A single `posts.xlsx` file contains `valid_posts` and `negative_cases` on separate sheets. This mirrors how QA teams maintain test data in real projects — one file per resource, sheets organised by scenario type. Pandas `sheet_name` parameter loads the correct sheet at runtime.

**CSV for flat data, Excel for structured multi-scenario data**
User data is flat — name, email, phone, website. CSV is the right tool — lightweight, readable, no overhead. Post data requires multiple scenario types (valid and negative). Excel's multi-sheet structure is the right tool. Each format chosen deliberately, not arbitrarily.

**Environment variable support in config**
`BASE_URL` is read from environment variables with a fallback default. CI pipelines can override the target environment without touching code — `BASE_URL=https://staging.api.com pytest` points the entire suite at staging. This is the foundation of multi-environment test execution.

---

## Known Limitations

- JSONPlaceholder has no real server-side validation — negative payload tests cannot assert 4xx responses; documented explicitly in test comments
- JSONPlaceholder does not persist created or updated resources — POST/PUT/DELETE tests verify response echo only, not actual persistence
- Phone number formats in JSONPlaceholder are inconsistent across users — CSV expected values must match exact API format including extensions and brackets
- Faker seed is hardcoded at 42 — in a production framework the seed would be randomised per run and logged for reproducibility

---

## Related Repos

- [python-api-test-framework](https://github.com/HSC-git-space/python-api-test-framework) — Repo 1: Core API testing framework with Pydantic validation, jsonschema, and GitHub Actions CI
  