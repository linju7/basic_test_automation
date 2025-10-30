from playwright.sync_api import Page
import time

# =====================
# 셀렉터 상수 (OrgUnit Delete Page)
# =====================
BTN_DELETE_ORG = 'div.ly_member_detail button:has-text("조직 삭제")'
DELETE_LAYER = 'div.ly_common.freeplan'
DELETE_CHECKBOXES = f'{DELETE_LAYER} input[type="checkbox"].lw_checkbox'
DELETE_CONFIRM_BUTTON = f'{DELETE_LAYER} button.lw_btn_point:text("확인")'
DELETE_FINISH_BUTTON = 'div.ly_common.freeplan button.lw_btn_point:text("확인")'


def click_delete_button(page):
    """조직 삭제 버튼 클릭"""
    page.locator(BTN_DELETE_ORG).click()
    return True


def check_delete_boxes(page):
    """삭제 확인 레이어 체크박스 전체 클릭"""
    page.wait_for_selector(DELETE_LAYER, timeout=10000)
    delete_boxes = page.locator(DELETE_CHECKBOXES)
    for i in range(delete_boxes.count()):
        delete_boxes.nth(i).scroll_into_view_if_needed()
        delete_boxes.nth(i).click(force=True)
    return True


def confirm_delete(page):
    """삭제 확인 버튼 클릭"""
    page.wait_for_selector(DELETE_CONFIRM_BUTTON, timeout=10000)
    page.locator(DELETE_CONFIRM_BUTTON).click()
    return True


def confirm_delete_finish(page):
    """삭제 완료 확인 버튼 클릭"""
    page.wait_for_selector(DELETE_FINISH_BUTTON, timeout=10000)
    page.locator(DELETE_FINISH_BUTTON).click()
    return True


# =====================
# 메인 플로우 함수
# =====================
def delete_orgunit(page: Page, app_state=None) -> bool:
    """조직 상세 페이지에서 조직 삭제 절차를 수행"""
    print("\n조직 삭제 자동화 시작")
    if not click_delete_button(page):
        print("조직 삭제 자동화 실패 - click_delete_button\n")
        return False
    if not check_delete_boxes(page):
        print("조직 삭제 자동화 실패 - check_delete_boxes\n")
        return False
    if not confirm_delete(page):
        print("조직 삭제 자동화 실패 - confirm_delete\n")
        return False
    if not confirm_delete_finish(page):
        print("조직 삭제 자동화 실패 - confirm_delete_finish\n")
        return False
    print("조직 삭제 자동화 완료\n")
    return True
