# tests/test_user.py
from automation.modules.user.create import create_user
from automation.modules.user.update import update_user
from tests.conftest import app_state, logged_in_page

def test_create_user(logged_in_page):
    assert create_user(logged_in_page, app_state=app_state), "구성원 추가 실패"

def test_update_user(logged_in_page):
    assert update_user(logged_in_page, app_state=app_state), "구성원 정보 수정 실패"
