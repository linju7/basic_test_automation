from automation.config.settings import settings
from playwright.sync_api import Page

# 주요 셀렉터 상수
BTN_MANAGE = 'button.lw_btn_drop.btn_more'
DROPDOWN_OPEN = 'div.btn_combo .ly_context[style*="display: block"]'
DROPDOWN_DELETE = 'div.ly_context a:text("계정 삭제")'
DELETE_LAYER = 'div.ly_common.ly_page'
DELETE_LAYER_CHECKBOX = 'div.ly_common.ly_page input[type="checkbox"].lw_checkbox'
BTN_ALERT_DELETE = 'div.ly_common.ly_page button.lw_btn_alert:not([disabled])'
BTN_PERMANENT_DELETE = 'a.btn_action:text("영구 삭제")'
PERMANENT_DELETE_LAYER = 'div.ly_common.freeplan'
BTN_PERMANENT_CONFIRM = 'div.ly_common.freeplan button.lw_btn_point:text("예")'


def click_manage_button(page: Page):
    BTN_MANAGE = 'button.lw_btn_drop.btn_more'

    # 1. 관리 버튼 클릭
    page.wait_for_selector(BTN_MANAGE, timeout=10000)
    btns = page.locator(BTN_MANAGE).filter(visible=True)
    print(f"[delete_user] 관리버튼 개수: {btns.count()}")
    btns.first.click()

    # 2. 드롭다운이 펼쳐졌는지(클래스에 on이 붙었는지) 확인
    BTN_MANAGE_ON = 'button.lw_btn_drop.btn_more.on'
    page.wait_for_selector(BTN_MANAGE_ON, timeout=5000)
    print("[delete_user] 관리버튼 드롭다운 on 상태 확인!")


def click_delete_in_dropdown(page: Page):
    """드롭다운에서 계정 삭제를 클릭한다."""
    page.wait_for_selector(DROPDOWN_DELETE, timeout=10000)
    page.locator(DROPDOWN_DELETE).click()


def check_all_delete_layer_checkboxes(page: Page):
    """삭제 레이어 내 모든 체크박스를 클릭한다."""
    page.wait_for_selector(DELETE_LAYER, timeout=10000)
    checkboxes = page.locator(DELETE_LAYER_CHECKBOX).all()
    for checkbox in checkboxes:
        checkbox.scroll_into_view_if_needed()
        checkbox.click(force=True)


def confirm_delete(page: Page):
    """삭제 버튼이 활성화될 때까지 대기 후 클릭한다."""
    page.wait_for_selector(BTN_ALERT_DELETE, timeout=10000)
    page.locator(BTN_ALERT_DELETE).click()


def permanent_delete(page: Page):
    """'영구 삭제' 버튼 클릭 및 '예'로 최종 삭제한다."""
    page.wait_for_selector(BTN_PERMANENT_DELETE, timeout=10000)
    page.locator(BTN_PERMANENT_DELETE).click()
    page.wait_for_selector(PERMANENT_DELETE_LAYER, timeout=10000)
    page.wait_for_selector(BTN_PERMANENT_CONFIRM, timeout=10000)
    page.locator(BTN_PERMANENT_CONFIRM).click()


def delete_user(page: Page, app_state=None):
    """
    상세 페이지(이미 진입 상태)에서 관리버튼 → 계정 삭제 → 레이어 체크박스 모두 클릭 → 삭제 → 영구 삭제까지 순차 실행.
    성공 시 True, 실패 시 False 반환.
    """
    try:
        print("[delete_user] 관리 버튼 클릭")
        click_manage_button(page)
        print("[delete_user] 드롭다운에서 계정 삭제 클릭")
        click_delete_in_dropdown(page)
        print("[delete_user] 삭제 레이어 체크박스 모두 클릭")
        check_all_delete_layer_checkboxes(page)
        print("[delete_user] 삭제 버튼 클릭")
        confirm_delete(page)
        print("[delete_user] 영구 삭제 버튼 클릭 및 최종 삭제")
        permanent_delete(page)
        print("[delete_user] 완료!")
        return True
    except Exception as e:
        print(f"[delete_user] 실패: {e}")
        return False


