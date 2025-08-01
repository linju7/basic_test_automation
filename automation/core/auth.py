from playwright.sync_api import Page
from automation.config.settings import settings

LOGIN_ID_SELECTOR = "input[id='user_id']"
LOGIN_PW_SELECTOR = "input[id='user_pwd']"
SUBMIT_BTN_SELECTOR = "button[class='btn_submit']"
ALL_SERVICES_SELECTOR = "a.btn_apps#btnApps span.label_tooltip:text('전체 서비스')"


def login(page: Page):
    """
    Works Mobile 서비스에 로그인하고, '전체 서비스' 버튼이 보일 때까지 대기한다.
    """
    username = "automation" + settings.get_account("id")
    password = settings.get_account("password")

    page.goto(settings.get_base_url())
    _login_step(page, username, password)
    page.wait_for_selector(ALL_SERVICES_SELECTOR, timeout=10000)


def _login_step(page: Page, username: str, password: str):
    """로그인 폼에 아이디/비밀번호 입력 및 로그인 버튼 클릭"""
    page.fill(LOGIN_ID_SELECTOR, username)
    page.click(SUBMIT_BTN_SELECTOR)
    page.wait_for_load_state("networkidle")
    page.fill(LOGIN_PW_SELECTOR, password)
    page.click(SUBMIT_BTN_SELECTOR)
    page.wait_for_load_state("networkidle")