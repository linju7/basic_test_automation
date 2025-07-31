from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Usertype Delete Page)
# =====================
BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'
BTN_DELETE = 'div.lw_tr:last-of-type button.btn_delete'
# 저장 확인 레이어
SAVE_CONFIRM_LAYER = 'div.ly_common.freeplan'
BTN_CONFIRM_SAVE = 'div.ly_common.freeplan button.lw_btn_point:text-is("확인")'

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
            page.wait_for_timeout(2000)
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

def confirm_save_changes(page):
    """저장 후 나타나는 확인 레이어에서 '확인' 버튼 클릭"""
    try:
        page.wait_for_selector(SAVE_CONFIRM_LAYER, timeout=10000)
        btn_confirm = page.locator(BTN_CONFIRM_SAVE)
        if btn_confirm.count() > 0:
            btn_confirm.first.click()
            return True
        else:
            print("[실패] 저장 확인 버튼을 찾을 수 없음")
            return False
    except Exception as e:
        print(f"[예외] 저장 확인 처리 중 오류 발생: {e}")
        return False

# =====================
# 메인 플로우 함수
# =====================
def delete_status(page):
    """상태 삭제 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    if not click_edit_button(page):
        return False
    if not click_last_delete_button(page):
        return False
    if not click_save_button(page):
        return False
    if not confirm_save_changes(page):
        return False
    return True
