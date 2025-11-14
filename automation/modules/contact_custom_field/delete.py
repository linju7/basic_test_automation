from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Contact Custom Field Delete Page)
# =====================

# 목록 및 삭제 버튼
LIST_ITEM_TEMPLATE = 'div.lw_tr:has(div.lw_td.item:has-text("{item_name}"))'
BTN_DELETE = 'button.btn_delete:text-is("삭제")'

# 삭제 확인 레이어
LAYER_CONFIRM = 'div.ly_common.freeplan'
BTN_CONFIRM = 'div.ly_common.freeplan div.btn_box button.lw_btn_point:text-is("확인")'


# =====================
# 단계별 함수
# =====================
def open_custom_field_page(page):
    """연락처 커스텀 필드 관리 페이지 열기"""
    page.goto(settings.CONTACT_CUSTOM_FIELD_URLS[settings.ENVIRONMENT])
    page.wait_for_timeout(2000)
    return True


def find_and_click_delete_button(page, item_name):
    """목록에서 항목을 찾아 삭제 버튼 클릭"""
    list_item_selector = LIST_ITEM_TEMPLATE.format(item_name=item_name)
    list_item = page.locator(list_item_selector)
    
    if list_item.count() == 0:
        print(f"[실패] 항목 '{item_name}'을 찾을 수 없음")
        return False
    
    modify_btn = list_item.locator(BTN_DELETE)
    if modify_btn.count() > 0:
        modify_btn.first.click()
        page.wait_for_selector(LAYER_CONFIRM, timeout=5000)
        return True
    
    print("[실패] '삭제' 버튼을 찾을 수 없음")
    return False


def click_confirm_button(page):
    """삭제 확인 버튼 클릭"""
    btn = page.locator(BTN_CONFIRM)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_timeout(2000)
        return True
    print("[실패] '확인' 버튼을 찾을 수 없음")
    return False


# =====================
# 메인 플로우 함수
# =====================
def delete_contact_custom_field(page, app_state=None):
    """연락처 커스텀 필드 삭제 플로우를 순차적으로 실행한다."""
    print("\n연락처 커스텀 필드 삭제 자동화 시작")
    
    if not app_state or not app_state.contact_custom_field_name:
        print("[실패] app_state에 contact_custom_field_name이 없음\n")
        return False
    
    if not open_custom_field_page(page):
        print("연락처 커스텀 필드 삭제 자동화 실패 - open_custom_field_page\n")
        return False
    
    if not find_and_click_delete_button(page, app_state.contact_custom_field_name):
        print("연락처 커스텀 필드 삭제 자동화 실패 - find_and_click_delete_button\n")
        return False
    
    if not click_confirm_button(page):
        print("연락처 커스텀 필드 삭제 자동화 실패 - click_confirm_button\n")
        return False
    
    print("연락처 커스텀 필드 삭제 자동화 완료\n")
    return True

