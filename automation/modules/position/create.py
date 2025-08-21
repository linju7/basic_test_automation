from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (Position Create Page)
# =====================

BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_ADD_ROW = 'div.lw_tfoot button.btn_add_row:text-is("직책 추가")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'

def get_last_position_input(page):
    """마지막 직책 입력란 찾기"""
    inputs = page.locator('input.lw_input[placeholder="직책"]')
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None


def get_last_lang_input(page, lang):
    """마지막 언어별 입력란 찾기"""
    lang_fields = page.locator(f'.lang_field:has(span.lang:text-is("{lang}")) input.lw_input')
    if lang_fields.count() > 0:
        return lang_fields.nth(lang_fields.count() - 1)
    return None


def open_position_page(page):
    """직책 관리 페이지 열기"""
    page.goto(settings.POSITION_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_EDIT, timeout=5000)
    return True


def click_edit_button(page):
    """수정 버튼 클릭"""
    btn = page.locator(BTN_EDIT)
    if btn.count() > 0:
        btn.first.click()
        return True
    return False


def click_add_row_button(page):
    """직책 추가 버튼 클릭"""
    btn = page.locator(BTN_ADD_ROW)
    if btn.count() > 0:
        btn.first.click()
        return True
    return False

def fill_position_fields(page, app_state=None):
    """직책 정보 입력 폼을 채우기"""
    # 유니크한 값 세팅을 위해 현재 시간값 사용
    timestamp = datetime.now().strftime("%m%d%H%M")
    position_name = f"자동화직책_{timestamp}"
    
    # 대표명 입력
    input_main = get_last_position_input(page)
    if input_main is not None:
        input_main.fill(position_name)
        if app_state is not None:
            app_state.position_name = position_name
    else:
        return False
    
    # 다국어 필드 입력
    lang_map = {
        "Korean": f"자동화직책KR_{timestamp}",
        "English": f"자동화직책EN_{timestamp}",
        "Japanese": f"자동화직책JP_{timestamp}",
        "Chinese (TWN)": f"자동화직책TW_{timestamp}",
        "Chinese (CHN)": f"자동화직책CH_{timestamp}",
    }
    
    for lang, value in lang_map.items():
        input_lang = get_last_lang_input(page, lang)
        if input_lang is not None:
            input_lang.fill(value)
        else:
            return False
    
    return True

def click_save_button(page):
    """저장 버튼 클릭"""
    btn = page.locator(BTN_SAVE)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(BTN_EDIT, timeout=5000)
        return True
    return False

# =====================
# 메인 플로우 함수
# =====================
def create_position(page, app_state=None):
    """직책 추가 플로우를 순차적으로 실행"""
    if not open_position_page(page):
        return False
    if not click_edit_button(page):
        return False
    if not click_add_row_button(page):
        return False
    if not fill_position_fields(page, app_state):
        return False
    if not click_save_button(page):
        return False
    return True
