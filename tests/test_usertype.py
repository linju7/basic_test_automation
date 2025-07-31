from automation.modules.usertype.create import create_usertype
from tests.conftest import app_state, logged_in_page

def test_usertype_create_flow(logged_in_page):
    assert create_usertype(logged_in_page, app_state=app_state), "사용자 유형 추가 실패"   