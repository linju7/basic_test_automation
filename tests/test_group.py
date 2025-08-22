# tests/test_group.py
from automation.modules.group.create import create_group
from automation.modules.group.update import update_group
from automation.modules.group.delete import delete_group
from automation.modules.group.retrieve import retrieve_group
from tests.conftest import app_state, logged_in_page

def test_01_group_create_flow(logged_in_page):
    assert create_group(logged_in_page, app_state=app_state), "그룹 추가 실패"

def test_02_group_retrieve_flow(logged_in_page):
    assert retrieve_group(logged_in_page, app_state=app_state), "그룹 조회 실패"

def test_03_group_update_flow(logged_in_page):
    assert update_group(logged_in_page, app_state=app_state), "그룹 수정 실패"
    
def test_04_group_retrieve_flow(logged_in_page):
    assert retrieve_group(logged_in_page, app_state=app_state), "그룹 조회 실패"

def test_05_group_delete_flow(logged_in_page):
    assert delete_group(logged_in_page), "그룹 삭제 실패"