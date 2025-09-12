from automation.config.settings import settings

# =====================
# 셀렉터 상수 (MY Tag Delete Page)
# =====================

# 테이블 관련
TABLE_COVER = 'div.lw_table_cover'
TABLE_BODY = 'div.lw_table_scroll table.lw_table.tb_contacts tbody'
TAG_NAME_CELLS = 'td.tag_name'

# 버튼
BTN_DELETE = 'button:text-is("삭제")'
BTN_CONFIRM_DELETE = 'div.btn_area button.lw_btn_alert_40:text-is("삭제")'

# 레이어
LAYER_DELETE_CONFIRM = 'div.ly_common h3.title'

# =====================
# 유틸 함수
# =====================

def open_my_tag_page(page):
    """MY 태그 페이지로 이동"""
    page.goto(settings.MY_TAG_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(TABLE_COVER, timeout=10000)
    return True

def wait_for_table_loading(page):
    """테이블 로딩 완료 대기"""
    page.wait_for_selector(TABLE_BODY, timeout=10000)
    page.wait_for_timeout(2000)  # 테이블 내용 로딩 대기

def find_and_click_delete_button(page, app_state=None):
    """자동화로 생성된 MY 태그를 찾고 삭제 버튼 클릭"""
    # app_state에서 MY 태그명 가져오기
    if not app_state or not hasattr(app_state, 'my_tag_name') or not app_state.my_tag_name:
        return False
    
    tag_name = app_state.my_tag_name
    
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
            # 해당 행의 삭제 버튼 찾기
            row = tag_cells.nth(i).locator('xpath=..')  # 부모 tr 요소
            delete_btn = row.locator(BTN_DELETE)
            if delete_btn.count() > 0:
                delete_btn.first.click()
                page.wait_for_selector(LAYER_DELETE_CONFIRM, timeout=5000)
                return True
    
    return False

def confirm_delete(page):
    """삭제 확인 레이어에서 삭제 버튼 클릭"""
    # 삭제 확인 레이어가 나타날 때까지 대기
    page.wait_for_selector(BTN_CONFIRM_DELETE, timeout=5000)
    
    btn = page.locator(BTN_CONFIRM_DELETE)
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

def delete_my_tag(page, app_state=None):
    """MY 태그 삭제 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    if not open_my_tag_page(page):
        return False
    if not find_and_click_delete_button(page, app_state):
        return False
    if not confirm_delete(page):
        return False
    return True
