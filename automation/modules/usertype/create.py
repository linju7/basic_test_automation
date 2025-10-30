from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill, safe_fill_last

# =====================
# 셀렉터 상수 (Usertype Create Page)
# =====================

BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_ADD_ROW = 'div.lw_tfoot button.btn_add_row'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'

# 입력 필드 (가장 마지막 행)
LAST_ROW = 'div.lw_table.tb_cols_multihead.modify > div.lw_tr:last-of-type'
INPUT_USERTYPE_NAME = f'{LAST_ROW} input.lw_input[placeholder="사용자 유형"]'
INPUT_LANG_FIELD = lambda lang: f'{LAST_ROW} .lang_field:has(span.lang:text-is("{lang}")) input.lw_input'

# =====================
# 유틸 함수
# =====================
def open_usertype_page(page):
    page.goto(settings.USERTYPE_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_EDIT, timeout=5000)

def click_edit_button(page):
    btn = page.locator(BTN_EDIT)
    if btn.count() > 0:
        btn.first.click()
        return True
    print("[실패] '수정' 버튼을 찾을 수 없음")
    return False

def click_add_row_button(page):
    btn = page.locator(BTN_ADD_ROW)
    if btn.count() > 0:
        btn.first.click()
        return True
    print("[실패] '사용자 유형 추가' 버튼을 찾을 수 없음")
    return False

def get_empty_usertype_input(page):
    inputs = page.locator('input.lw_input[placeholder="사용자 유형"]')
    for i in range(inputs.count()):
        if inputs.nth(i).input_value() == "":
            return inputs.nth(i)
    return None

def get_empty_lang_input(page, lang):
    lang_fields = page.locator(f'.lang_field:has(span.lang:text-is("{lang}")) input.lw_input')
    for i in range(lang_fields.count()):
        if lang_fields.nth(i).input_value() == "":
            return lang_fields.nth(i)
    return None

def get_last_usertype_input(page):
    inputs = page.locator('input.lw_input[placeholder="사용자 유형"]')
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None

def get_last_lang_input(page, lang):
    lang_fields = page.locator(f'.lang_field:has(span.lang:text-is("{lang}")) input.lw_input')
    if lang_fields.count() > 0:
        return lang_fields.nth(lang_fields.count() - 1)
    return None

def fill_usertype_fields(page, app_state=None):
    timestamp = datetime.now().strftime("%m%d%H%M")
    usertype_name = f"자동화유형_{timestamp}"
    # 대표명 입력
    input_main = get_last_usertype_input(page)
    if input_main is not None:
        safe_fill_last(page, 'input.lw_input[placeholder="사용자 유형"]', usertype_name)
        if app_state is not None:
            app_state.usertype_name = usertype_name
    else:
        print("[실패] 사용자 유형명 입력란을 찾을 수 없음")
        return False
    # 다국어 입력
    lang_map = {
        "Korean": f"자동화유형KR_{timestamp}",
        "English": f"자동화유형EN_{timestamp}",
        "Japanese": f"자동화유형JP_{timestamp}",
        "Chinese (TWN)": f"자동화유형TW_{timestamp}",
        "Chinese (CHN)": f"자동화유형CH_{timestamp}",
    }
    for lang, value in lang_map.items():
        input_lang = get_last_lang_input(page, lang)
        if input_lang is not None:
            lang_selector = f'.lang_field:has(span.lang:text-is("{lang}")) input.lw_input'
            safe_fill_last(page, lang_selector, value)
        else:
            print(f"[실패] {lang} 입력란을 찾을 수 없음")
            return False
    return True

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
def create_usertype(page, app_state=None):
    """사용자 유형 추가 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    print("\n사용자 유형 추가 자동화 시작")
    open_usertype_page(page)
    if not click_edit_button(page):
        print("사용자 유형 추가 자동화 실패 - click_edit_button\n")
        return False
    if not click_add_row_button(page):
        print("사용자 유형 추가 자동화 실패 - click_add_row_button\n")
        return False
    if not fill_usertype_fields(page, app_state):
        print("사용자 유형 추가 자동화 실패 - fill_usertype_fields\n")
        return False
    if not click_save_button(page):
        print("사용자 유형 추가 자동화 실패 - click_save_button\n")
        return False
    print("사용자 유형 추가 자동화 완료\n")
    return True
