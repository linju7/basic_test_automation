from automation.config.settings import settings
from playwright.sync_api import Page

# =====================
# 셀렉터 상수 (User Delete Page)
# =====================

# 관리 메뉴 및 삭제 관련 셀렉터
MANAGE_BUTTON = 'div.btn_combo:has-text("계정 삭제") >> button:has-text("관리")'
DROPDOWN_DELETE = 'div.ly_context a:text("계정 삭제")'

# 삭제 확인 레이어
DELETE_LAYER = 'div.ly_common'
DELETE_CHECKBOXES = f'{DELETE_LAYER} input[type="checkbox"].lw_checkbox'
DELETE_CONFIRM_BUTTON = f'{DELETE_LAYER} button.lw_btn_alert:not([disabled])'

# 영구 삭제 관련 셀렉터
PERMANENT_DELETE_MENU = 'div.ly_context a:text("계정 영구 삭제")'
PERMANENT_LAYER = 'div.ly_common.freeplan'
PERMANENT_CHECKBOXES = f'{PERMANENT_LAYER} input[type="checkbox"].lw_checkbox'
PERMANENT_CONFIRM_BUTTON = 'div.ly_common button.lw_btn_point:text("예")'
PERMANENT_FINISH_BUTTON = 'div.ly_common button.lw_btn_point:text("확인")'


def open_manage_menu(page):
    """관리 메뉴 열기"""
    page.wait_for_selector(MANAGE_BUTTON, timeout=10000)
    page.locator(MANAGE_BUTTON).click()
    return True


def click_account_delete(page):
    """계정 삭제 메뉴 클릭"""
    page.wait_for_selector(DROPDOWN_DELETE, timeout=10000)
    page.locator(DROPDOWN_DELETE).click()
    return True


def check_delete_boxes(page):
    """삭제 체크박스 전체 클릭"""
    page.wait_for_selector(DELETE_LAYER, timeout=20000)
    delete_boxes = page.locator(DELETE_CHECKBOXES)
    for i in range(delete_boxes.count()):
        delete_boxes.nth(i).scroll_into_view_if_needed()
        delete_boxes.nth(i).click(force=True)
    return True


def click_delete_confirm(page):
    """삭제 확인 버튼 클릭"""
    page.wait_for_selector(DELETE_CONFIRM_BUTTON, timeout=10000)
    page.locator(DELETE_CONFIRM_BUTTON).click()
    return True


def click_permanent_delete(page):
    """영구 삭제 메뉴 클릭"""
    page.wait_for_selector(PERMANENT_DELETE_MENU, timeout=10000)
    page.locator(PERMANENT_DELETE_MENU).click()
    return True


def check_permanent_boxes(page):
    """영구 삭제 체크박스 전체 클릭"""
    page.wait_for_selector(PERMANENT_LAYER, timeout=10000)
    perm_boxes = page.locator(PERMANENT_CHECKBOXES)
    for i in range(perm_boxes.count()):
        perm_boxes.nth(i).scroll_into_view_if_needed()
        perm_boxes.nth(i).click(force=True)
    return True


def confirm_permanent_delete(page):
    """영구 삭제 확인"""
    page.wait_for_selector(PERMANENT_CONFIRM_BUTTON, timeout=10000)
    page.locator(PERMANENT_CONFIRM_BUTTON).click()
    
    page.wait_for_selector(PERMANENT_FINISH_BUTTON, timeout=10000)
    page.locator(PERMANENT_FINISH_BUTTON).click()
    return True


# =====================
# 메인 플로우 함수
# =====================
def delete_user(page: Page, app_state=None) -> bool:
    """구성원 상세 페이지에서 계정 삭제 및 영구 삭제 절차를 수행"""

    # 계정 삭제
    if not open_manage_menu(page):
        return False
    if not click_account_delete(page):
        return False
    if not check_delete_boxes(page):
        return False
    if not click_delete_confirm(page):
        return False
    
    # 영구 삭제
    if not open_manage_menu(page):
        return False
    if not click_permanent_delete(page):
        return False
    if not check_permanent_boxes(page):
        return False
    if not confirm_permanent_delete(page):
        return False
    
    return True