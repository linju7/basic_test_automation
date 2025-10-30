from automation.config.settings import settings
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (Company Tag Retrieve Page)
# =====================

# 테이블 관련
TABLE_COVER = 'div.lw_table_cover'
TABLE_BODY = 'div.lw_table_scroll table.lw_table.tb_contacts tbody'
TAG_NAME_CELLS = 'td.tag_name'
TAG_NAME_TITLE = 'td.tag_name[title]'

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

def find_company_tag_in_list(page, app_state=None):
    """회사 태그 리스트에서 특정 태그명 찾기"""
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
            print(f"[성공] 회사 태그 '{tag_name}' 조회 성공")
            return True
    
    print(f"[실패] 회사 태그 '{tag_name}' 조회 실패")
    return False

# =====================
# 메인 플로우 함수
# =====================

def retrieve_company_tag(page, app_state=None):
    """회사 태그 조회 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    print("\n회사 태그 조회 자동화 시작")
    if not open_company_tag_page(page):
        print("회사 태그 조회 자동화 실패 - open_company_tag_page\n")
        return False
    if not find_company_tag_in_list(page, app_state):
        print("회사 태그 조회 자동화 실패 - find_company_tag_in_list\n")
        return False
    print("회사 태그 조회 자동화 완료\n")
    return True
