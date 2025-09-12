from automation.modules.my_tag.create import create_my_tag
from automation.modules.my_tag.retrieve import retrieve_my_tag
from automation.modules.my_tag.update import update_my_tag
from automation.modules.my_tag.delete import delete_my_tag
from tests.conftest import app_state, logged_in_page

def test_01_create_my_tag_flow(logged_in_page):
    assert create_my_tag(logged_in_page, app_state=app_state), "MY 태그 추가 실패"

def test_02_retrieve_my_tag_flow(logged_in_page):
    assert retrieve_my_tag(logged_in_page, app_state=app_state), "MY 태그 조회 실패"

def test_03_update_my_tag_flow(logged_in_page):
    assert update_my_tag(logged_in_page, app_state=app_state), "MY 태그 수정 실패"

def test_04_retrieve_my_tag_flow(logged_in_page):
    assert retrieve_my_tag(logged_in_page, app_state=app_state), "MY 태그 조회 실패"

def test_05_delete_my_tag_flow(logged_in_page):
    assert delete_my_tag(logged_in_page, app_state=app_state), "MY 태그 삭제 실패"
