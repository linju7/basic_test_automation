from playwright.sync_api import Page
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (OrgUnit Update Page)
# =====================
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





def access_org_detail(page: Page, org_name: str):
    """조직 검색 후 상세 페이지로 진입"""
    page.wait_for_selector(BTN_SEARCH, timeout=10000)
    page.locator(BTN_SEARCH).click()
    page.wait_for_selector(INPUT_SEARCH, timeout=10000)
    safe_fill(page, INPUT_SEARCH, org_name)
    page.locator(INPUT_SEARCH).press('Enter')
    page.wait_for_timeout(2000)
    # 검색 결과에서 조직명 클릭
    page.wait_for_selector(ORG_NAME_CELL, timeout=10000)
    page.locator(ORG_NAME_CELL).first.click()
    page.wait_for_selector(BTN_MODIFY_ORG, timeout=10000)
    return True


def click_modify_button(page):
    """수정 버튼 클릭"""
    page.locator(BTN_MODIFY_ORG).click()
    return True


def update_orgunit_info(page, app_state=None):
    """조직 정보 수정 폼을 채우기"""
    page.wait_for_timeout(2000)
    
    safe_fill(page, INPUT_ORG_NAME, app_state.org_name + "(수정됨)")
    safe_fill(page, INPUT_ENGLISH, "AutoOrg_EN_(수정됨)")
    safe_fill(page, INPUT_KOREAN, "자동화조직_KR_(수정됨)")
    safe_fill(page, INPUT_CHINESE_TWN, "自動組織_TWN_(수정됨)")
    safe_fill(page, INPUT_JAPANESE, "自動組織_JP_(수정됨)")
    safe_fill(page, INPUT_CHINESE_CHN, "自动组织_CHN_(수정됨)")
    safe_fill(page, INPUT_DESCRIPTION, "자동화로 생성된 조직입니다.(수정됨)")
    
    return True


def click_save_button(page):
    """저장 버튼 클릭"""
    page.wait_for_selector(BTN_SAVE, timeout=5000)
    if page.locator(BTN_SAVE).count() > 0:
        page.wait_for_timeout(2000)
        page.locator(BTN_SAVE).first.click()
        return True
    return False


# =====================
# 메인 플로우 함수
# =====================
def update_orgunit(page: Page, app_state=None):
    """조직 상세 페이지에서 조직 수정 절차를 수행"""
    org_name = app_state.org_name if app_state and hasattr(app_state, 'org_name') else None
    if not org_name:
        raise ValueError("app_state.org_name이 필요합니다.")
    
    if not access_org_detail(page, org_name):
        return False
    if not click_modify_button(page):
        return False
    if not update_orgunit_info(page, app_state):
        return False
    if not click_save_button(page):
        return False
    return True
