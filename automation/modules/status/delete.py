from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Status Delete Page)
# =====================
BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'

# 테이블 행과 삭제 버튼
DATA_ROWS = 'div.lw_tr:not(.thead)'
BTN_DELETE = 'button.btn_delete'
# 저장 확인 레이어
SAVE_CONFIRM_LAYER = 'div.ly_common.freeplan'
BTN_CONFIRM_SAVE = 'div.ly_common.freeplan button.lw_btn_point:text-is("확인")'

def open_status_page(page):
    """상태 관리 페이지 열기"""
    page.goto(settings.STATUS_URLS[settings.ENVIRONMENT])
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
    """마지막 데이터 행의 삭제 버튼 클릭"""
    # thead가 아닌 데이터 행만 찾기 (tfoot 제외)
    data_rows = page.locator(DATA_ROWS)
    if data_rows.count() > 0:
        last_data_row = data_rows.nth(data_rows.count() - 1)
        btn = last_data_row.locator(BTN_DELETE)
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(2000)
            return True
    return False


def click_save_button(page):
    """저장 버튼 클릭"""
    btn = page.locator(BTN_SAVE)
    if btn.count() > 0:
        btn.first.click()
        return True
    return False


def confirm_save_changes(page):
    """저장 후 확인 레이어에서 확인 버튼 클릭"""
    try:
        page.wait_for_selector(SAVE_CONFIRM_LAYER, timeout=10000)
        btn_confirm = page.locator(BTN_CONFIRM_SAVE)
        if btn_confirm.count() > 0:
            btn_confirm.first.click()
            return True
        else:
            return False
    except Exception:
        return False

# =====================
# 메인 플로우 함수
# =====================
def delete_status(page, app_state=None):
    """상태 삭제 플로우를 순차적으로 실행"""
    if not open_status_page(page):
        return False
    if not click_edit_button(page):
        return False
    if not click_last_delete_button(page):
        return False
    if not click_save_button(page):
        return False
    if not confirm_save_changes(page):
        return False
    return True
