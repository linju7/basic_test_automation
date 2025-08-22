from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (User Create Page)
# =====================

# 페이지 진입 버튼
BTN_ADD_MEMBER = 'button.lw_btn_point:text-is("구성원 추가")'
BTN_SHOW_ALL = 'button.opt_toggle.fold:text-is("모든 항목 표시")'
BTN_EXPAND_ALL = 'button.opt_toggle.fold'

# 폼 필드 - 기본 정보
INPUT_LAST_NAME = 'input.lw_input[placeholder="성"][maxlength="80"]'
INPUT_FIRST_NAME = 'input.lw_input[placeholder="이름"][maxlength="80"]'
INPUT_NICKNAME = 'input.lw_input[placeholder="닉네임"]'
INPUT_USER_ID = 'input.lw_input[placeholder="ID"]'
INPUT_INTERNAL_NUMBER = 'input.lw_input[placeholder="사내 번호"]'
INPUT_PHONE_NUMBER = 'input.lw_input[placeholder="전화번호"]'
INPUT_WORKPLACE = 'input.lw_input[placeholder="근무처"]'
INPUT_TASK = 'input.lw_input[placeholder="담당 업무"]'
INPUT_EMPLOYEE_NUMBER = 'input.lw_input[placeholder="사원 번호"]'
INPUT_BIRTHDAY = 'input.lw_input[name="birthday"]'
INPUT_HIRED_DATE = 'input.lw_input[name="hiredDate"]'

# 폼 필드 - 다국어명
INPUT_JAPANESE_LAST = 'input.lw_input[placeholder="姓(日本語)"]'
INPUT_JAPANESE_FIRST = 'input.lw_input[placeholder="名(日本語)"]'
INPUT_ENGLISH_LAST = 'input.lw_input[placeholder="Last"]'
INPUT_ENGLISH_FIRST = 'input.lw_input[placeholder="First"]'
INPUT_KOREAN_LAST = 'input.lw_input[placeholder="성"][maxlength="100"]'
INPUT_KOREAN_FIRST = 'input.lw_input[placeholder="이름"][maxlength="100"]'
INPUT_SIMPLIFIED_CHINESE_LAST = 'input.lw_input[placeholder="姓(简体中文)"]'
INPUT_SIMPLIFIED_CHINESE_FIRST = 'input.lw_input[placeholder="名(简体中文)"]'
INPUT_TRADITIONAL_CHINESE_LAST = 'input.lw_input[placeholder="姓(繁體中文)"]'
INPUT_TRADITIONAL_CHINESE_FIRST = 'input.lw_input[placeholder="名(繁體中文)"]'

# 폼 필드 - 이메일
BTN_ADD_SUB_EMAIL = 'button.generate:text("보조 이메일 추가")'
INPUT_SUB_EMAIL = 'input.lw_input.email_id[placeholder="보조 이메일"]'
INPUT_PRIVATE_EMAIL = 'input.lw_input[placeholder="개인 이메일"]'
INPUT_PRIVATE_DOMAIN = 'input.lw_input[placeholder="직접 입력"]'

# 셀렉트 박스
SELECT_USER_TYPE = '//div[i[text()="사용자 유형"]]//select[@id="member_type"]'
SELECT_POSITION = '//div[i[text()="직급"]]//select[@id="member_type"]'

# 액션 버튼
BTN_ADD = 'button.lw_btn_point:text-is("추가")'

# 성공 모달
MODAL_SUCCESS = 'div.ly_common.ly_page.ly_member_added'
MODAL_SUCCESS_TITLE = 'div.ly_member_added h3.tit:text("구성원 추가 완료")'
MODAL_SUCCESS_BTN_CONFIRM = 'div.ly_member_added button.lw_btn:text("확인")'
MODAL_SUCCESS_BTN_CONTINUE = 'div.ly_member_added button.lw_btn_point:text("계속 추가")'


def create_user_info():
    """사용자 입력 데이터를 생성한다."""
    timestamp = datetime.now().strftime("%m%d%H%M")
    user_id = "junil_" + timestamp
    
    user_info = {
        "timestamp": timestamp,
        "user_id": user_id,
        "basic_fields": {
            "last_name": "자동화_",
            "first_name": timestamp,
            "nickname": "자동화_닉네임",
            "internal_number": f"P-{timestamp}",
            "phone_number": f"T-{timestamp}",
            "workplace": "자동화_근무처",
            "task": "자동화_담당업무",
            "employee_number": f"자동화_{timestamp}",
            "birthday": "1999. 12. 31",
            "hired_date": "2000. 01. 01"
        },
        "multilingual_fields": {
            "japanese_last": "일본어성",
            "japanese_first": "일본어이름", 
            "english_last": "영어성",
            "english_first": "영어이름",
            "korean_last": "한국어성",
            "korean_first": "한국어이름",
            "simplified_chinese_last": "간체성",
            "simplified_chinese_first": "간체이름",
            "traditional_chinese_last": "번체성",
            "traditional_chinese_first": "번체이름"
        },
        "email_fields": {
            "sub_email": f"sub_email_{timestamp}",
            "private_email": f"private_email_{timestamp}",
            "private_domain": "private.domain"
        }
    }
    
    return user_info


def wait_and_click(page, selector, timeout=5000):
    """selector가 나타날 때까지 대기 후 클릭한다."""
    page.wait_for_selector(selector, timeout=timeout)
    page.locator(selector).click()


def open_user_add_page(page):
    """구성원 추가 페이지 열기"""
    page.goto(settings.USERS_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_ADD_MEMBER, timeout=5000)
    if page.locator(BTN_ADD_MEMBER).count() > 0:
        page.locator(BTN_ADD_MEMBER).click()
        page.wait_for_selector(BTN_SHOW_ALL, timeout=5000)
        return True
    return False


def expand_all_fields(page):
    """모든 항목 표시 버튼 클릭"""
    if page.locator(BTN_EXPAND_ALL).count() > 0:
        button = page.locator(BTN_EXPAND_ALL)
        if button.is_visible():
            button.click()
            return True
    return True


def fill_user_info(page, app_state=None):
    """사용자 정보 입력 폼을 채운다."""
    # 사용자 정보 객체 생성
    user_info = create_user_info()
    
    # app_state에 저장
    if app_state is not None:
        app_state.global_user_id = user_info["user_id"]
        app_state.user_info = user_info

    # 기본 필드 입력
    basic = user_info["basic_fields"]
    basic_fields = [
        ("성", INPUT_LAST_NAME, basic["last_name"]),
        ("이름", INPUT_FIRST_NAME, basic["first_name"]),
        ("닉네임", INPUT_NICKNAME, basic["nickname"]),
        ("ID", INPUT_USER_ID, user_info["user_id"]),
        ("사내 번호", INPUT_INTERNAL_NUMBER, basic["internal_number"]),
        ("전화번호", INPUT_PHONE_NUMBER, basic["phone_number"]),
        ("근무처", INPUT_WORKPLACE, basic["workplace"]),
        ("담당 업무", INPUT_TASK, basic["task"]),
        ("사원 번호", INPUT_EMPLOYEE_NUMBER, basic["employee_number"]),
        ("생일", INPUT_BIRTHDAY, basic["birthday"]),
        ("입사일", INPUT_HIRED_DATE, basic["hired_date"])
    ]
    for _, selector, value in basic_fields:
        safe_fill(page, selector, value)

    # 사용자 유형 1번째 선택
    user_type_select = page.locator(SELECT_USER_TYPE)
    if user_type_select.count() > 0:
        first_value = user_type_select.locator('option').nth(1).get_attribute('value')
        user_type_select.select_option(value=first_value)

    # 직급 1번째 선택
    position_select = page.locator(SELECT_POSITION)
    if position_select.count() > 0:
        first_value = position_select.locator('option').nth(1).get_attribute('value')
        position_select.select_option(value=first_value)

    # 다국어 필드 입력
    multilingual = user_info["multilingual_fields"]
    multilingual_fields = [
        ("姓(日本語)", INPUT_JAPANESE_LAST, multilingual["japanese_last"]),
        ("名(日本語)", INPUT_JAPANESE_FIRST, multilingual["japanese_first"]),
        ("Last", INPUT_ENGLISH_LAST, multilingual["english_first"]),  # 순서 바꿈 (Last=이름)
        ("First", INPUT_ENGLISH_FIRST, multilingual["english_last"]),  # 순서 바꿈 (First=성)
        ("성", INPUT_KOREAN_LAST, multilingual["korean_last"]),
        ("이름", INPUT_KOREAN_FIRST, multilingual["korean_first"]),
        ("姓(简体中文)", INPUT_SIMPLIFIED_CHINESE_LAST, multilingual["simplified_chinese_last"]),
        ("名(简体中文)", INPUT_SIMPLIFIED_CHINESE_FIRST, multilingual["simplified_chinese_first"]),
        ("姓(繁體中文)", INPUT_TRADITIONAL_CHINESE_LAST, multilingual["traditional_chinese_last"]),
        ("名(繁體中文)", INPUT_TRADITIONAL_CHINESE_FIRST, multilingual["traditional_chinese_first"]),
    ]
    for _, selector, value in multilingual_fields:
        safe_fill(page, selector, value)

    # 보조 이메일 추가
    email = user_info["email_fields"]
    if page.locator(BTN_ADD_SUB_EMAIL).count() > 0:
        page.locator(BTN_ADD_SUB_EMAIL).click()
        safe_fill(page, INPUT_SUB_EMAIL, email["sub_email"])

    # 개인 이메일 입력
    safe_fill(page, INPUT_PRIVATE_EMAIL, email["private_email"])
    safe_fill(page, INPUT_PRIVATE_DOMAIN, email["private_domain"])

    return True


def click_add_button(page):
    """추가 버튼 클릭"""
    if page.locator(BTN_ADD).count() > 0:
        page.locator(BTN_ADD).click()

    page.wait_for_selector(MODAL_SUCCESS_BTN_CONFIRM, timeout=5000)
    if page.locator(MODAL_SUCCESS_BTN_CONFIRM).count() > 0:
        page.locator(MODAL_SUCCESS_BTN_CONFIRM).click()

    return True


# =====================
# 메인 플로우 함수
# =====================
def create_user(page, app_state=None):
    """구성원 추가 플로우를 순차적으로 실행"""
    if not open_user_add_page(page):
        return False
    if not expand_all_fields(page):
        return False
    if not fill_user_info(page, app_state):
        return False
    if not click_add_button(page):
        return False
    return True
