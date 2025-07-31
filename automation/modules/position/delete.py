from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Position Delete Page)
# =====================
BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'
BTN_DELETE = 'div.lw_tr:last-of-type button.btn_delete'

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
    rows = page.locator('div.lw_tr')
    if rows.count() > 0:
        last_row = rows.nth(rows.count() - 1)
        btn = last_row.locator('button.btn_delete')
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
def delete_position(page):
    """직책 삭제 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    if not click_edit_button(page):
        return False
    if not click_last_delete_button(page):
        return False
    if not click_save_button(page):
        return False
    return True
