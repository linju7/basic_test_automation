import pytest
from playwright.sync_api import Page, expect


def test_basic_page_load(page: Page):
    """기본 페이지 로딩 테스트"""
    page.goto("https://www.google.com")
    expect(page).to_have_title("Google") 