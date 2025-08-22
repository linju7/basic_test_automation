from automation.config.settings import settings
from playwright.sync_api import Page
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (User Update Page)
# =====================

# 액션 버튼
BTN_MODIFY_MEMBER = 'button.lw_btn_point:text-is("구성원 수정")'
BTN_SAVE = 'button.lw_btn_point:text-is("저장")'

# 기본 입력 필드
INPUT_LAST_NAME_80 = 'input.lw_input[placeholder="성"][maxlength="80"]'
INPUT_FIRST_NAME_80 = 'input.lw_input[placeholder="이름"][maxlength="80"]'
INPUT_LAST_NAME_100 = 'input.lw_input[placeholder="성"][maxlength="100"]'
INPUT_FIRST_NAME_100 = 'input.lw_input[placeholder="이름"][maxlength="100"]'
INPUT_NICKNAME = 'input.lw_input[placeholder="닉네임"]'
INPUT_USER_ID = 'input.lw_input[placeholder="ID"]'

# 다국어 입력 필드
INPUT_JAPANESE_LAST = 'input.lw_input[placeholder="姓(日本語)"]'
INPUT_JAPANESE_FIRST = 'input.lw_input[placeholder="名(日本語)"]'
INPUT_ENGLISH_LAST = 'input.lw_input[placeholder="Last"]'
INPUT_ENGLISH_FIRST = 'input.lw_input[placeholder="First"]'
INPUT_SIMPLIFIED_CHINESE_LAST = 'input.lw_input[placeholder="姓(简体中文)"]'
INPUT_SIMPLIFIED_CHINESE_FIRST = 'input.lw_input[placeholder="名(简体中文)"]'
INPUT_TRADITIONAL_CHINESE_LAST = 'input.lw_input[placeholder="姓(繁體中文)"]'
INPUT_TRADITIONAL_CHINESE_FIRST = 'input.lw_input[placeholder="名(繁體中文)"]'

# 이메일 및 기타 필드
INPUT_SUB_EMAIL = 'input.lw_input.email_id[placeholder="보조 이메일"]'
INPUT_PRIVATE_EMAIL = 'input.lw_input[placeholder="개인 이메일"]'
INPUT_INTERNAL_NUMBER = 'input.lw_input[placeholder="사내 번호"]'
INPUT_PHONE_NUMBER = 'input.lw_input[placeholder="전화번호"]'
INPUT_WORKPLACE = 'input.lw_input[placeholder="근무처"]'
INPUT_TASK = 'input.lw_input[placeholder="담당 업무"]'
INPUT_EMPLOYEE_NUMBER = 'input.lw_input[placeholder="사원 번호"]'

# 다국어 필드 placeholder 리스트
MULTILINGUAL_PLACEHOLDERS = [
    "姓(日本語)", "名(日本語)", "Last", "First",
    "姓(简体中文)", "名(简体中文)", "姓(繁體中文)", "名(繁體中文)"
]


def click_modify_button(page):
    """구성원 수정 버튼 클릭"""
    page.wait_for_selector(BTN_MODIFY_MEMBER, timeout=10000)
    page.locator(BTN_MODIFY_MEMBER).click()
    return True


def update_user_info(page: Page, app_state=None):
    """구성원 정보 입력 필드들을 수정"""
    # 성 (기본/다국어)
    for selector in [INPUT_LAST_NAME_80, INPUT_LAST_NAME_100]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            safe_fill(page, selector, current_value + "(수정됨)")
    
    # 이름 (기본/다국어)
    for selector in [INPUT_FIRST_NAME_80, INPUT_FIRST_NAME_100]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            safe_fill(page, selector, current_value + "(수정됨)")
    
    # 다국어 필드
    for placeholder in MULTILINGUAL_PLACEHOLDERS:
        selector = f'input.lw_input[placeholder="{placeholder}"]'
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            safe_fill(page, selector, current_value + "(수정됨)")
    
    # 닉네임, ID
    for selector in [INPUT_NICKNAME, INPUT_USER_ID]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            safe_fill(page, selector, current_value + "(수정됨)")
    
    # 보조 이메일, 개인 이메일
    for selector, suffix in [
        (INPUT_SUB_EMAIL, 'modified'),
        (INPUT_PRIVATE_EMAIL, 'modified')
    ]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            safe_fill(page, selector, current_value + suffix)
    
    # 기타 필드
    fields = [
        (INPUT_INTERNAL_NUMBER, '--'),
        (INPUT_PHONE_NUMBER, '--'),
        (INPUT_WORKPLACE, '(수정됨)'),
        (INPUT_TASK, '(수정됨)'),
        (INPUT_EMPLOYEE_NUMBER, '(수정됨)')
    ]
    for selector, suffix in fields:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            safe_fill(page, selector, current_value + suffix)
    
    return True


def click_save_button(page):
    """저장 버튼 클릭"""
    if page.locator(BTN_SAVE).count() > 0:
        page.locator(BTN_SAVE).click()
        return True
    return False


# =====================
# 메인 플로우 함수
# =====================
def update_user(page: Page, app_state=None):
    """구성원 수정 플로우를 순차적으로 실행"""
    if not click_modify_button(page):
        return False
    if not update_user_info(page, app_state):
        return False
    if not click_save_button(page):
        return False
    return True
