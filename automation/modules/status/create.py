from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill, safe_fill_last

# =====================
# 셀렉터 상수 (Status Create Page)
# =====================
BTN_EDIT = 'div.task_area button.lw_btn:text-is("수정")'
BTN_ADD_ROW = 'div.lw_tfoot button.btn_add_row:text-is("상태 추가")'
BTN_SAVE = 'div.task_area button.lw_btn_point:text-is("저장")'

# 입력 필드 셀렉터
INPUT_STATUS = 'input.lw_input[placeholder="상태"]'
LANG_FIELD_TEMPLATE = '.lang_field:has(span.lang:text-is("{lang}")) input.lw_input'

# 저장 확인 레이어
SAVE_CONFIRM_LAYER = 'div.ly_common.freeplan'
BTN_CONFIRM_SAVE = 'div.ly_common.freeplan button.lw_btn_point:text-is("확인")'

def get_last_status_input(page):
    """마지막 상태 입력란 찾기"""
    inputs = page.locator('input.lw_input[placeholder="상태"]')
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None


def get_last_lang_input(page, lang):
    """마지막 언어별 입력란 찾기"""
    selector = f'div.lang_field:has-text("{lang}") input.lw_input'
    inputs = page.locator(selector)
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None


def open_status_page(page):
    """상태 관리 페이지 열기"""
    page.goto(settings.STATUS_URLS[settings.ENVIRONMENT])
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
    """상태 추가 버튼 클릭"""
    btn = page.locator(BTN_ADD_ROW)
    if btn.count() > 0:
        btn.first.click()
        return True
    return False

def fill_status_fields(page, app_state=None):
    """상태 정보 입력 폼을 채우기"""
    # 유니크한 값 세팅을 위해 현재 시간값 사용
    timestamp = datetime.now().strftime("%m%d%H%M")
    status_name = f"자동화상태_{timestamp}"

    # 주 상태명 입력
    input_main = get_last_status_input(page)
    if input_main is not None:
        safe_fill_last(page, INPUT_STATUS, status_name)
        if app_state is not None:
            app_state.status_name = status_name
    else:
        return False

    page.wait_for_timeout(1000)

    # 다국어 필드 입력
    lang_map = {
        "Korean": f"자동화상태KR_{timestamp}",
        "English": f"자동화상태EN_{timestamp}",
        "Japanese": f"자동화상태JP_{timestamp}",
        "Chinese (TWN)": f"자동화상태TW_{timestamp}",
        "Chinese (CHN)": f"자동화상태CH_{timestamp}",
    }

    for lang, value in lang_map.items():
        try:
            input_lang = get_last_lang_input(page, lang)
            if input_lang is not None:
                lang_selector = LANG_FIELD_TEMPLATE.format(lang=lang)
                safe_fill_last(page, lang_selector, value)
            else:
                return False
        except Exception:
            return False

    return True

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
def create_status(page, app_state=None):
    """상태 추가 플로우를 순차적으로 실행"""
    print("\n상태 추가 자동화 시작")
    if not open_status_page(page):
        print("상태 추가 자동화 실패 - open_status_page\n")
        return False
    if not click_edit_button(page):
        print("상태 추가 자동화 실패 - click_edit_button\n")
        return False
    if not click_add_row_button(page):
        print("상태 추가 자동화 실패 - click_add_row_button\n")
        return False
    if not fill_status_fields(page, app_state):
        print("상태 추가 자동화 실패 - fill_status_fields\n")
        return False
    if not click_save_button(page):
        print("상태 추가 자동화 실패 - click_save_button\n")
        return False
    if not confirm_save_changes(page):
        print("상태 추가 자동화 실패 - confirm_save_changes\n")
        return False
    print("상태 추가 자동화 완료\n")
    return True