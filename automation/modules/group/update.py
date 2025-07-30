from playwright.sync_api import Page
import time

# 주요 셀렉터 상수
BTN_SEARCH = 'button.btn_search'
INPUT_SEARCH = '#group_search_input'
GROUP_NAME_CELL = 'strong.ellipsis_element'
BTN_MODIFY_GROUP = 'div.ly_member_detail button.lw_btn_point:text-is("수정")'
BTN_SAVE = 'div.ly_member_add button.lw_btn_point:text-is("저장")'
INPUT_GROUP_NAME = 'input.lw_input[placeholder="그룹명"]'


def access_group_detail(page: Page, group_name: str):
    """그룹 검색 후 상세 페이지로 진입한다."""
    page.wait_for_selector(BTN_SEARCH, timeout=10000)
    page.locator(BTN_SEARCH).click()
    page.wait_for_selector(INPUT_SEARCH, timeout=10000)
    page.fill(INPUT_SEARCH, group_name)
    page.wait_for_timeout(2000)
    page.locator(INPUT_SEARCH).press('Enter')
    page.wait_for_timeout(2000)
    # 검색 결과에서 그룹명 클릭
    page.wait_for_selector(GROUP_NAME_CELL, timeout=10000)
    page.locator(GROUP_NAME_CELL).first.click()
    page.wait_for_selector(BTN_MODIFY_GROUP, timeout=10000)
    page.wait_for_timeout(3000)
    return page


def update_group_info(page: Page, app_state=None):
    """그룹명 입력 필드의 기존 값 뒤에 '(수정됨)'을 붙인다."""
    if page.locator(INPUT_GROUP_NAME).count() > 0:
        new_value = app_state.group_name + "(수정됨)"
        page.locator(INPUT_GROUP_NAME).fill(new_value)
        if app_state is not None:
            app_state.group_name = new_value
    return page


def update_group(page: Page, app_state=None):
    """그룹 정보 수정 플로우를 순차적으로 실행한다. 저장 버튼 클릭 시 True 반환."""
    group_name = app_state.group_name if app_state and hasattr(app_state, 'group_name') else None
    if not group_name:
        raise ValueError("app_state.group_name이 필요합니다.")
    access_group_detail(page, group_name)
    page.locator(BTN_MODIFY_GROUP).click()
    update_group_info(page, app_state)
    # 저장 버튼이 활성화될 때까지 대기 후 클릭
    page.wait_for_selector(BTN_SAVE, timeout=5000)
    if page.locator(BTN_SAVE).count() > 0:
        page.wait_for_timeout(3000)
        page.locator(BTN_SAVE).first.click()
        page.wait_for_timeout(2000)
        return True
    return False