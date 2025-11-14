from automation.modules.users_custom_field.create import create_users_custom_field
from tests.conftest import app_state, logged_in_page


def test_01_users_custom_field_create_flow(logged_in_page):
    """구성원 커스텀 필드 생성 테스트"""
    assert create_users_custom_field(logged_in_page, app_state=app_state), "구성원 커스텀 필드 추가 실패"

