from automation.modules.external_group.create import create_external_group
from tests.conftest import app_state, logged_in_page

def test_01_create_external_group_flow(logged_in_page):
    assert create_external_group(logged_in_page, app_state=app_state), "외부그룹 추가 실패"