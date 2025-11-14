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

# 폼 필드 - 메신저/SNS
INPUT_SNS_NAME = 'input.lw_input.sns_name[placeholder="직접 입력"]'
INPUT_SNS_ID = 'div.field:has(i.hd:text("메신저/SNS")) input.lw_input[placeholder="ID"]'

# 셀렉트 박스 (페이지에 select#member_type가 4개 존재하므로 정확히 구분 필요)
SELECT_USER_TYPE = 'div.field:has(i.hd:text("사용자 유형")) select#member_type'
SELECT_LEVEL = 'div.field:has(i.hd:text("직급")) select#member_type'
SELECT_POSITION_AFTER_ORG = 'div.item:has(span.fmbox) select#member_type'
SELECT_MESSENGER = 'div.field:has(i.hd:text("메신저/SNS")) select#member_type'

# 소속 조직 관련
BTN_ADD_ORGUNIT = 'button.generate:text("소속 조직 추가")'
ORGUNIT_LAYER = 'div.ly_common.ly_page.ly_org_tree'
ORGUNIT_CONFIRM_BTN = 'div.ly_org_tree button.lw_btn_point:text-is("확인")'

# 액션 버튼
BTN_ADD = 'button.lw_btn_point:text-is("추가")'

# 성공 모달
MODAL_SUCCESS = 'div.ly_common.ly_page.ly_member_added'
MODAL_SUCCESS_TITLE = 'div.ly_member_added h3.tit:text("구성원 추가 완료")'
MODAL_SUCCESS_BTN_CONFIRM = 'div.ly_member_added button.lw_btn:text("확인")'
MODAL_SUCCESS_BTN_CONTINUE = 'div.ly_member_added button.lw_btn_point:text("계속 추가")'


# =====================
# 데이터 생성 함수
# =====================
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


# =====================
# 유틸리티 함수
# =====================
def select_option_by_text(page, select_selector, option_text):
    """셀렉트 박스에서 텍스트로 옵션 선택"""
    try:
        select = page.locator(select_selector)
        if select.count() > 0:
            options = select.locator('option')
            for i in range(options.count()):
                option = options.nth(i)
                text = option.inner_text().strip()
                if text == option_text:
                    value = option.get_attribute('value')
                    select.select_option(value=value)
                    return True
        return False
    except Exception as e:
        print(f"옵션 선택 실패: {e}")
        return False


def select_first_option(page, select_selector):
    """셀렉트 박스에서 첫 번째 옵션 선택 (0번 제외)"""
    try:
        select = page.locator(select_selector)
        if select.count() > 0:
            first_value = select.locator('option').nth(1).get_attribute('value')
            select.select_option(value=first_value)
            return True
        return False
    except Exception as e:
        print(f"첫 번째 옵션 선택 실패: {e}")
        return False


# =====================
# 페이지 진입 및 설정
# =====================
def open_user_add_page(page):
    """구성원 추가 페이지 열기"""
    page.goto(settings.USERS_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_ADD_MEMBER, timeout=30000)
    if page.locator(BTN_ADD_MEMBER).count() > 0:
        page.locator(BTN_ADD_MEMBER).click()
        page.wait_for_selector(BTN_SHOW_ALL, timeout=30000)
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


# =====================
# 단계별 입력 함수
# =====================
def fill_basic_fields(page, user_info):
    """기본 정보 필드 입력"""
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
    
    return True


def select_user_type_and_level(page, app_state, auto_apply):
    """사용자 유형과 직급 선택"""
    # 사용자 유형 선택
    if auto_apply and app_state and app_state.usertype_name:
        if not select_option_by_text(page, SELECT_USER_TYPE, app_state.usertype_name):
            print(f"⚠️ 사용자 유형 '{app_state.usertype_name}' 선택 실패 (첫 번째 옵션으로 대체)")
            select_first_option(page, SELECT_USER_TYPE)
    else:
        select_first_option(page, SELECT_USER_TYPE)
    
    # 직급 선택
    if auto_apply and app_state and app_state.level_name:
        if not select_option_by_text(page, SELECT_LEVEL, app_state.level_name):
            print(f"⚠️ 직급 '{app_state.level_name}' 선택 실패 (첫 번째 옵션으로 대체)")
            select_first_option(page, SELECT_LEVEL)
    else:
        select_first_option(page, SELECT_LEVEL)
    
    return True


def fill_multilingual_fields(page, user_info):
    """다국어 필드 입력"""
    multilingual = user_info["multilingual_fields"]
    multilingual_fields = [
        ("姓(日本語)", INPUT_JAPANESE_LAST, multilingual["japanese_last"]),
        ("名(日本語)", INPUT_JAPANESE_FIRST, multilingual["japanese_first"]),
        ("Last", INPUT_ENGLISH_LAST, multilingual["english_first"]),
        ("First", INPUT_ENGLISH_FIRST, multilingual["english_last"]),
        ("성", INPUT_KOREAN_LAST, multilingual["korean_last"]),
        ("이름", INPUT_KOREAN_FIRST, multilingual["korean_first"]),
        ("姓(简体中文)", INPUT_SIMPLIFIED_CHINESE_LAST, multilingual["simplified_chinese_last"]),
        ("名(简体中文)", INPUT_SIMPLIFIED_CHINESE_FIRST, multilingual["simplified_chinese_first"]),
        ("姓(繁體中文)", INPUT_TRADITIONAL_CHINESE_LAST, multilingual["traditional_chinese_last"]),
        ("名(繁體中文)", INPUT_TRADITIONAL_CHINESE_FIRST, multilingual["traditional_chinese_first"]),
    ]
    
    for _, selector, value in multilingual_fields:
        safe_fill(page, selector, value)
    
    return True


def fill_email_fields(page, user_info):
    """이메일 정보 입력"""
    email = user_info["email_fields"]
    
    # 보조 이메일 추가
    if page.locator(BTN_ADD_SUB_EMAIL).count() > 0:
        page.locator(BTN_ADD_SUB_EMAIL).click()
        safe_fill(page, INPUT_SUB_EMAIL, email["sub_email"])
    
    # 개인 이메일 입력
    safe_fill(page, INPUT_PRIVATE_EMAIL, email["private_email"])
    safe_fill(page, INPUT_PRIVATE_DOMAIN, email["private_domain"])
    
    return True


def fill_messenger_info(page):
    """메신저/SNS 정보 입력"""
    try:
        messenger_select = page.locator(SELECT_MESSENGER)
        if messenger_select.count() == 0:
            print("⚠️ 메신저/SNS 셀렉트를 찾을 수 없음")
            return False
        
        # label(텍스트)로 직접 선택
        messenger_select.select_option(label="직접 입력")
        page.wait_for_timeout(1000)
        
        # SNS 이름 및 ID 입력
        safe_fill(page, INPUT_SNS_NAME, "자동화SNS")
        safe_fill(page, INPUT_SNS_ID, "auto_sns")
        
        return True
    except Exception as e:
        print(f"⚠️ 메신저/SNS 정보 입력 중 오류: {e}")
        return False


def add_orgunit_and_position(page, app_state, auto_apply):
    """소속 조직 및 직책 추가 (auto_apply=True일 때만)"""
    if not auto_apply or not app_state:
        return True
    
    if not app_state.org_name:
        print("⚠️ app_state에 org_name이 없어 조직 추가를 건너뜁니다.")
        return True
    
    try:
        # 1. 소속 조직 추가 버튼 클릭
        btn_add_org = page.locator(BTN_ADD_ORGUNIT)
        if btn_add_org.count() == 0:
            print("❌ 소속 조직 추가 버튼을 찾을 수 없습니다.")
            return False
        
        btn_add_org.click()
        page.wait_for_selector(ORGUNIT_LAYER, timeout=5000)
        page.wait_for_timeout(3000)
        
        # 2. 조직 선택
        org_name = app_state.org_name
        org_link_selector = f'a.group_name:has(span.txt:text-is("{org_name}"))'
        org_item = page.locator(org_link_selector)
        
        if org_item.count() == 0:
            print(f"❌ 조직 '{org_name}'을 찾을 수 없습니다.")
            return False
        
        org_item.first.click()
        page.wait_for_timeout(500)
        
        # 3. 확인 버튼 클릭
        confirm_btn = page.locator(ORGUNIT_CONFIRM_BTN)
        if confirm_btn.count() == 0:
            print("❌ 확인 버튼을 찾을 수 없습니다.")
            return False
        
        confirm_btn.click()
        page.wait_for_timeout(1000)
        
        # 4. 직책 선택
        if app_state.position_name:
            page.wait_for_selector(SELECT_POSITION_AFTER_ORG, timeout=5000)
            if not select_option_by_text(page, SELECT_POSITION_AFTER_ORG, app_state.position_name):
                print(f"⚠️ 직책 '{app_state.position_name}' 선택 실패 (첫 번째 옵션으로 대체)")
                select_first_option(page, SELECT_POSITION_AFTER_ORG)
        else:
            select_first_option(page, SELECT_POSITION_AFTER_ORG)
        
        return True
    except Exception as e:
        print(f"❌ 조직/직책 추가 중 오류 발생: {e}")
        return False


def click_add_button(page):
    """추가 버튼 클릭 및 성공 모달 처리"""
    if page.locator(BTN_ADD).count() > 0:
        page.locator(BTN_ADD).click()
    
    page.wait_for_selector(MODAL_SUCCESS_BTN_CONFIRM, timeout=30000)
    if page.locator(MODAL_SUCCESS_BTN_CONFIRM).count() > 0:
        page.locator(MODAL_SUCCESS_BTN_CONFIRM).click()
    
    return True


# =====================
# 메인 플로우 함수
# =====================
def fill_user_info(page, user_info, app_state, auto_apply):
    """
    사용자 정보 입력 플로우를 순차적으로 실행
    
    Args:
        page: Playwright page 객체
        user_info: 사용자 정보 딕셔너리
        app_state: 전역 상태 객체
        auto_apply: app_state 값 자동 적용 여부
    """
    if not fill_basic_fields(page, user_info):
        print("기본 정보 입력 실패")
        return False
    
    if not select_user_type_and_level(page, app_state, auto_apply):
        print("사용자 유형/직급 선택 실패")
        return False
    
    if not fill_multilingual_fields(page, user_info):
        print("다국어 필드 입력 실패")
        return False
    
    if not fill_email_fields(page, user_info):
        print("이메일 정보 입력 실패")
        return False
    
    if not fill_messenger_info(page):
        print("⚠️ 메신저/SNS 정보 입력 실패 (계속 진행)")
    
    if not add_orgunit_and_position(page, app_state, auto_apply):
        print("⚠️ 조직/직책 추가 실패 (계속 진행)")
    
    return True


def create_user(page, app_state=None, auto_apply=False):
    """
    구성원 추가 플로우를 순차적으로 실행
    
    Args:
        page: Playwright page 객체
        app_state: 전역 상태 객체
        auto_apply: app_state 값 자동 적용 여부 (시나리오 테스트용)
    """
    print("\n구성원 추가 자동화 시작")
    if auto_apply:
        print("📌 시나리오 모드: app_state의 조직/직책/직급/유형 자동 적용")
    
    # 사용자 정보 생성 및 저장
    user_info = create_user_info()
    if app_state is not None:
        app_state.global_user_id = user_info["user_id"]
        app_state.user_info = user_info
    
    # 순차적 실행
    if not open_user_add_page(page):
        print("구성원 추가 자동화 실패 - open_user_add_page\n")
        return False
    
    if not expand_all_fields(page):
        print("구성원 추가 자동화 실패 - expand_all_fields\n")
        return False
    
    if not fill_user_info(page, user_info, app_state, auto_apply):
        print("구성원 추가 자동화 실패 - fill_user_info\n")
        return False
    
    if not click_add_button(page):
        print("구성원 추가 자동화 실패 - click_add_button\n")
        return False
    
    print("구성원 추가 자동화 완료\n")
    return True
