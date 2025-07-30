# tests/test_orgunit.py
from automation.modules.orgunit.create import create_orgunit
from tests.conftest import app_state, logged_in_page

def test_orgunit_create_flow(logged_in_page):
    assert create_orgunit(logged_in_page, app_state=app_state), "조직 추가 실패"