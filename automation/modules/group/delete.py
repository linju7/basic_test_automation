from playwright.sync_api import Page

# 주요 셀렉터 상수
BTN_DELETE_GROUP = 'div.ly_member_detail button:has-text("그룹 삭제")'
DELETE_LAYER = 'div.ly_common.freeplan'
DELETE_CHECKBOXES = f'{DELETE_LAYER} input[type="checkbox"].lw_checkbox'
DELETE_CONFIRM_BUTTON = f'{DELETE_LAYER} button.lw_btn_point:text("확인")'


def delete_group(page: Page) -> bool:
    """
    그룹 상세 페이지에서 그룹 삭제 절차를 수행한다.
    성공 시 True, 실패 시 False 반환.
    """
    page.locator(BTN_DELETE_GROUP).click()
    # 삭제 확인 레이어 체크박스 전체 클릭
    page.wait_for_selector(DELETE_LAYER, timeout=10000)
    delete_boxes = page.locator(DELETE_CHECKBOXES)
    for i in range(delete_boxes.count()):
        delete_boxes.nth(i).scroll_into_view_if_needed()
        delete_boxes.nth(i).click(force=True)
    # '확인' 버튼 클릭
    page.wait_for_selector(DELETE_CONFIRM_BUTTON, timeout=10000)
    page.locator(DELETE_CONFIRM_BUTTON).click()
    return True
