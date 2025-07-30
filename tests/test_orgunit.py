# tests/test_orgunit.py
from automation.modules.orgunit.create import create_orgunit
from automation.modules.orgunit.update import update_orgunit
from automation.modules.orgunit.delete import delete_orgunit

from tests.conftest import app_state, logged_in_page

def test_orgunit_create_flow(logged_in_page):
    assert create_orgunit(logged_in_page, app_state=app_state), "조직 추가 실패"

def test_orgunit_update_flow(logged_in_page):
    assert update_orgunit(logged_in_page, app_state=app_state), "조직 수정 실패"

def test_orgunit_delete_flow(logged_in_page):
    assert delete_orgunit(logged_in_page, app_state=app_state), "조직 삭제 실패"