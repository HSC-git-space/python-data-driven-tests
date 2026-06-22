import pytest
from api.endpoints import UserEndpoints, PostEndpoints
from utils.fake_data import set_seed


@pytest.fixture(scope="session")
def user_client():
    return UserEndpoints()


@pytest.fixture(scope="session")
def post_client():
    return PostEndpoints()


@pytest.fixture(scope="session", autouse=True)
def set_faker_seed():
    set_seed(42)


@pytest.fixture
def user_data_csv():
    from utils.data_loader import load_csv
    return load_csv("data/users.csv")


@pytest.fixture
def posts_data_excel():
    from utils.data_loader import load_excel
    return load_excel("data/posts.xlsx", sheet_name="valid_posts")


@pytest.fixture
def negative_posts_excel():
    from utils.data_loader import load_excel
    return load_excel("data/posts.xlsx", sheet_name="negative_cases")
