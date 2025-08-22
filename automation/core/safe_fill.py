from playwright.sync_api import Page

def safe_fill(page: Page, selector: str, value: str):
    """해당 selector가 존재할 때만 값을 입력한다."""
    if page.locator(selector).count() > 0:
        page.locator(selector).fill(value)

def safe_fill_last(page: Page, selector: str, value: str):
    """해당 selector의 마지막 요소에만 값을 입력한다. (직책/직급/유형/상태 등에서 사용)"""
    elements = page.locator(selector)
    if elements.count() > 0:
        last_element = elements.nth(elements.count() - 1)
        last_element.fill(value)