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
INPUT_LAST_NAME_80 = 'div.name_box:not(.minor) input.lw_input[placeholder="성"]'
INPUT_FIRST_NAME_80 = 'div.name_box:not(.minor) input.lw_input[placeholder="이름"]'
INPUT_LAST_NAME_100 = 'input.lw_input[placeholder="성"][maxlength="100"]'
INPUT_FIRST_NAME_100 = 'input.lw_input[placeholder="이름"][maxlength="100"]'
INPUT_NICKNAME = 'div.field:has(i.hd:text-is("닉네임")) input.lw_input.w_limit'
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
INPUT_SUB_EMAIL = 'div.field:has(i.hd:text-is("보조 이메일")) div.item input.lw_input.email_id'
INPUT_PRIVATE_EMAIL = 'div.field:has(i.hd:text-is("개인 이메일")) input.lw_input.email_id'
INPUT_INTERNAL_NUMBER = 'input.lw_input[placeholder="사내 번호"]'
INPUT_PHONE_NUMBER = 'input.lw_input[placeholder="전화번호"]'
INPUT_WORKPLACE = 'input.lw_input[placeholder="근무처"]'
INPUT_TASK = 'input.lw_input[placeholder="담당 업무"]'
INPUT_EMPLOYEE_NUMBER = 'input.lw_input[placeholder="사원 번호"]'

# 다국어 필드 placeholder 리스트
MULTILINGUAL_PLACEHOLDERS = [
    "姓(日本語)", "名(日本語)", "Last", "First",
    "성", "이름",  # 한국어 다국어명 (maxlength="100")
    "姓(简体中文)", "名(简体中文)", "姓(繁體中文)", "名(繁體中文)"
]


def click_modify_button(page):
    """구성원 수정 버튼 클릭"""
    page.wait_for_selector(BTN_MODIFY_MEMBER, timeout=30000)
    page.locator(BTN_MODIFY_MEMBER).click()
    return True


def update_user_info(page: Page, app_state=None):
    """구성원 정보 입력 필드들을 수정"""
    # app_state에 수정된 정보 저장을 위한 딕셔너리 초기화
    if app_state is not None and hasattr(app_state, 'user_info') and app_state.user_info:
        updated_info = {
            "timestamp": app_state.user_info.get("timestamp"),
            "user_id": app_state.user_info.get("user_id"),
            "basic_fields": app_state.user_info.get("basic_fields", {}).copy(),
            "multilingual_fields": app_state.user_info.get("multilingual_fields", {}).copy(),
            "email_fields": app_state.user_info.get("email_fields", {}).copy()
        }
    
    # 성 (기본 필드만 - maxlength="80")
    if page.locator(INPUT_LAST_NAME_80).count() > 0:
        current_value = page.locator(INPUT_LAST_NAME_80).input_value()
        new_value = current_value + "(수정됨)"
        safe_fill(page, INPUT_LAST_NAME_80, new_value)
        # app_state에 저장
        if app_state is not None and 'updated_info' in locals():
            updated_info["basic_fields"]["last_name"] = new_value
    
    # 이름 (기본 필드만 - maxlength="80")
    if page.locator(INPUT_FIRST_NAME_80).count() > 0:
        current_value = page.locator(INPUT_FIRST_NAME_80).input_value()
        new_value = current_value + "(수정됨)"
        safe_fill(page, INPUT_FIRST_NAME_80, new_value)
        # app_state에 저장
        if app_state is not None and 'updated_info' in locals():
            updated_info["basic_fields"]["first_name"] = new_value
    
    # 다국어 필드 - create.py와 정확히 동일한 매핑
    multilingual_mapping = {
        "姓(日本語)": "japanese_last",
        "名(日本語)": "japanese_first",
        "Last": "english_first",  # Last=이름 (create.py 173줄과 동일)
        "First": "english_last",  # First=성 (create.py 174줄과 동일)
        "성": "korean_last",      # 한국어 다국어명 (create.py 175줄과 동일)
        "이름": "korean_first",    # 한국어 다국어명 (create.py 176줄과 동일)
        "姓(简体中文)": "simplified_chinese_last",
        "名(简体中文)": "simplified_chinese_first",
        "姓(繁體中文)": "traditional_chinese_last",
        "名(繁體中文)": "traditional_chinese_first"
    }
    
    for placeholder in MULTILINGUAL_PLACEHOLDERS:
        # 한국어 다국어명은 maxlength="100"으로 구분해야 함
        if placeholder in ["성", "이름"]:
            selector = f'input.lw_input[placeholder="{placeholder}"][maxlength="100"]'
        else:
            selector = f'input.lw_input[placeholder="{placeholder}"]'
            
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            new_value = current_value + "(수정됨)"
            safe_fill(page, selector, new_value)
            # app_state에 저장
            if app_state is not None and 'updated_info' in locals() and placeholder in multilingual_mapping:
                field_key = multilingual_mapping[placeholder]
                updated_info["multilingual_fields"][field_key] = new_value
    
    # 닉네임, ID
    for selector in [INPUT_NICKNAME, INPUT_USER_ID]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            new_value = current_value + "(수정됨)"
            safe_fill(page, selector, new_value)
            # app_state에 저장
            if app_state is not None and 'updated_info' in locals():
                if selector == INPUT_NICKNAME:
                    updated_info["basic_fields"]["nickname"] = new_value
                elif selector == INPUT_USER_ID:
                    app_state.global_user_id = new_value
                    updated_info[field_key] = new_value
                else:
                    updated_info["basic_fields"][field_key] = new_value
    
    # 보조 이메일, 개인 이메일
    email_mapping = {
        INPUT_SUB_EMAIL: "sub_email",
        INPUT_PRIVATE_EMAIL: "private_email"
    }
    
    for selector, suffix in [
        (INPUT_SUB_EMAIL, 'modified'),
        (INPUT_PRIVATE_EMAIL, 'modified')
    ]:
        if page.locator(selector).count() > 0:
            current_value = page.locator(selector).input_value()
            new_value = current_value + suffix
            safe_fill(page, selector, new_value)
            # app_state에 저장
            if app_state is not None and 'updated_info' in locals() and selector in email_mapping:
                field_key = email_mapping[selector]
                updated_info["email_fields"][field_key] = new_value
    
    # 기타 필드
    basic_field_mapping = {
        INPUT_INTERNAL_NUMBER: "internal_number",
        INPUT_PHONE_NUMBER: "phone_number",
        INPUT_WORKPLACE: "workplace",
        INPUT_TASK: "task",
        INPUT_EMPLOYEE_NUMBER: "employee_number"
    }
    
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
            new_value = current_value + suffix
            safe_fill(page, selector, new_value)
            # app_state에 저장
            if app_state is not None and 'updated_info' in locals() and selector in basic_field_mapping:
                field_key = basic_field_mapping[selector]
                updated_info["basic_fields"][field_key] = new_value
    
    # 수정된 정보를 app_state에 최종 저장
    if app_state is not None and 'updated_info' in locals():
        app_state.user_info = updated_info
    
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
    print("\n구성원 수정 자동화 시작")
    if not click_modify_button(page):
        print("구성원 수정 자동화 실패 - click_modify_button\n")
        return False
    if not update_user_info(page, app_state):
        print("구성원 수정 자동화 실패 - update_user_info\n")
        return False
    if not click_save_button(page):
        print("구성원 수정 자동화 실패 - click_save_button\n")
        return False
    print("구성원 수정 자동화 완료\n")
    return True
