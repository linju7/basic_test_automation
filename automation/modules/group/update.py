from playwright.sync_api import Page
import time

# =====================
# 셀렉터 상수 (Group Update Page)
# =====================
BTN_MODIFY_GROUP = 'div.ly_member_detail button.lw_btn_point:text-is("수정")'
BTN_SAVE = 'div.ly_member_add button.lw_btn_point:text-is("저장")'
INPUT_GROUP_NAME = 'input.lw_input[placeholder="그룹명"]'
INPUT_DESCRIPTION = 'input.lw_input[placeholder="설명"]'
INPUT_MAILING_LIST = 'input.lw_input.w_limit[placeholder="ID"]'


def click_modify_button(page):
    """그룹 수정 버튼 클릭"""
    page.wait_for_selector(BTN_MODIFY_GROUP, timeout=10000)
    page.wait_for_timeout(3000)
    page.locator(BTN_MODIFY_GROUP).click()
    return True


def update_group_info(page: Page, app_state=None):
    """모든 그룹 정보 필드를 수정"""
    # 그룹명 수정
    if page.locator(INPUT_GROUP_NAME).count() > 0:
        new_value = app_state.group_name + "(수정됨)"
        page.locator(INPUT_GROUP_NAME).fill(new_value)
        if app_state is not None:
            app_state.group_name = new_value
            if hasattr(app_state, 'group_info') and app_state.group_info:
                app_state.group_info['group_name'] = new_value
    
    # 설명 수정
    if page.locator(INPUT_DESCRIPTION).count() > 0:
        if app_state and hasattr(app_state, 'group_info') and app_state.group_info:
            original_description = app_state.group_info.get('description', '')
            new_description = original_description + "_수정"
            page.locator(INPUT_DESCRIPTION).fill(new_description)
            app_state.group_info['description'] = new_description
    
    # 메일링 리스트 수정
    if page.locator(INPUT_MAILING_LIST).count() > 0:
        if app_state and hasattr(app_state, 'group_info') and app_state.group_info:
            original_mailing = app_state.group_info.get('mailing_id', '')
            new_mailing = original_mailing + "_00"
            page.locator(INPUT_MAILING_LIST).fill('')
            page.locator(INPUT_MAILING_LIST).fill(new_mailing)
            app_state.group_info['mailing_id'] = new_mailing
    
    return True


def click_save_button(page):
    """저장 버튼 클릭"""
    page.wait_for_selector(BTN_SAVE, timeout=5000)
    if page.locator(BTN_SAVE).count() > 0:
        page.wait_for_timeout(3000)
        page.locator(BTN_SAVE).first.click()
        page.wait_for_timeout(2000)
        return True
    return False


# =====================
# 메인 플로우 함수
# =====================
def update_group(page: Page, app_state=None):
    """그룹 정보 수정 플로우를 순차적으로 실행"""
    group_name = app_state.group_name if app_state and hasattr(app_state, 'group_name') else None
    if not group_name:
        raise ValueError("app_state.group_name이 필요합니다.")
    
    if not click_modify_button(page):
        return False
    if not update_group_info(page, app_state):
        return False
    if not click_save_button(page):
        return False
    return True