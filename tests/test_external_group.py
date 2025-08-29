from automation.modules.external_group.create import create_external_group
from automation.modules.external_group.retrieve import retrieve_external_group
from automation.modules.external_group.update import update_external_group
from automation.modules.external_group.delete import delete_external_group
from tests.conftest import app_state, logged_in_page

def test_01_create_external_group_flow(logged_in_page):
    assert create_external_group(logged_in_page, app_state=app_state), "외부그룹 추가 실패"

def test_02_retrieve_external_group_flow(logged_in_page):
    assert retrieve_external_group(logged_in_page, app_state=app_state), "외부그룹 조회 실패"

def test_03_update_external_group_flow(logged_in_page):
    assert update_external_group(logged_in_page, app_state=app_state), "외부그룹 수정 실패"

def test_04_delete_external_group_flow(logged_in_page):
    assert delete_external_group(logged_in_page, app_state=app_state), "외부그룹 삭제 실패"