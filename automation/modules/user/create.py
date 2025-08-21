from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (User Create Page)
# =====================
BTN_ADD_MEMBER = 'button.lw_btn_point:text-is("구성원 추가")'
BTN_SHOW_ALL = 'button.opt_toggle.fold:text-is("모든 항목 표시")'
BTN_ADD = 'button.lw_btn_point:text-is("추가")'
BTN_CONFIRM = 'button.lw_btn:text-is("확인")'


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
    if page.locator('button.opt_toggle.fold').count() > 0:
        button = page.locator('button.opt_toggle.fold')
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
        ("성", 'input.lw_input[placeholder="성"][maxlength="80"]', basic["last_name"]),
        ("이름", 'input.lw_input[placeholder="이름"][maxlength="80"]', basic["first_name"]),
        ("닉네임", 'input.lw_input[placeholder="닉네임"]', basic["nickname"]),
        ("ID", 'input.lw_input[placeholder="ID"]', user_info["user_id"]),
        ("사내 번호", 'input.lw_input[placeholder="사내 번호"]', basic["internal_number"]),
        ("전화번호", 'input.lw_input[placeholder="전화번호"]', basic["phone_number"]),
        ("근무처", 'input.lw_input[placeholder="근무처"]', basic["workplace"]),
        ("담당 업무", 'input.lw_input[placeholder="담당 업무"]', basic["task"]),
        ("사원 번호", 'input.lw_input[placeholder="사원 번호"]', basic["employee_number"]),
        ("생일", 'input.lw_input[name="birthday"]', basic["birthday"]),
        ("입사일", 'input.lw_input[name="hiredDate"]', basic["hired_date"])
    ]
    for _, selector, value in basic_fields:
        safe_fill(page, selector, value)

    # 사용자 유형 1번째 선택
    user_type_select = page.locator("//div[i[text()='사용자 유형']]//select[@id='member_type']")
    if user_type_select.count() > 0:
        first_value = user_type_select.locator('option').nth(1).get_attribute('value')
        user_type_select.select_option(value=first_value)

    # 직급 1번째 선택
    position_select = page.locator("//div[i[text()='직급']]//select[@id='member_type']")
    if position_select.count() > 0:
        first_value = position_select.locator('option').nth(1).get_attribute('value')
        position_select.select_option(value=first_value)

    # 다국어 필드 입력
    multilingual = user_info["multilingual_fields"]
    multilingual_fields = [
        ("姓(日本語)", 'input.lw_input[placeholder="姓(日本語)"]', multilingual["japanese_last"]),
        ("名(日本語)", 'input.lw_input[placeholder="名(日本語)"]', multilingual["japanese_first"]),
        ("Last", 'input.lw_input[placeholder="Last"]', multilingual["english_first"]),  # 순서 바꿈 (Last=이름)
        ("First", 'input.lw_input[placeholder="First"]', multilingual["english_last"]),  # 순서 바꿈 (First=성)
        ("성", 'input.lw_input[placeholder="성"][maxlength="100"]', multilingual["korean_last"]),
        ("이름", 'input.lw_input[placeholder="이름"][maxlength="100"]', multilingual["korean_first"]),
        ("姓(简体中文)", 'input.lw_input[placeholder="姓(简体中文)"]', multilingual["simplified_chinese_last"]),
        ("名(简体中文)", 'input.lw_input[placeholder="名(简体中文)"]', multilingual["simplified_chinese_first"]),
        ("姓(繁體中文)", 'input.lw_input[placeholder="姓(繁體中文)"]', multilingual["traditional_chinese_last"]),
        ("名(繁體中文)", 'input.lw_input[placeholder="名(繁體中文)"]', multilingual["traditional_chinese_first"]),
    ]
    for _, selector, value in multilingual_fields:
        safe_fill(page, selector, value)

    # 보조 이메일 추가
    email = user_info["email_fields"]
    if page.locator('button.generate', has_text="보조 이메일 추가").count() > 0:
        page.locator('button.generate', has_text="보조 이메일 추가").click()
        safe_fill(page, 'input.lw_input.email_id[placeholder="보조 이메일"]', email["sub_email"])

    # 개인 이메일 입력
    safe_fill(page, 'input.lw_input[placeholder="개인 이메일"]', email["private_email"])
    safe_fill(page, 'input.lw_input[placeholder="직접 입력"]', email["private_domain"])

    return True


def click_add_button(page):
    """추가 버튼 클릭"""
    if page.locator(BTN_ADD).count() > 0:
        page.locator(BTN_ADD).click()
        return True
    return False


def click_confirm_button(page):
    """확인 버튼 클릭"""
    if page.locator(BTN_CONFIRM).count() > 0:
        page.locator(BTN_CONFIRM).click()
        return True
    return False


def wait_success_modal(page):
    """성공 모달 확인 및 닫기"""
    try:
        page.wait_for_selector("div.ly_member_added h3.tit:text('구성원 추가 완료')", timeout=5000)
        if page.locator("div.ly_member_added button.lw_btn:text('확인')").count() > 0:
            page.locator("div.ly_member_added button.lw_btn:text('확인')").click()
        return True
    except Exception:
        return False


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
    if not click_confirm_button(page):
        return False
    if not wait_success_modal(page):
        return False
    return True
