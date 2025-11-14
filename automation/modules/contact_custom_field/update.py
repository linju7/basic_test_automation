from automation.config.settings import settings
from automation.core.safe_fill import safe_fill
from datetime import datetime

# =====================
# 셀렉터 상수 (Contact Custom Field Update Page)
# =====================

# 목록 및 수정 버튼
LIST_ITEM_TEMPLATE = 'div.lw_tr:has(div.lw_td.item:has-text("{item_name}"))'
BTN_MODIFY = 'button.btn_modify:text-is("수정")'

# 항목 수정 레이어
LAYER_EDIT_ITEM = 'div.ly_common.ly_page.ly_contact_add_item'
INPUT_ITEM_NAME = 'div.ly_contact_add_item input.lwds_input[maxlength="20"]'
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
def create_updated_field_info():
    """수정할 연락처 커스텀 필드 데이터를 생성한다."""
    timestamp = datetime.now().strftime("%m%d%H%M")
    
    updated_info = {
        "item_name": f"연락처커스텀_{timestamp}_수정",
        "multilingual_fields": {
            "english": f"연락처커스텀EN_{timestamp}_수정",
            "korean": f"연락처커스텀KR_{timestamp}_수정",
            "japanese": f"연락처커스텀JP_{timestamp}_수정",
            "chinese_simplified": f"연락처커스텀CH_{timestamp}_수정",
            "chinese_traditional": f"연락처커스텀TW_{timestamp}_수정",
        }
    }
    
    return updated_info


# =====================
# 단계별 함수
# =====================
def open_custom_field_page(page):
    """연락처 커스텀 필드 관리 페이지 열기"""
    page.goto(settings.CONTACT_CUSTOM_FIELD_URLS[settings.ENVIRONMENT])
    page.wait_for_timeout(2000)
    return True


def find_and_click_modify_button(page, item_name):
    """목록에서 항목을 찾아 수정 버튼 클릭"""
    # 항목명을 포함하는 행 찾기
    list_item_selector = LIST_ITEM_TEMPLATE.format(item_name=item_name)
    list_item = page.locator(list_item_selector)
    
    if list_item.count() == 0:
        print(f"[실패] 항목 '{item_name}'을 찾을 수 없음")
        return False
    
    # 해당 행 내의 수정 버튼 클릭
    modify_btn = list_item.locator(BTN_MODIFY)
    if modify_btn.count() > 0:
        modify_btn.first.click()
        page.wait_for_selector(LAYER_EDIT_ITEM, timeout=5000)
        return True
    
    print("[실패] '수정' 버튼을 찾을 수 없음")
    return False


def update_item_name(page, new_item_name):
    """항목명을 새 값으로 수정한다."""
    input_field = page.locator(INPUT_ITEM_NAME)
    if input_field.count() > 0:
        input_field.first.clear()
        safe_fill(page, INPUT_ITEM_NAME, new_item_name)
        return True
    print("[실패] 항목명 입력란을 찾을 수 없음")
    return False


def click_set_global_button(page):
    """다국어 설정 버튼 클릭"""
    btn = page.locator(BTN_SET_GLOBAL)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(LAYER_INPUT_GLOBAL, timeout=5000)
        return True
    print("[실패] '다국어 설정' 버튼을 찾을 수 없음")
    return False


def update_multilingual_fields(page, multilingual_fields):
    """다국어 필드를 새 값으로 수정한다."""
    multilingual_mapping = [
        ("english", INPUT_ENGLISH),
        ("korean", INPUT_KOREAN),
        ("japanese", INPUT_JAPANESE),
        ("chinese_simplified", INPUT_CHINESE_SIMPLIFIED),
        ("chinese_traditional", INPUT_CHINESE_TRADITIONAL),
    ]
    
    for field_key, selector in multilingual_mapping:
        value = multilingual_fields.get(field_key)
        if value:
            input_field = page.locator(selector)
            if input_field.count() > 0:
                input_field.first.clear()
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


def save_to_app_state(app_state, updated_info):
    """app_state에 수정된 값을 저장한다."""
    if app_state is None:
        return True
    
    app_state.contact_custom_field_name = updated_info["item_name"]
    app_state.contact_custom_field_name_kr = updated_info["multilingual_fields"]["korean"]
    return True


# =====================
# 메인 플로우 함수
# =====================
def update_contact_custom_field(page, app_state=None):
    """연락처 커스텀 필드 수정 플로우를 순차적으로 실행한다."""
    print("\n연락처 커스텀 필드 수정 자동화 시작")
    
    if not app_state or not app_state.contact_custom_field_name:
        print("[실패] app_state에 contact_custom_field_name이 없음\n")
        return False
    
    # 수정할 데이터 생성
    updated_info = create_updated_field_info()
    # 기존 항목명 (리스트에서 찾기 위함)
    original_name = app_state.contact_custom_field_name
    
    if not save_to_app_state(app_state, updated_info):
        print("연락처 커스텀 필드 수정 자동화 실패 - save_to_app_state\n")
        return False
    
    if not open_custom_field_page(page):
        print("연락처 커스텀 필드 수정 자동화 실패 - open_custom_field_page\n")
        return False
    
    if not find_and_click_modify_button(page, original_name):
        print("연락처 커스텀 필드 수정 자동화 실패 - find_and_click_modify_button\n")
        return False
    
    if not update_item_name(page, updated_info["item_name"]):
        print("연락처 커스텀 필드 수정 자동화 실패 - update_item_name\n")
        return False
    
    if not click_set_global_button(page):
        print("연락처 커스텀 필드 수정 자동화 실패 - click_set_global_button\n")
        return False
    
    if not update_multilingual_fields(page, updated_info["multilingual_fields"]):
        print("연락처 커스텀 필드 수정 자동화 실패 - update_multilingual_fields\n")
        return False
    
    if not click_confirm_global_button(page):
        print("연락처 커스텀 필드 수정 자동화 실패 - click_confirm_global_button\n")
        return False
    
    if not click_save_button(page):
        print("연락처 커스텀 필드 수정 자동화 실패 - click_save_button\n")
        return False
    
    print("연락처 커스텀 필드 수정 자동화 완료\n")
    return True

