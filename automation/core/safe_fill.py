from playwright.sync_api import Page

def safe_fill(page: Page, selector: str, value: str):
    """해당 selector가 존재할 때만 값을 입력한다."""
    if page.locator(selector).count() > 0:
        page.locator(selector).fill(value)