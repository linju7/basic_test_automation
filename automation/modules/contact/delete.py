from automation.config.settings import settings
from automation.core.safe_fill import safe_fill

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


def search_contact(page, contact_name):
    """연락처 검색"""
    page.wait_for_selector(SEARCH_INPUT, timeout=5000)
    page.wait_for_timeout(2000)
    safe_fill(page, SEARCH_INPUT, contact_name)
    page.wait_for_timeout(2000)
    page.locator(SEARCH_SUBMIT).click()
    page.wait_for_timeout(2000)
    page.wait_for_selector(SEARCH_RESULT_ROW, timeout=5000)
    page.locator(SEARCH_RESULT_NAME).first.click()  # 검색 결과 중 첫 번째 연락처 클릭 (유니크 값이 보장되어야 함)
    page.wait_for_selector(DETAIL_NAME, timeout=3000)

    return True

def open_delete_menu(page):
    """상세 뷰 삭제 클릭"""
    page.locator(DETAIL_SHOW_MORE).click()
    page.wait_for_selector(DETAIL_MORE_MENU, state="visible", timeout=2000)
    page.locator(DETAIL_DELETE).click()  # 삭제 메뉴 클릭

    return True


def confirm_delete(page):
    """삭제 확인 레이어 클릭"""
    page.wait_for_selector(CONFIRM_LAYER, timeout=2000)
    page.locator(CONFIRM_BUTTON).click()

    return True

# =====================
# 메인 플로우 함수
# =====================
def delete_contact(page, app_state=None):
    """연락처를 검색 후 상세 진입, 삭제 메뉴 클릭 및 확인"""
    print("\n외부 연락처 삭제 자동화 시작")

    # app_state 에 저장된 연락처 이름을 불러와서 검색에 사용 (저장에 문제가 있는 경우 검색되지 않음 -> create 파일 참고)
    if not search_contact(page, app_state.contact_name):
        print("외부 연락처 삭제 자동화 실패 - search_contact\n")
        return False
    if not open_delete_menu(page):
        print("외부 연락처 삭제 자동화 실패 - open_delete_menu\n")
        return False
    if not confirm_delete(page):
        print("외부 연락처 삭제 자동화 실패 - confirm_delete\n")
        return False
    print("외부 연락처 삭제 자동화 완료\n")
    return True
