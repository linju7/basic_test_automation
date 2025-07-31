from datetime import datetime
from playwright.sync_api import Page


def wait_and_click(page: Page, selector: str, timeout=5000):
    """selector가 나타날 때까지 대기 후 클릭"""
    page.wait_for_selector(selector, timeout=timeout)
    page.locator(selector).click()


def click_edit_button(page: Page):
    """상태 수정 버튼 클릭"""
    try:
        wait_and_click(page, 'button.lw_btn:has-text("수정")')
        return True
    except Exception as e:
        print(f"[실패] 수정 버튼 클릭 오류: {e}")
        return False


def get_last_status_input(page: Page):
    """마지막 상태 입력란 반환"""
    inputs = page.locator('input.lw_input[placeholder="상태명을 입력해 주세요."]')
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None


def get_last_lang_input(page: Page, lang: str):
    """다국어 입력란 중 마지막 항목 반환"""
    selector = f'div.lang_field:has-text("{lang}") input.lw_input'
    inputs = page.locator(selector)
    if inputs.count() > 0:
        return inputs.nth(inputs.count() - 1)
    return None


def click_save_button(page: Page):
    """저장 버튼 클릭"""
    try:
        wait_and_click(page, 'button.lw_btn_point:has-text("저장")')
        return True
    except Exception as e:
        print(f"[실패] 저장 버튼 클릭 오류: {e}")
        return False


def confirm_save_changes(page: Page):
    """저장 확인 팝업 처리"""
    try:
        page.wait_for_selector('div.ly_common.freeplan', timeout=5000)
        wait_and_click(page, 'div.ly_common.freeplan button.lw_btn_point:has-text("확인")')
        return True
    except Exception as e:
        print(f"[실패] 저장 확인 레이어 처리 오류: {e}")
        return False


def modify_last_status(page: Page, app_state=None):
    """기존 상태 항목의 마지막 항목을 수정하는 플로우"""
    # 수정 버튼 클릭
    if not click_edit_button(page):
        return False

    timestamp = datetime.now().strftime("%m%d%H%M")
    status_name = f"자동화상태_{timestamp}_수정"

    # 메인 상태명 입력란 수정
    input_main = get_last_status_input(page)
    if input_main is not None:
        input_main.fill(status_name)
        if app_state is not None:
            app_state.status_name = status_name
    else:
        print("[실패] 상태명 입력란을 찾을 수 없음")
        return False

    page.wait_for_timeout(1000)

    # 다국어 입력란 수정
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

    # 저장 + 확인
    if not click_save_button(page):
        return False
    if not confirm_save_changes(page):
        return False

    return True