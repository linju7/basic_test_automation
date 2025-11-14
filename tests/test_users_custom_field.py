from automation.modules.users_custom_field.create import create_users_custom_field
from automation.modules.users_custom_field.update import update_users_custom_field
from automation.modules.users_custom_field.delete import delete_users_custom_field
from tests.conftest import app_state, logged_in_page


def test_01_users_custom_field_create_flow(logged_in_page):
    """구성원 커스텀 필드 생성 테스트"""
    assert create_users_custom_field(logged_in_page, app_state=app_state), "구성원 커스텀 필드 추가 실패"


def test_02_users_custom_field_update_flow(logged_in_page):
    """구성원 커스텀 필드 수정 테스트"""
    assert update_users_custom_field(logged_in_page, app_state=app_state), "구성원 커스텀 필드 수정 실패"


def test_03_users_custom_field_delete_flow(logged_in_page):
    """구성원 커스텀 필드 삭제 테스트"""
    assert delete_users_custom_field(logged_in_page, app_state=app_state), "구성원 커스텀 필드 삭제 실패"

