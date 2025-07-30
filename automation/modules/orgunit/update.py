from playwright.sync_api import Page
from datetime import datetime

# 주요 셀렉터 상수
BTN_SEARCH = 'button.btn_search'
INPUT_SEARCH = '#search_input'
ORG_NAME_CELL = 'ul.org_tree.search_result a.group_name'
BTN_MODIFY_ORG = 'div.ly_member_detail button.lw_btn_point:text-is("수정")'
BTN_SAVE = 'div.ly_member_add button.lw_btn_point:text-is("저장")'
INPUT_ORG_NAME = 'input.lw_input[placeholder="조직명"]'
INPUT_ENGLISH = 'input.lw_input[placeholder="English"]'
INPUT_KOREAN = 'input.lw_input[placeholder="Korean"]'
INPUT_CHINESE_TWN = 'input.lw_input[placeholder="Chinese (TWN)"]'
INPUT_JAPANESE = 'input.lw_input[placeholder="Japanese"]'
INPUT_CHINESE_CHN = 'input.lw_input[placeholder="Chinese (CHN)"]'
INPUT_DESCRIPTION = 'input.lw_input[placeholder="설명"]'


def safe_fill(page, selector, value):
    """해당 selector가 존재할 때만 값을 입력한다."""
    if page.locator(selector).count() > 0:
        page.locator(selector).fill(value)


def access_org_detail(page: Page, org_name: str):
    """조직 검색 후 상세 페이지로 진입한다."""
    page.wait_for_selector(BTN_SEARCH, timeout=10000)
    page.locator(BTN_SEARCH).click()
    page.wait_for_selector(INPUT_SEARCH, timeout=10000)
    page.fill(INPUT_SEARCH, org_name)
    page.locator(INPUT_SEARCH).press('Enter')
    page.wait_for_timeout(2000)
    # 검색 결과에서 조직명 클릭
    page.wait_for_selector(ORG_NAME_CELL, timeout=10000)
    page.locator(ORG_NAME_CELL).first.click()
    page.wait_for_selector(BTN_MODIFY_ORG, timeout=10000)
    return page


def update_orgunit_info(page, app_state=None):
    """조직명, 다국어명, 설명 필드의 기존 값 뒤에 '(수정됨)'을 붙여 입력한다."""
    page.wait_for_timeout(2000)
    safe_fill(page, INPUT_ORG_NAME, app_state.org_name + "(수정됨)")
    safe_fill(page, INPUT_ENGLISH, "AutoOrg_EN_(수정됨)")
    safe_fill(page, INPUT_KOREAN, "자동화조직_KR_(수정됨)")
    safe_fill(page, INPUT_CHINESE_TWN, "自動組織_TWN_(수정됨)")
    safe_fill(page, INPUT_JAPANESE, "自動組織_JP_(수정됨)")
    safe_fill(page, INPUT_CHINESE_CHN, "自动组织_CHN_(수정됨)")
    safe_fill(page, INPUT_DESCRIPTION, "자동화로 생성된 조직입니다.(수정됨)")
    return True


def update_orgunit(page: Page, app_state=None):
    """조직 상세 페이지에서 조직 수정 절차를 수행한다."""
    org_name = app_state.org_name if app_state and hasattr(app_state, 'org_name') else None
    if not org_name:
        raise ValueError("app_state.org_name이 필요합니다.")
    access_org_detail(page, org_name)
    page.locator(BTN_MODIFY_ORG).click()
    update_orgunit_info(page, app_state)
    page.wait_for_selector(BTN_SAVE, timeout=5000)
    if page.locator(BTN_SAVE).count() > 0:
        page.wait_for_timeout(2000)
        page.locator(BTN_SAVE).first.click()
        return True
    return False
