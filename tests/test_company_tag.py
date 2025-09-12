from automation.modules.company_tag.create import create_company_tag
from automation.modules.company_tag.retrieve import retrieve_company_tag
from tests.conftest import app_state, logged_in_page

def test_01_create_company_tag_flow(logged_in_page):
    assert create_company_tag(logged_in_page, app_state=app_state), "회사 태그 추가 실패"

def test_02_retrieve_company_tag_flow(logged_in_page):
    assert retrieve_company_tag(logged_in_page, app_state=app_state), "회사 태그 조회 실패"