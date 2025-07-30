from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Contact Delete Page)
# =====================

# 검색 및 결과
SEARCH_INPUT = 'input.workscmn_search_input'
SEARCH_SUBMIT = 'button.workscmn_btn_search_submit'
SEARCH_RESULT_NAME = 'td.name p span.text strong em.keyword'
SEARCH_RESULT_ROW = 'tbody tr'

# 상세 뷰
DETAIL_NAME = 'div.list_detail p.name_box strong'
DETAIL_SHOW_MORE = 'div.list_detail a.ico_more'
DETAIL_MORE_MENU = 'div.ly_more_menu'
DETAIL_DELETE = 'div.ly_more_menu ul > li:nth-child(3) > a:has-text("삭제")'

# 삭제 확인 레이어
CONFIRM_LAYER = 'div.type_c.type_c_confirm'
CONFIRM_BUTTON = 'div.type_c.type_c_confirm button.btn_point:has-text("확인")'

# =====================
# 유틸 함수
# =====================
def search_contact(page, contact_name):
    page.wait_for_selector(SEARCH_INPUT, timeout=5000)
    page.locator(SEARCH_INPUT).fill(contact_name)
    page.wait_for_timeout(2000)
    page.locator(SEARCH_SUBMIT).click()
    page.wait_for_timeout(2000)
    page.wait_for_selector(SEARCH_RESULT_ROW, timeout=5000)
    page.locator(SEARCH_RESULT_NAME).first.click()
    page.wait_for_selector(DETAIL_NAME, timeout=3000)

def open_delete_menu(page):
    page.locator(DETAIL_SHOW_MORE).click()
    page.wait_for_selector(DETAIL_MORE_MENU, state="visible", timeout=2000)
    page.locator(DETAIL_DELETE).click()

def confirm_delete(page):
    page.wait_for_selector(CONFIRM_LAYER, timeout=2000)
    page.locator(CONFIRM_BUTTON).click()

# =====================
# 메인 플로우 함수
# =====================
def delete_contact(page, app_state=None):
    """연락처를 검색 후 상세 진입, 삭제 메뉴 클릭 및 확인한다."""
    search_contact(page, app_state.contact_name)
    open_delete_menu(page)
    confirm_delete(page)
    return True
