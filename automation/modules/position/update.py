from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Position Update Page)
# =====================
BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'

def get_last_position_input(page):
    inputs = page.locator('input.lw_input[placeholder="직책"]')
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None

def get_last_lang_input(page, lang):
    lang_fields = page.locator(f'.lang_field:has(span.lang:text-is("{lang}")) input.lw_input')
    if lang_fields.count() > 0:
        return lang_fields.nth(lang_fields.count() - 1)
    return None

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

def fill_position_update_fields(page, app_state=None):
    from datetime import datetime
    timestamp = datetime.now().strftime("%m%d%H%M")
    position_name = f"자동화직책_{timestamp}_수정"
    # 대표명 입력
    input_main = get_last_position_input(page)
    if input_main is not None:
        input_main.click()
        input_main.fill(position_name)
        if app_state is not None:
            app_state.position_name = position_name
    else:
        print("[실패] 직책명 입력란을 찾을 수 없음")
        return False
    # 다국어 입력
    lang_map = {
        "Korean": f"자동화직책KR_{timestamp}_수정",
        "English": f"자동화직책EN_{timestamp}_수정",
        "Japanese": f"자동화직책JP_{timestamp}_수정",
        "Chinese (TWN)": f"자동화직책TW_{timestamp}_수정",
        "Chinese (CHN)": f"자동화직책CH_{timestamp}_수정",
    }
    for lang, value in lang_map.items():
        input_lang = get_last_lang_input(page, lang)
        if input_lang is not None:
            input_lang.click()
            input_lang.fill(value)
        else:
            print(f"[실패] {lang} 입력란을 찾을 수 없음")
            return False
    return True

def click_save_button(page):
    btn = page.locator(BTN_SAVE)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(BTN_EDIT, timeout=5000)
        return True
    print("[실패] '저장' 버튼을 찾을 수 없음")
    return False

# =====================
# 메인 플로우 함수
# =====================
def update_position(page, app_state=None):
    """직책 수정 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    if not click_edit_button(page):
        return False
    if not fill_position_update_fields(page, app_state):
        return False
    if not click_save_button(page):
        return False
    return True
