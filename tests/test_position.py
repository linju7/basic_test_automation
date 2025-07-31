from automation.modules.position.create import create_position
from automation.modules.position.update import update_position
# from automation.modules.position.delete import delete_position
from tests.conftest import app_state, logged_in_page

def test_position_create_flow(logged_in_page):
    assert create_position(logged_in_page, app_state=app_state), "직책 추가 실패"

def test_position_update_flow(logged_in_page):
    assert update_position(logged_in_page, app_state=app_state), "직책 수정 실패"

# def test_position_delete_flow(logged_in_page):
#     assert delete_position(logged_in_page, app_state=app_state), "직책 삭제 실패"