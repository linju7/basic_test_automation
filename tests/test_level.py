from automation.modules.level.create import create_level
from automation.modules.level.update import update_level
from automation.modules.level.delete import delete_level
from tests.conftest import app_state, logged_in_page

def test_level_create_flow(logged_in_page):
    assert create_level(logged_in_page, app_state=app_state), "직급 추가 실패"

def test_level_update_flow(logged_in_page):
    assert update_level(logged_in_page, app_state=app_state), "직급 수정 실패"

def test_level_delete_flow(logged_in_page):
    assert delete_level(logged_in_page), "직급 삭제 실패"