from automation.config.settings import settings
from datetime import datetime

# 주요 셀렉터 상수
BTN_ADD_MEMBER = 'button.lw_btn_point:text-is("구성원 추가")'
BTN_SHOW_ALL = 'button.opt_toggle.fold:text-is("모든 항목 표시")'
BTN_ADD = 'button.lw_btn_point:text-is("추가")'
BTN_CONFIRM = 'button.lw_btn:text-is("확인")'


def safe_fill(page, selector, value):
    """해당 selector가 존재할 때만 값을 입력한다."""
    if page.locator(selector).count() > 0:
        page.locator(selector).fill(value)


def wait_and_click(page, selector, timeout=5000):
    """selector가 나타날 때까지 대기 후 클릭한다."""
    page.wait_for_selector(selector, timeout=timeout)
    page.locator(selector).click()


def fill_user_info(page, app_state=None):
    """사용자 정보 입력 폼을 채운다."""
    timestamp = datetime.now().strftime("%m%d%H%M")
    user_id = "junil_" + timestamp

    if app_state is not None:
        app_state.global_user_id = user_id

    # 모든 항목 표시 버튼 클릭
    if page.locator('button.opt_toggle.fold').count() > 0:
        button = page.locator('button.opt_toggle.fold')
        if button.is_visible():
            button.click()

    # 기본 필드 입력
    basic_fields = [
        ("성", 'input.lw_input[placeholder="성"][maxlength="80"]', "자동화_"),
        ("이름", 'input.lw_input[placeholder="이름"][maxlength="80"]', timestamp),
        ("닉네임", 'input.lw_input[placeholder="닉네임"]', "자동화_닉네임"),
        ("ID", 'input.lw_input[placeholder="ID"]', user_id),
        ("사내 번호", 'input.lw_input[placeholder="사내 번호"]', f"P-{timestamp}"),
        ("전화번호", 'input.lw_input[placeholder="전화번호"]', f"T-{timestamp}"),
        ("근무처", 'input.lw_input[placeholder="근무처"]', "자동화_근무처"),
        ("담당 업무", 'input.lw_input[placeholder="담당 업무"]', "자동화_담당업무"),
        ("사원 번호", 'input.lw_input[placeholder="사원 번호"]', f"자동화_{timestamp}"),
        ("생일", 'input.lw_input[name="birthday"]', "1999. 12. 31"),
        ("입사일", 'input.lw_input[name="hiredDate"]', "2000. 01. 01")
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
    multilingual_fields = [
        ("姓(日本語)", 'input.lw_input[placeholder="姓(日本語)"]', "일본어성"),
        ("名(日本語)", 'input.lw_input[placeholder="名(日本語)"]', "일본어이름"),
        ("Last", 'input.lw_input[placeholder="Last"]', "영어성"),
        ("First", 'input.lw_input[placeholder="First"]', "영어이름"),
        ("성", 'input.lw_input[placeholder="성"][maxlength="100"]', "한국어성"),
        ("이름", 'input.lw_input[placeholder="이름"][maxlength="100"]', "한국어이름"),
        ("姓(简体中文)", 'input.lw_input[placeholder="姓(简体中文)"]', "간체성"),
        ("名(简体中文)", 'input.lw_input[placeholder="名(简体中文)"]', "간체이름"),
        ("姓(繁體中文)", 'input.lw_input[placeholder="姓(繁體中文)"]', "번체성"),
        ("名(繁體中文)", 'input.lw_input[placeholder="名(繁體中文)"]', "번체이름"),
    ]
    for _, selector, value in multilingual_fields:
        safe_fill(page, selector, value)

    # 보조 이메일 추가
    if page.locator('button.generate', has_text="보조 이메일 추가").count() > 0:
        page.locator('button.generate', has_text="보조 이메일 추가").click()
        safe_fill(page, 'input.lw_input.email_id[placeholder="보조 이메일"]', f"sub_email_{timestamp}")

    # 개인 이메일 입력
    safe_fill(page, 'input.lw_input[placeholder="개인 이메일"]', f"private_email_{timestamp}")
    safe_fill(page, 'input.lw_input[placeholder="직접 입력"]', "private.domain")

    return page


def create_user(page, app_state=None):
    """구성원 추가 플로우를 순차적으로 실행한다."""
    page.goto(settings.get_users_url())
    page.wait_for_selector(BTN_ADD_MEMBER, timeout=5000)

    if page.locator(BTN_ADD_MEMBER).count() > 0:
        page.locator(BTN_ADD_MEMBER).click()
        page.wait_for_selector(BTN_SHOW_ALL, timeout=5000)

    fill_user_info(page, app_state)

    if page.locator(BTN_ADD).count() > 0:
        page.locator(BTN_ADD).click()
    if page.locator(BTN_CONFIRM).count() > 0:
        page.locator(BTN_CONFIRM).click()
