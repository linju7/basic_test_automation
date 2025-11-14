from automation.modules.orgunit.create import create_orgunit
from automation.modules.position.create import create_position
from automation.modules.level.create import create_level
from automation.modules.usertype.create import create_usertype
from automation.modules.user.create import create_user
from tests.conftest import app_state, logged_in_page


def test_01_orgunit_create_flow(logged_in_page):
    """조직 생성"""
    assert create_orgunit(logged_in_page, app_state=app_state), "조직 추가 실패"


def test_02_position_create_flow(logged_in_page):
    """직책 생성"""
    assert create_position(logged_in_page, app_state=app_state), "직책 추가 실패"


def test_03_level_create_flow(logged_in_page):
    """직급 생성"""
    assert create_level(logged_in_page, app_state=app_state), "직급 추가 실패"


def test_04_usertype_create_flow(logged_in_page):
    """사용자 유형 생성"""
    assert create_usertype(logged_in_page, app_state=app_state), "사용자 유형 추가 실패"


def test_05_user_create_flow(logged_in_page):
    """구성원 생성 (앞서 생성한 조직/직책/직급/유형 자동 적용)"""
    assert create_user(logged_in_page, app_state=app_state, auto_apply=True), "구성원 추가 실패"