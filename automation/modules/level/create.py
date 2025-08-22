from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill, safe_fill_last

# =====================
# 셀렉터 상수 (Level Create Page)
# =====================

BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_ADD_ROW = 'div.lw_tfoot button.btn_add_row:text-is("직급 추가")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'

# 입력 필드 셀렉터
INPUT_LEVEL = 'input.lw_input[placeholder="직급"]'
LANG_FIELD_TEMPLATE = '.lang_field:has(span.lang:text-is("{lang}")) input.lw_input'

# 입력 필드 (가장 마지막 행)
def get_last_level_input(page):
    inputs = page.locator(INPUT_LEVEL)
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None

def get_last_lang_input(page, lang):
    lang_fields = page.locator(LANG_FIELD_TEMPLATE.format(lang=lang))
    if lang_fields.count() > 0:
        return lang_fields.nth(lang_fields.count() - 1)
    return None

# =====================
# 유틸 함수
# =====================
def open_level_page(page):
    page.goto(settings.LEVEL_URLS[settings.ENVIRONMENT])
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
    print("[실패] '직급 추가' 버튼을 찾을 수 없음")
    return False

def fill_level_fields(page, app_state=None):
    timestamp = datetime.now().strftime("%m%d%H%M")
    level_name = f"자동화직급_{timestamp}"
    # 대표명 입력
    input_main = get_last_level_input(page)
    if input_main is not None:
        safe_fill_last(page, INPUT_LEVEL, level_name)
        if app_state is not None:
            app_state.level_name = level_name
    else:
        print("[실패] 직급명 입력란을 찾을 수 없음")
        return False
    # 다국어 입력
    lang_map = {
        "Korean": f"자동화직급KR_{timestamp}",
        "English": f"자동화직급EN_{timestamp}",
        "Japanese": f"자동화직급JP_{timestamp}",
        "Chinese (TWN)": f"자동화직급TW_{timestamp}",
        "Chinese (CHN)": f"자동화직급CH_{timestamp}",
    }
    for lang, value in lang_map.items():
        input_lang = get_last_lang_input(page, lang)
        if input_lang is not None:
            lang_selector = LANG_FIELD_TEMPLATE.format(lang=lang)
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
def create_level(page, app_state=None):
    """직급 추가 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    open_level_page(page)
    if not click_edit_button(page):
        return False
    if not click_add_row_button(page):
        return False
    if not fill_level_fields(page, app_state):
        return False
    if not click_save_button(page):
        return False
    return True
