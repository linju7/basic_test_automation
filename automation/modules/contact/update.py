from automation.config.settings import settings
from datetime import datetime

# =====================
# 셀렉터 상수 (Contact Update Page)
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
DETAIL_EDIT = 'div.ly_more_menu ul li a:has-text("수정")'

# 수정 레이어
LAYER_EDIT = 'div.layer_area.ly_add_contact'
BTN_DETAIL = 'div.fd_btnarea a:text-is("자세히 입력하기")'
BTN_SAVE = 'div.btn_area button.btn_point:text-is("저장")'

# 입력 필드 (수정 레이어 내부)
INPUT_LASTNAME = 'input[placeholder="성"]'
INPUT_FIRSTNAME = 'input[placeholder="이름"]'
INPUT_NICKNAME = 'input[placeholder="닉네임"]'
INPUT_ORG = 'input[placeholder="소속"]'
INPUT_DEPT = 'input[placeholder="부서"]'
INPUT_POSITION = 'input[placeholder="직책"]'
INPUT_PHONE = 'input[placeholder="전화번호"]'
INPUT_EMAIL = 'input[placeholder="이메일"]'
INPUT_ADDRESS = 'input[placeholder="주소"]'
INPUT_ZIP = 'input[placeholder="우편번호"]'
INPUT_HOMEPAGE = 'input[placeholder="URL"]'
INPUT_MESSENGER = 'input[placeholder="ID"]'
INPUT_MEMO = 'textarea[placeholder="메모(최대 4,000자)"]'
INPUT_ADDRESS_TYPE = 'input[placeholder="주소종류"]'
INPUT_BIRTHDAY_DATE = 'input[type="date"].date'

# 주소 관련 드롭다운
BTN_ADDRESS_SELECT = 'div.lc_article:has(span.lc_lt:text("주소")) .selectbox a.status'
DROPDOWN_ADDRESS_DIRECT = 'ul[style*="translateZ"] li a:has-text("직접입력")'

# =====================
# 유틸 함수
# =====================
def safe_fill(page, selector, value):
    """해당 selector가 존재할 때만 값을 입력한다."""
    if page.locator(selector).count() > 0:
        page.locator(selector).fill(value)

# =====================
# 단계별 함수 분리
# =====================
def search_contact(page, contact_name):
    page.wait_for_selector(SEARCH_INPUT, timeout=5000)
    page.locator(SEARCH_INPUT).fill(contact_name)
    page.locator(SEARCH_SUBMIT).click()
    page.wait_for_selector(SEARCH_RESULT_ROW, timeout=5000)
    page.locator(SEARCH_RESULT_NAME).first.click()
    page.wait_for_selector(DETAIL_NAME, timeout=3000)

def open_edit_layer(page):
    page.locator(DETAIL_SHOW_MORE).click()
    page.wait_for_selector(DETAIL_MORE_MENU, state="visible", timeout=2000)
    page.locator(DETAIL_EDIT).click()
    page.wait_for_selector(LAYER_EDIT, timeout=5000)
    if page.locator(BTN_DETAIL).count() > 0:
        page.locator(BTN_DETAIL).click()

def fill_contact_update_fields(page, app_state=None):
    timestamp = datetime.now().strftime("%m%d%H%M")
    safe_fill(page, INPUT_LASTNAME, "연락처자동화(수정됨)")
    safe_fill(page, INPUT_FIRSTNAME, f"{timestamp}(수정됨)")
    if app_state is not None:
        app_state.contact_name = f"연락처자동화(수정됨){timestamp}(수정됨)"
    safe_fill(page, INPUT_NICKNAME, "자동화닉네임(수정됨)")
    safe_fill(page, INPUT_ORG, "자동화소속(수정됨)")
    safe_fill(page, INPUT_DEPT, "자동화부서(수정됨)")
    safe_fill(page, INPUT_POSITION, "자동화직책(수정됨)")
    safe_fill(page, INPUT_PHONE, "P-12340000")
    safe_fill(page, INPUT_EMAIL, "automation@email.test.mod")
    if page.locator(BTN_ADDRESS_SELECT).count() > 0:
        page.locator(BTN_ADDRESS_SELECT).click()
        page.wait_for_selector(DROPDOWN_ADDRESS_DIRECT, timeout=2000)
        if page.locator(DROPDOWN_ADDRESS_DIRECT).count() > 0:
            page.locator(DROPDOWN_ADDRESS_DIRECT).click()
            page.wait_for_selector(INPUT_ADDRESS_TYPE, timeout=2000)
            if page.locator(INPUT_ADDRESS_TYPE).count() > 0:
                safe_fill(page, INPUT_ADDRESS_TYPE, "자동화주소종류(수정됨)")
    safe_fill(page, INPUT_ZIP, "1230000")
    safe_fill(page, INPUT_ADDRESS, "자동화주소(수정됨)")
    safe_fill(page, INPUT_HOMEPAGE, "automation.url(수정됨)")
    safe_fill(page, INPUT_BIRTHDAY_DATE, "2000-01-02")
    safe_fill(page, INPUT_MESSENGER, "automation_sns_mod")
    safe_fill(page, INPUT_MEMO, "자동화메모(수정됨)")

def save_contact_update(page):
    page.wait_for_selector(BTN_SAVE, timeout=2000)
    page.locator(BTN_SAVE).first.click()

# =====================
# 메인 플로우 함수
# =====================
def update_contact(page, app_state=None):
    """연락처를 검색 후 상세 진입, 수정 레이어에서 값 변경 후 저장한다."""
    search_contact(page, app_state.contact_name)
    open_edit_layer(page)
    fill_contact_update_fields(page, app_state)
    save_contact_update(page)
    return True
