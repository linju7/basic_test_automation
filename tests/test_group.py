# tests/test_group.py
from automation.modules.group.create import create_group
from tests.conftest import app_state, logged_in_page

def test_group_create_flow(logged_in_page):
    assert create_group(logged_in_page, app_state=app_state), "그룹 추가 실패"