import pytest

BASE_URL = 'https://jsonplaceholder.typicode.com'

@pytest.fixture(scope='module')
def posts_url():
    """URL base para operaciones sobre la colección de posts."""
    return f"{BASE_URL}/posts"

@pytest.fixture(scope='module')
def post_by_id_url():
    """Función que genera URLs específicas para cada post según su ID."""
    def _get_url(post_id):
        return f"{BASE_URL}/posts/{post_id}"
    return _get_url

@pytest.fixture(scope='module')
def users_url():
    """URL base para operaciones sobre usuarios."""
    return f"{BASE_URL}/users"
