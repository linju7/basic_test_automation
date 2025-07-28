"""
로그인 테스트
"""
import pytest
from playwright.sync_api import Page
from automation.core.auth import login

def test_login(page: Page):
    """로그인 성공 여부를 확인한다."""
    login(page)
    assert "worksmobile" in page.url, "로그인 후 URL에 'worksmobile'이 포함되어야 합니다." 