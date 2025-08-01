from automation.config.settings import settings
from datetime import datetime

# =====================
# 셀렉터 상수 (Status Page)
# =====================
BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'

# 저장 확인 레이어
SAVE_CONFIRM_LAYER = 'div.ly_common.freeplan'
BTN_CONFIRM_SAVE = 'div.ly_common.freeplan button.lw_btn_point:text-is("확인")'

# =====================
# 입력 필드 관련 함수
# =====================
def get_last_status_input(page):
    inputs = page.locator('input.lw_input[placeholder="상태"]')
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None

def get_last_lang_input(page, lang):
    selector = f'div.lang_field:has-text("{lang}") input.lw_input'
    inputs = page.locator(selector)
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None

# =====================
# 유틸 함수
# =====================
def open_status_page(page):
    page.goto(settings.STATUS_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_EDIT, timeout=5000)

def click_edit_button(page):
    btn = page.locator(BTN_EDIT)
    if btn.count() > 0:
        btn.first.click()
        return True
    print("[실패] '수정' 버튼을 찾을 수 없음")
    return False

def fill_status_fields_for_update(page, app_state=None):
    timestamp = datetime.now().strftime("%m%d%H%M")
    status_name = f"자동화상태_{timestamp}_수정"

    input_main = get_last_status_input(page)
    if input_main is not None:
        input_main.fill(status_name)
        if app_state is not None:
            app_state.status_name = status_name
    else:
        print("[실패] 상태명 입력란을 찾을 수 없음")
        return False

    page.wait_for_timeout(1000)

    lang_map = {
        "Korean": f"자동화상태KR_{timestamp}_수정",
        "English": f"자동화상태EN_{timestamp}_수정",
        "Japanese": f"자동화상태JP_{timestamp}_수정",
        "Chinese (TWN)": f"자동화상태TW_{timestamp}_수정",
        "Chinese (CHN)": f"자동화상태CH_{timestamp}_수정",
    }

    for lang, value in lang_map.items():
        try:
            input_lang = get_last_lang_input(page, lang)
            if input_lang is not None:
                input_lang.fill(value)
            else:
                print(f"[실패] {lang} 입력란을 찾을 수 없음")
                return False
        except Exception as e:
            print(f"[예외] {lang} 입력 처리 중 오류 발생: {e}")
            return False

    return True

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
# 메인 플로우 함수 (수정용)
# =====================
def update_status(page, app_state=None):
    """마지막 상태 항목을 수정한다. 성공 시 True, 실패 시 False 반환."""
    if not click_edit_button(page):
        return False
    if not fill_status_fields_for_update(page, app_state):
        return False
    if not click_save_button(page):
        return False
    if not confirm_save_changes(page):
        return False
    return True