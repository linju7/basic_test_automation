import pytest
from playwright.sync_api import Page
from automation.core.auth import login
from automation.modules.user.create import create_user

def test_create_user(page: Page):
    """구성원 추가 성공 모달이 정상적으로 노출되는지 확인한다."""

    # 1. 로그인
    login(page)

    # 2. 구성원 추가
    create_user(page, app_state=None)

    # 3. 구성원 추가 완료 모달 확인
    page.wait_for_selector("div.ly_member_added h3.tit:text('구성원 추가 완료')", timeout=5000)
    assert page.locator("div.ly_member_added h3.tit:text('구성원 추가 완료')").count() > 0, "구성원 추가 완료 모달이 나타나야 합니다."