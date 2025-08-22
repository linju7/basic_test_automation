from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (Contact Add Page)
# =====================

# 버튼/레이어
BTN_NEW = 'a:has-text("새로 만들기")'
DROPDOWN_DIRECT = 'div.main_pane div.ly_context ul li a:has-text("외부 연락처 직접 입력 ")'
LAYER_CONTACT_ADD = 'div.layer_pd h3.lc_h3:text("외부 연락처 만들기")'
BTN_DETAIL = 'div.fd_btnarea a:text-is("자세히 입력하기")'
BTN_SAVE = 'div.btn_area button.btn_point:text-is("저장")'

# 입력 필드
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


def open_contact_add_layer(page):
    """외부 연락처 추가 레이어 열기"""
    page.wait_for_selector(BTN_NEW, timeout=5000)
    page.locator(BTN_NEW).click()
    
    # 드롭다운이 보일 때까지 기다리기
    page.wait_for_selector('div.ly_context', timeout=5000, state='visible')
    page.wait_for_timeout(500)  
    
    # 외부연락처 직접 입력 선택
    page.wait_for_selector(DROPDOWN_DIRECT, timeout=3000, state='visible')
    page.locator(DROPDOWN_DIRECT).first.click()
    page.wait_for_selector(LAYER_CONTACT_ADD, timeout=5000)
    return True


def click_detail_button(page):
    """'자세히 입력하기' 버튼을 클릭하기"""
    if page.locator(BTN_DETAIL).count() > 0:
        page.locator(BTN_DETAIL).click()
        return True
    return False


def fill_contact_info(page, app_state=None):
    """외부 연락처 필드에 값을 입력한다."""

    # 유니크한 값 세팅을 위해 현재 시간값 사용
    timestamp = datetime.now().strftime("%m%d%H%M")

    safe_fill(page, INPUT_LASTNAME, "연락처자동화")
    safe_fill(page, INPUT_FIRSTNAME, timestamp)
    # 조회를 위해 정보 저장 필요 -> app_state 에 기록 
    if app_state is not None:
        app_state.contact_name = f"연락처자동화{timestamp}"
    
    safe_fill(page, INPUT_NICKNAME, "자동화닉네임")
    safe_fill(page, INPUT_ORG, "자동화소속")
    safe_fill(page, INPUT_DEPT, "자동화부서")
    safe_fill(page, INPUT_POSITION, "자동화직책")
    safe_fill(page, INPUT_PHONE, "P-1234")
    safe_fill(page, INPUT_EMAIL, "automation@email.test")

    # 주소: 드랍다운 열고 '직접입력' 선택
    if page.locator(BTN_ADDRESS_SELECT).count() > 0:
        page.locator(BTN_ADDRESS_SELECT).click()
        page.wait_for_selector(DROPDOWN_ADDRESS_DIRECT, timeout=2000)
        if page.locator(DROPDOWN_ADDRESS_DIRECT).count() > 0:
            page.locator(DROPDOWN_ADDRESS_DIRECT).click()
            page.wait_for_selector(INPUT_ADDRESS_TYPE, timeout=2000)
            if page.locator(INPUT_ADDRESS_TYPE).count() > 0:
                safe_fill(page, INPUT_ADDRESS_TYPE, "자동화주소종류")

    safe_fill(page, INPUT_ZIP, "123")
    safe_fill(page, INPUT_ADDRESS, "자동화주소")
    safe_fill(page, INPUT_HOMEPAGE, "automation.url")
    safe_fill(page, INPUT_BIRTHDAY_DATE, "2000-01-01")
    safe_fill(page, INPUT_MESSENGER, "automation_sns")
    safe_fill(page, INPUT_MEMO, "자동화메모")
    return True


def click_save_button(page):
    """'저장' 버튼을 클릭한다."""
    if page.locator(BTN_SAVE).count() > 0:
        page.wait_for_timeout(2000)
        page.locator(BTN_SAVE).first.click()
        page.wait_for_timeout(2000)
        return True
    return False


# =====================
# 메인 플로우 함수
# =====================
def create_contact(page, app_state=None):
    """외부 연락처 추가 플로우를 순차적으로 실행"""
    page.goto(settings.CONTACT_URLS[settings.ENVIRONMENT])
    if not open_contact_add_layer(page):
        return False
    if not click_detail_button(page):
        return False
    if not fill_contact_info(page, app_state):
        return False
    if not click_save_button(page):
        return False
    return True
