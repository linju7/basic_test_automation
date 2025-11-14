from automation.modules.contact_custom_field.create import create_contact_custom_field
from tests.conftest import app_state, logged_in_page


def test_contact_custom_field_create_flow(logged_in_page):
    """연락처 커스텀 필드 생성 테스트"""
    assert create_contact_custom_field(logged_in_page, app_state=app_state), "연락처 커스텀 필드 추가 실패"

