"""
로그인 테스트
"""
from playwright.sync_api import Page
from automation.core.auth import AuthManager


def test_login(page: Page):
    """로그인 테스트"""
    auth = AuthManager(page)
    auth.login()
    
    # 로그인 성공 확인 (페이지 제목이나 특정 요소로 확인)
    assert "worksmobile" in page.url 

    page.pause()