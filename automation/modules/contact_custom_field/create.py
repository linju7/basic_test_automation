from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (Contact Custom Field Create Page)
# =====================

# 페이지 진입 버튼
BTN_ADD_ITEM = 'div.task_area button.lw_btn_point:text-is("항목 추가")'

# 항목 추가 레이어
LAYER_ADD_ITEM = 'div.ly_common.ly_page.ly_contact_add_item'
INPUT_ITEM_NAME = 'div.ly_contact_add_item input.lwds_input[maxlength="20"]'
INPUT_PROPERTY_NAME = 'div.ly_contact_add_item input.lwds_input[maxlength="120"]'
BTN_SET_GLOBAL = 'div.ly_contact_add_item button.btn_set_global'
BTN_SAVE = 'div.ly_contact_add_item div.btn_box button.lwds_button_contain:text-is("저장")'

# 다국어 설정 레이어
LAYER_INPUT_GLOBAL = 'div.ly_common.ly_page.ly_input_global'
INPUT_ENGLISH = 'div.ly_input_global li:has(span.label_cover:text("English")) input.lwds_input'
INPUT_KOREAN = 'div.ly_input_global li:has(span.label_cover:text("한국어")) input.lwds_input'
INPUT_JAPANESE = 'div.ly_input_global li:has(span.label_cover:text("日本語")) input.lwds_input'
INPUT_CHINESE_SIMPLIFIED = 'div.ly_input_global li:has(span.label_cover:text("简体中文")) input.lwds_input'
INPUT_CHINESE_TRADITIONAL = 'div.ly_input_global li:has(span.label_cover:text("繁體中文")) input.lwds_input'
BTN_CONFIRM_GLOBAL = 'div.ly_input_global div.btn_box button.lwds_button_contain:text-is("확인")'


# =====================
# 데이터 생성 함수
# =====================
def create_custom_field_info():
    """연락처 커스텀 필드 입력 데이터를 생성한다."""
    timestamp = datetime.now().strftime("%m%d%H%M")
    
    custom_field_info = {
        "timestamp": timestamp,
        "item_name": f"연락처커스텀_{timestamp}",
        "property_name": f"contact_custom_{timestamp}",
        "multilingual_fields": {
            "english": f"연락처커스텀EN_{timestamp}",
            "korean": f"연락처커스텀KR_{timestamp}",
            "japanese": f"연락처커스텀JP_{timestamp}",
            "chinese_simplified": f"연락처커스텀CH_{timestamp}",
            "chinese_traditional": f"연락처커스텀TW_{timestamp}",
        }
    }
    
    return custom_field_info


# =====================
# 단계별 함수
# =====================
def open_custom_field_page(page):
    """연락처 커스텀 필드 관리 페이지 열기"""
    page.goto(settings.CONTACT_CUSTOM_FIELD_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_ADD_ITEM, timeout=5000)
    return True


def click_add_item_button(page):
    """항목 추가 버튼 클릭"""
    btn = page.locator(BTN_ADD_ITEM)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(LAYER_ADD_ITEM, timeout=5000)
        return True
    print("[실패] '항목 추가' 버튼을 찾을 수 없음")
    return False


def fill_item_name(page, item_name):
    """항목명 입력"""
    safe_fill(page, INPUT_ITEM_NAME, item_name)
    return True


def fill_property_name(page, property_name):
    """propertyName 입력"""
    safe_fill(page, INPUT_PROPERTY_NAME, property_name)
    return True


def click_set_global_button(page):
    """다국어 설정 버튼 클릭"""
    btn = page.locator(BTN_SET_GLOBAL)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(LAYER_INPUT_GLOBAL, timeout=5000)
        return True
    print("[실패] '다국어 설정' 버튼을 찾을 수 없음")
    return False


def fill_multilingual_fields(page, custom_field_info):
    """다국어 필드 입력"""
    multilingual = custom_field_info["multilingual_fields"]
    multilingual_fields = [
        ("English", INPUT_ENGLISH, multilingual["english"]),
        ("한국어", INPUT_KOREAN, multilingual["korean"]),
        ("日本語", INPUT_JAPANESE, multilingual["japanese"]),
        ("简体中文", INPUT_CHINESE_SIMPLIFIED, multilingual["chinese_simplified"]),
        ("繁體中文", INPUT_CHINESE_TRADITIONAL, multilingual["chinese_traditional"]),
    ]
    
    for lang, selector, value in multilingual_fields:
        safe_fill(page, selector, value)
    
    return True


def click_confirm_global_button(page):
    """다국어 설정 확인 버튼 클릭"""
    btn = page.locator(BTN_CONFIRM_GLOBAL)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_timeout(500)
        return True
    print("[실패] 다국어 설정 '확인' 버튼을 찾을 수 없음")
    return False


def click_save_button(page):
    """저장 버튼 클릭"""
    btn = page.locator(BTN_SAVE)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_timeout(2000)
        return True
    print("[실패] '저장' 버튼을 찾을 수 없음")
    return False


def save_to_app_state(app_state, custom_field_info):
    """app_state에 생성된 값을 저장한다."""
    if app_state is None:
        return True
    
    app_state.contact_custom_field_name = custom_field_info["item_name"]
    app_state.contact_custom_field_name_kr = custom_field_info["multilingual_fields"]["korean"]
    return True


# =====================
# 메인 플로우 함수
# =====================
def create_contact_custom_field(page, app_state=None):
    """연락처 커스텀 필드 추가 플로우를 순차적으로 실행한다."""
    print("\n연락처 커스텀 필드 추가 자동화 시작")
    
    # 커스텀 필드 정보 생성
    custom_field_info = create_custom_field_info()
    
    if not save_to_app_state(app_state, custom_field_info):
        print("연락처 커스텀 필드 추가 자동화 실패 - save_to_app_state\n")
        return False
    
    if not open_custom_field_page(page):
        print("연락처 커스텀 필드 추가 자동화 실패 - open_custom_field_page\n")
        return False
    
    if not click_add_item_button(page):
        print("연락처 커스텀 필드 추가 자동화 실패 - click_add_item_button\n")
        return False
    
    if not fill_item_name(page, custom_field_info["item_name"]):
        print("연락처 커스텀 필드 추가 자동화 실패 - fill_item_name\n")
        return False
    
    if not fill_property_name(page, custom_field_info["property_name"]):
        print("연락처 커스텀 필드 추가 자동화 실패 - fill_property_name\n")
        return False
    
    if not click_set_global_button(page):
        print("연락처 커스텀 필드 추가 자동화 실패 - click_set_global_button\n")
        return False
    
    if not fill_multilingual_fields(page, custom_field_info):
        print("연락처 커스텀 필드 추가 자동화 실패 - fill_multilingual_fields\n")
        return False
    
    if not click_confirm_global_button(page):
        print("연락처 커스텀 필드 추가 자동화 실패 - click_confirm_global_button\n")
        return False
    
    if not click_save_button(page):
        print("연락처 커스텀 필드 추가 자동화 실패 - click_save_button\n")
        return False
    
    print("연락처 커스텀 필드 추가 자동화 완료\n")
    return True

