from automation.modules.contact.create import create_contact
from automation.modules.contact.update import update_contact
from automation.modules.contact.delete import delete_contact
from tests.conftest import app_state, logged_in_page

def test_01_contact_create_flow(logged_in_page):
    assert create_contact(logged_in_page, app_state=app_state), "외부 연락처 추가 실패"

def test_02_contact_update_flow(logged_in_page):
    assert update_contact(logged_in_page, app_state=app_state), "외부 연락처 수정 실패"

def test_03_contact_delete_flow(logged_in_page):
    assert delete_contact(logged_in_page, app_state=app_state), "외부 연락처 삭제 실패"