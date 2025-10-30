from automation.config.settings import settings
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (Company Tag Update Page)
# =====================

# 테이블 관련
TABLE_COVER = 'div.lw_table_cover'
TABLE_BODY = 'div.lw_table_scroll table.lw_table.tb_contacts tbody'
TAG_NAME_CELLS = 'td.tag_name'
MANAGE_BUTTONS = 'td.manage div.task button'

# 버튼
BTN_RENAME = 'button:text-is("이름 바꾸기")'
BTN_SAVE = 'div.btn_area button.lw_btn_point_40:text-is("저장")'

# 입력 필드
INPUT_TAG_NAME = 'input#_tag_dialog_input.lw_input'

# 레이어
LAYER_RENAME_TAG = 'div.ly_common h3.title:text-is("태그 이름 바꾸기")'

# =====================
# 유틸 함수
# =====================

def open_company_tag_page(page):
    """회사 태그 페이지로 이동"""
    page.goto(settings.COMPANY_TAG_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(TABLE_COVER, timeout=10000)
    return True

def wait_for_table_loading(page):
    """테이블 로딩 완료 대기"""
    page.wait_for_selector(TABLE_BODY, timeout=10000)
    page.wait_for_timeout(2000)  # 테이블 내용 로딩 대기

def find_and_click_rename_button(page, app_state=None):
    """자동화로 생성된 태그를 찾고 이름 바꾸기 버튼 클릭"""
    # app_state에서 회사 태그명 가져오기
    if not app_state or not hasattr(app_state, 'company_tag_name') or not app_state.company_tag_name:
        return False
    
    tag_name = app_state.company_tag_name
    
    # 테이블 로딩 대기
    wait_for_table_loading(page)
    
    # 모든 태그명 셀 찾기
    tag_cells = page.locator(TAG_NAME_CELLS)
    if tag_cells.count() == 0:
        return False
    
    # 모든 태그를 순회하면서 찾기
    for i in range(tag_cells.count()):
        cell_text = tag_cells.nth(i).text_content().strip()
        if cell_text == tag_name:
            # 해당 행의 이름 바꾸기 버튼 찾기
            row = tag_cells.nth(i).locator('xpath=..')  # 부모 tr 요소
            rename_btn = row.locator(BTN_RENAME)
            if rename_btn.count() > 0:
                rename_btn.first.click()
                page.wait_for_selector(LAYER_RENAME_TAG, timeout=5000)
                return True
    
    return False

def update_tag_name(page, app_state=None):
    """태그명 뒤에 (수정) 추가"""
    if not app_state or not hasattr(app_state, 'company_tag_name') or not app_state.company_tag_name:
        return False
    
    original_name = app_state.company_tag_name
    updated_name = f"{original_name}(수정)"
    
    # 입력 필드가 나타날 때까지 대기
    page.wait_for_selector(INPUT_TAG_NAME, timeout=5000)
    
    # 기존 텍스트를 모두 선택하고 새로운 이름으로 교체
    input_field = page.locator(INPUT_TAG_NAME)
    if input_field.count() > 0:
        input_field.first.click()
        input_field.first.select_text()
        safe_fill(page, INPUT_TAG_NAME, updated_name)
        
        # app_state에 업데이트된 이름 저장
        app_state.company_tag_name = updated_name
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

def update_company_tag(page, app_state=None):
    """회사 태그 수정 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    print("\n회사 태그 수정 자동화 시작")
    if not open_company_tag_page(page):
        print("회사 태그 수정 자동화 실패 - open_company_tag_page\n")
        return False
    if not find_and_click_rename_button(page, app_state):
        print("회사 태그 수정 자동화 실패 - find_and_click_rename_button\n")
        return False
    if not update_tag_name(page, app_state):
        print("회사 태그 수정 자동화 실패 - update_tag_name\n")
        return False
    if not click_save_button(page):
        print("회사 태그 수정 자동화 실패 - click_save_button\n")
        return False
    print("회사 태그 수정 자동화 완료\n")
    return True
