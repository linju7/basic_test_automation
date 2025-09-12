from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (MY Tag Create Page)
# =====================

# 버튼
BTN_ADD_MY_TAG = 'div.task_area button.lw_btn.right_aligned:text-is("MY 태그 추가")'
BTN_SAVE = 'div.btn_area button.lw_btn_point_40:text-is("저장")'

# 입력 필드
INPUT_TAG_NAME = 'input#_tag_dialog_input.lw_input'

# 레이어
LAYER_CREATE_TAG = 'div.ly_common h3.title:text-is("MY 태그 만들기")'

# =====================
# 유틸 함수
# =====================

def open_my_tag_page(page):
    """MY 태그 페이지로 이동"""
    page.goto(settings.MY_TAG_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_ADD_MY_TAG, timeout=5000)

def click_add_my_tag_button(page):
    """MY 태그 추가 버튼 클릭"""
    btn = page.locator(BTN_ADD_MY_TAG)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(LAYER_CREATE_TAG, timeout=5000)
        return True
    return False

def fill_tag_name(page, app_state=None):
    """MY 태그명 입력"""
    timestamp = datetime.now().strftime("%m%d%H%M")
    tag_name = f"MY태그_자동화_{timestamp}"
    
    # 입력 필드가 나타날 때까지 대기
    page.wait_for_selector(INPUT_TAG_NAME, timeout=5000)
    
    # 태그명 입력
    input_field = page.locator(INPUT_TAG_NAME)
    if input_field.count() > 0:
        safe_fill(page, INPUT_TAG_NAME, tag_name)
        # app_state에 저장
        if app_state is not None:
            app_state.my_tag_name = tag_name
        return True
    return False

def click_save_button(page):
    """저장 버튼 클릭"""
    # 저장 버튼이 활성화될 때까지 대기
    page.wait_for_selector(BTN_SAVE, timeout=5000)
    
    btn = page.locator(BTN_SAVE)
    if btn.count() > 0:
        # 버튼이 활성화될 때까지 대기
        page.wait_for_timeout(1000)
        btn.first.click()
        page.wait_for_timeout(2000)
        return True
    return False

# =====================
# 메인 플로우 함수
# =====================

def create_my_tag(page, app_state=None):
    """MY 태그 추가 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    open_my_tag_page(page)
    if not click_add_my_tag_button(page):
        return False
    if not fill_tag_name(page, app_state):
        return False
    if not click_save_button(page):
        return False
    return True
