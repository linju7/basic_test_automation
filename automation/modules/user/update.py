from automation.config.settings import settings
from playwright.sync_api import Page

# 주요 셀렉터 상수
BTN_MODIFY_MEMBER = 'button.lw_btn_point:text-is("구성원 수정")'
BTN_SAVE = 'button.lw_btn_point:text-is("저장")'


def update_user_info(page: Page, app_state=None):
    """구성원 정보 입력 필드들을 수정한다."""
    # 성 (기본/다국어)
    for selector in [
        'input.lw_input[placeholder="성"][maxlength="80"]',
        'input.lw_input[placeholder="성"][maxlength="100"]'
    ]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            page.locator(selector).fill(current_value + "(수정됨)")
    # 이름 (기본/다국어)
    for selector in [
        'input.lw_input[placeholder="이름"][maxlength="80"]',
        'input.lw_input[placeholder="이름"][maxlength="100"]'
    ]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            page.locator(selector).fill(current_value + "(수정됨)")
    # 다국어 필드
    placeholders = [
        "姓(日本語)", "名(日本語)", "Last", "First",
        "姓(简体中文)", "名(简体中文)", "姓(繁體中文)", "名(繁體中文)"
    ]
    for placeholder in placeholders:
        selector = f'input.lw_input[placeholder="{placeholder}"]'
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            page.locator(selector).fill(current_value + "(수정됨)")
    # 닉네임, ID
    for selector in [
        'input.lw_input[placeholder="닉네임"]',
        'input.lw_input[placeholder="ID"]'
    ]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            page.locator(selector).fill(current_value + "(수정됨)")
    # 보조 이메일, 개인 이메일
    for selector, suffix in [
        ('input.lw_input.email_id[placeholder="보조 이메일"]', 'modified'),
        ('input.lw_input[placeholder="개인 이메일"]', 'modified')
    ]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            page.locator(selector).fill(current_value + suffix)
    # 기타 필드
    fields = [
        ('input.lw_input[placeholder="사내 번호"]', '--'),
        ('input.lw_input[placeholder="전화번호"]', '--'),
        ('input.lw_input[placeholder="근무처"]', '(수정됨)'),
        ('input.lw_input[placeholder="담당 업무"]', '(수정됨)'),
        ('input.lw_input[placeholder="사원 번호"]', '(수정됨)')
    ]
    for selector, suffix in fields:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            page.locator(selector).fill(current_value + suffix)
    return page


def update_user(page: Page, app_state=None):
    page.wait_for_selector(BTN_MODIFY_MEMBER, timeout=10000)
    page.locator(BTN_MODIFY_MEMBER).click()
    
    update_user_info(page, app_state)
    if page.locator(BTN_SAVE).count() > 0:
        page.locator(BTN_SAVE).click()
        return True
    return False
