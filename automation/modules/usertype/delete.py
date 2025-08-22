from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Usertype Delete Page)
# =====================
BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'

# 테이블 행과 삭제 버튼
DATA_ROWS = 'div.lw_tr:not(.thead)'
BTN_DELETE = 'button.btn_delete'

# =====================
# 유틸 함수
# =====================
def click_edit_button(page):
    page.wait_for_selector(BTN_EDIT, timeout=5000)
    btn = page.locator(BTN_EDIT)
    if btn.count() > 0:
        btn.first.click()
        return True
    print("[실패] '수정' 버튼을 찾을 수 없음")
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
            page.wait_for_timeout(5000)
            return True
    print("[실패] 마지막 행의 '삭제' 버튼을 찾을 수 없음")
    return False

def click_save_button(page):
    btn = page.locator(BTN_SAVE)
    if btn.count() > 0:
        btn.first.click()
        return True
    print("[실패] '저장' 버튼을 찾을 수 없음")
    return False

# =====================
# 메인 플로우 함수
# =====================
def delete_usertype(page):
    """사용자유형 삭제 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    if not click_edit_button(page):
        return False
    if not click_last_delete_button(page):
        return False
    if not click_save_button(page):
        return False
    return True
