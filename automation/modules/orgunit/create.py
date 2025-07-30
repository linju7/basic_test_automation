from automation.config.settings import settings
from datetime import datetime

# 주요 셀렉터 상수
BTN_ORG_ADD = 'button.btn_save:text-is("조직 추가")'
LAYER_ORG_ADD = 'div.ly_member_add h3.tit:text("조직 추가")'
INPUT_ORG_NAME = 'input.lw_input[placeholder="조직명"]'
INPUT_ENGLISH = 'input.lw_input[placeholder="English"]'
INPUT_KOREAN = 'input.lw_input[placeholder="Korean"]'
INPUT_CHINESE_TWN = 'input.lw_input[placeholder="Chinese (TWN)"]'
INPUT_JAPANESE = 'input.lw_input[placeholder="Japanese"]'
INPUT_CHINESE_CHN = 'input.lw_input[placeholder="Chinese (CHN)"]'
INPUT_DESCRIPTION = 'input.lw_input[placeholder="설명"]'
BTN_ADD = 'div.ly_member_add button.lw_btn_point:text-is("추가")'

def safe_fill(page, selector, value):
    """해당 selector가 존재할 때만 값을 입력한다."""
    if page.locator(selector).count() > 0:
        page.locator(selector).fill(value)

def open_org_add_layer(page):
    """조직 추가 버튼을 클릭한다."""
    page.wait_for_selector(BTN_ORG_ADD, timeout=5000)
    page.locator(BTN_ORG_ADD).click()
    page.wait_for_selector(LAYER_ORG_ADD, timeout=5000)
    return True

def fill_org_info(page, app_state=None):
    """조직명, 다국어명, 설명 필드를 입력한다. (safe_fill 사용)"""
    timestamp = datetime.now().strftime("%m%d%H%M")
    org_name = f"자동화조직_{timestamp}"
    safe_fill(page, INPUT_ORG_NAME, org_name)
    if app_state is not None:
        app_state.org_name = org_name
    safe_fill(page, INPUT_ENGLISH, "AutoOrg_EN")
    safe_fill(page, INPUT_KOREAN, "자동화조직_KR")
    safe_fill(page, INPUT_CHINESE_TWN, "自動組織_TWN")
    safe_fill(page, INPUT_JAPANESE, "自動組織_JP")
    safe_fill(page, INPUT_CHINESE_CHN, "自动组织_CHN")
    safe_fill(page, INPUT_DESCRIPTION, "자동화로 생성된 조직입니다.")
    return True


def click_add_button(page):
    """'추가' 버튼을 클릭한다."""
    add_btn = page.locator(BTN_ADD)
    if add_btn.count() > 0:
        add_btn.first.click()
        page.wait_for_timeout(2000)
        return True
    return False


def create_orgunit(page, app_state=None):
    """조직 추가 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    page.goto(settings.ORG_URLS[settings.ENVIRONMENT])
    if not open_org_add_layer(page):
        return False
    fill_org_info(page, app_state)
    if not click_add_button(page):
        return False
    return True
