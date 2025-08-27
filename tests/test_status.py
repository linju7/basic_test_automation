from automation.modules.status.create import create_status
from automation.modules.status.update import update_status
from automation.modules.status.delete import delete_status
from tests.conftest import app_state, logged_in_page

def test_01_status_create_flow(logged_in_page):
    assert create_status(logged_in_page, app_state=app_state), "상태 추가 실패"

def test_02_status_update_flow(logged_in_page):
    assert update_status(logged_in_page, app_state=app_state), "상태 수정 실패"

def test_03_status_delete_flow(logged_in_page):
    assert delete_status(logged_in_page), "상태 삭제 실패"