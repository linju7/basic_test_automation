from automation.modules.level.create import create_level
from tests.conftest import app_state, logged_in_page

def test_level_create_flow(logged_in_page):
    assert create_level(logged_in_page, app_state=app_state), "직급 추가 실패"