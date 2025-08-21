from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Position Delete Page)
# =====================
BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'
BTN_DELETE = 'div.lw_tr:last-of-type button.btn_delete'

def open_position_page(page):
    """직책 관리 페이지 열기"""
    page.goto(settings.POSITION_URLS[settings.ENVIRONMENT])
    return True


def click_edit_button(page):
    """수정 버튼 클릭"""
    page.wait_for_selector(BTN_EDIT, timeout=5000)
    btn = page.locator(BTN_EDIT)
    if btn.count() > 0:
        btn.first.click()
        return True
    return False


def click_last_delete_button(page):
    """마지막 행의 삭제 버튼 클릭"""
    rows = page.locator('div.lw_tr')
    if rows.count() > 0:
        last_row = rows.nth(rows.count() - 1)
        btn = last_row.locator('button.btn_delete')
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(5000)
            return True
    return False


def click_save_button(page):
    """저장 버튼 클릭"""
    btn = page.locator(BTN_SAVE)
    if btn.count() > 0:
        btn.first.click()
        return True
    return False

# =====================
# 메인 플로우 함수
# =====================
def delete_position(page, app_state=None):
    """직책 삭제 플로우를 순차적으로 실행"""
    if not open_position_page(page):
        return False
    if not click_edit_button(page):
        return False
    if not click_last_delete_button(page):
        return False
    if not click_save_button(page):
        return False
    return True
