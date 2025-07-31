from automation.modules.position.create import create_position
from tests.conftest import app_state, logged_in_page

def test_position_create_flow(logged_in_page):
    assert create_position(logged_in_page, app_state=app_state), "직책 추가 실패"