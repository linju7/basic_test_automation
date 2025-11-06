from playwright.sync_api import Page
from automation.core.safe_fill import safe_fill
from automation.config.settings import settings
# =====================
# 셀렉터 상수 (User Retrieve Page)
# =====================

# 검색 관련
BTN_SEARCH = 'button.btn_search'
INPUT_SEARCH = '#search_input'
USER_NAME_CELL = 'div.lw_td.user_name'

# 사용자 정보 표시 영역
BTN_MANAGE = '.fm_members button.opt_toggle'
AREA_MEMBER_INFO = '.fm_members'
AREA_MEMBER_MINIMIZED = '.fm_members.minimize'

# 기본 정보 추출 셀렉터
TEXT_NAME = '.fm_members .member .infor .name strong'
TEXT_NICKNAME = '.fm_members .member .infor .name.nickname'
TEXT_EMAIL = '.fm_members .member .infor .box .email'

# 다국어명 추출
TEXT_LANG_NAMES = '.fm_members .member .infor .name.lang'

# 필드별 정보 추출 (특수 필드)
PHONE_SELECTOR = '.fm_members li.box:has(em.h_li:text-is("휴대폰")) ul.txt_box'
PHONE_ALT_SELECTORS = [
    '.fm_members li:has(em:text-is("휴대폰")) ul.txt_box',
    '.fm_members li.box:has(em:text-is("휴대폰")) ul',
    '.fm_members li:has(em:text-is("휴대폰")) ul'
]

SUB_EMAIL_SELECTORS = [
    '.fm_members li.box:has(em.h_li:text-is("보조 이메일")) ul.txt_box li.txt',
    '.fm_members li.box:has(em.h_li:text-is("보조 이메일")) ul.txt_box',
    '.fm_members li:has(em:text-is("보조 이메일")) ul.txt_box li.txt',
    '.fm_members li:has(em:text-is("보조 이메일")) ul.txt_box'
]

PRIVATE_EMAIL_SELECTORS = [
    '.fm_members li.box:has(em.h_li:text-is("개인 이메일")) a.link',
    '.fm_members li.box:has(em.h_li:text-is("개인 이메일")) .link',
    '.fm_members li:has(em:text-is("개인 이메일")) a.link',
    '.fm_members li:has(em:text-is("개인 이메일")) .link'
]

# 일반 필드 추출 템플릿
FIELD_GENERAL_SELECTORS_TEMPLATE = [
    '.fm_members li.box:has(em.h_li:text-is("{field_name}")) .txt',
    '.fm_members li.box:has(em.h_li:text-is("{field_name}")) span.txt',
    '.fm_members li:has(em:text-is("{field_name}")) .txt',
    '.fm_members li:has(em:text-is("{field_name}")) span.txt'
]


def access_user_detail(page: Page, user_id: str):
    """사용자 상세 페이지 접근"""
    page.goto(settings.USERS_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_SEARCH, timeout=30000)
    page.locator(BTN_SEARCH).click()
    page.wait_for_selector(INPUT_SEARCH, timeout=30000)
    safe_fill(page, INPUT_SEARCH, user_id)
    page.wait_for_timeout(2000) 
    page.locator(INPUT_SEARCH).press('Enter')
    page.wait_for_timeout(2000) 
    page.locator(USER_NAME_CELL).first.click()
    page.wait_for_timeout(2000)
    return True


def extract_page_user_info(page):
    """페이지에서 사용자 정보를 추출한다."""
    # 관리 버튼 클릭하여 전체 정보 표시 (필요한 경우에만)
    manage_btn = page.locator(BTN_MANAGE)
    fm_members = page.locator(AREA_MEMBER_INFO)
    is_minimized = 'minimize' in fm_members.get_attribute('class') if fm_members.count() > 0 else False
    
    if manage_btn.count() > 0 and is_minimized:
        manage_btn.click()
        page.wait_for_timeout(2000)
    
    page_info = {}
    
    # 기본 이름 정보 추출
    name_elem = page.locator(TEXT_NAME)
    if name_elem.count() > 0:
        full_name = name_elem.text_content().strip()
        if '_ ' in full_name:
            name_parts = full_name.split('_ ', 1)
            page_info['last_name'] = name_parts[0] + '_'
            page_info['first_name'] = name_parts[1]
        else:
            name_parts = full_name.split(' ', 1)
            if len(name_parts) >= 2:
                page_info['last_name'] = name_parts[0]
                page_info['first_name'] = name_parts[1]
    
    # 닉네임
    nickname_elem = page.locator(TEXT_NICKNAME)
    if nickname_elem.count() > 0:
        page_info['nickname'] = nickname_elem.text_content().strip()
    
    # 이메일 (ID)
    email_elem = page.locator(TEXT_EMAIL)
    if email_elem.count() > 0:
        page_info['email'] = email_elem.text_content().strip()
    
    # 다국어명 정보 - 페이지의 실제 값을 그대로 저장
    page_info['multilingual'] = {}
    lang_names = page.locator(TEXT_LANG_NAMES)
    lang_count = lang_names.count()
    
    zh_count = 0  # 중국어 카운터
    for i in range(lang_count):
        lang_elem = lang_names.nth(i)
        lang_attr = lang_elem.get_attribute('lang')
        lang_text = lang_elem.text_content().strip()
        
        if lang_attr and lang_text:
            # 중국어의 경우 순서에 따라 구분
            if lang_attr == 'zh':
                if zh_count == 0:
                    key = 'zh_CN'  # 첫 번째 zh는 간체
                else:
                    key = 'zh_TW'  # 두 번째 zh는 번체
                zh_count += 1
            else:
                key = lang_attr
            
            # 페이지의 실제 텍스트를 그대로 저장
            page_info['multilingual'][key] = lang_text
    
    # 필드별 정보 추출
    field_mapping = {
        '사용자 유형': 'user_type',
        '직급': 'position',
        '사내 번호': 'internal_number',
        '휴대폰': 'phone_number',
        '보조 이메일': 'sub_email',
        '개인 이메일': 'private_email',
        '근무처': 'workplace',
        '담당 업무': 'task',
        '생일': 'birthday',
        '입사일': 'hired_date',
        '사원 번호': 'employee_number'
    }
    
    for field_name, key in field_mapping.items():
        if key == 'phone_number':
            # 휴대폰 전용 로직
            phone_elem = page.locator(PHONE_SELECTOR)
            
            if phone_elem.count() > 0:
                value = phone_elem.first.text_content().strip()
                if value.startswith('+82 '):
                    value = value[4:]
                if value:
                    page_info[key] = value
            else:
                # 대안 셀렉터들 시도
                for alt_selector in PHONE_ALT_SELECTORS:
                    alt_elem = page.locator(alt_selector)
                    if alt_elem.count() > 0:
                        value = alt_elem.first.text_content().strip()
                        if value.startswith('+82 '):
                            value = value[4:]
                        if value:
                            page_info[key] = value
                            break
        
        elif key == 'sub_email':
            # 보조 이메일 전용 로직
            for sub_email_selector in SUB_EMAIL_SELECTORS:
                sub_email_elem = page.locator(sub_email_selector)
                if sub_email_elem.count() > 0:
                    value = sub_email_elem.first.text_content().strip()
                    if value:
                        page_info[key] = value
                        break
        
        elif key == 'private_email':
            # 개인 이메일 전용 로직
            for private_email_selector in PRIVATE_EMAIL_SELECTORS:
                private_email_elem = page.locator(private_email_selector)
                if private_email_elem.count() > 0:
                    value = private_email_elem.first.text_content().strip()
                    if value:
                        page_info[key] = value
                        break
        
        else:
            # 일반 필드들
            general_selectors = [selector.format(field_name=field_name) for selector in FIELD_GENERAL_SELECTORS_TEMPLATE]
            
            for general_selector in general_selectors:
                general_elem = page.locator(general_selector)
                if general_elem.count() > 0:
                    value = general_elem.first.text_content().strip()
                    if value:
                        page_info[key] = value
                        break
    
    return page_info


def get_display_width(text):
    """텍스트의 실제 표시 너비를 계산한다 (한글 등은 2칸)."""
    width = 0
    for char in str(text):
        if ord(char) > 127:  # 비ASCII 문자 (한글, 중국어, 일본어 등)
            width += 2
        else:
            width += 1
    return width


def print_comparison_table(comparisons):
    """비교 결과를 박스 스타일 표로 깔끔하게 출력한다."""
    # 각 컬럼의 최대 너비 계산
    max_field_width = max(get_display_width(comp['field']) for comp in comparisons)
    max_input_width = max(get_display_width(comp['input']) for comp in comparisons)
    max_page_width = max(get_display_width(comp['page']) for comp in comparisons)
    
    # 최소 너비 보장 및 최대 너비 제한
    field_width = max(max_field_width, 8)
    input_width = min(max(max_input_width, 12), 30)
    page_width = min(max(max_page_width, 12), 30)
    result_width = 6
    
    total_width = field_width + input_width + page_width + result_width + 7  # 경계선 포함
    
    def pad_text(text, target_width):
        """텍스트를 목표 너비에 맞게 패딩한다."""
        display_width = get_display_width(text)
        if display_width > target_width - 2:
            # 너무 길면 자르고 .. 추가
            truncated = ""
            current_width = 0
            for char in str(text):
                char_width = 2 if ord(char) > 127 else 1
                if current_width + char_width > target_width - 4:
                    break
                truncated += char
                current_width += char_width
            text = truncated + ".."
            display_width = get_display_width(text)
        
        padding = target_width - display_width
        return text + " " * padding
    
    # 타이틀 텍스트와 길이 계산
    title_text = "📋 구성원 정보 비교"
    title_display_width = get_display_width(title_text)
    title_padding = max((total_width - title_display_width) // 2, 1)
    title_right_padding = total_width - title_display_width - title_padding
    
    print("\n┌" + "─" * total_width + "┐")
    print("│" + " " * title_padding + title_text + " " * title_right_padding + "│")
    print("├" + "─" * field_width + "┬" + "─" * input_width + "┬" + "─" * page_width + "┬" + "─" * result_width + "┤")
    
    # 헤더 출력
    header_field = pad_text("항목", field_width)
    header_input = pad_text("입력값", input_width) 
    header_page = pad_text("페이지값", page_width)
    header_result = pad_text("결과", result_width)
    print(f"│{header_field}│{header_input}│{header_page}│{header_result}│")
    print("├" + "─" * field_width + "┼" + "─" * input_width + "┼" + "─" * page_width + "┼" + "─" * result_width + "┤")
    
    # 데이터 출력
    all_match = True
    for comparison in comparisons:
        field_text = pad_text(comparison['field'], field_width)
        input_text = pad_text(comparison['input'], input_width)
        page_text = pad_text(comparison['page'], page_width)
        result_icon = "✅" if comparison['match'] else "❌"
        result_text = pad_text(result_icon, result_width)
        
        print(f"│{field_text}│{input_text}│{page_text}│{result_text}│")
        
        if not comparison['match']:
            all_match = False
    
    print("└" + "─" * field_width + "┴" + "─" * input_width + "┴" + "─" * page_width + "┴" + "─" * result_width + "┘")
    
    # 결과 요약
    if all_match:
        print("\n🎉 결과: 모든 정보가 일치합니다!")
    else:
        print("\n⚠️  결과: 일부 정보가 일치하지 않습니다.")
    print()


def compare_user_info(user_info, page_info):
    """user_info와 페이지에서 추출한 정보를 비교한다."""
    if not user_info or not page_info:
        print("❌ 비교할 정보가 없습니다.")
        return False
    
    comparisons = []
    basic_fields = user_info.get('basic_fields', {})
    
    # 기본 필드 비교
    basic_comparisons = [
        ('성', basic_fields.get('last_name'), page_info.get('last_name')),
        ('이름', basic_fields.get('first_name'), page_info.get('first_name')),
        ('닉네임', basic_fields.get('nickname'), page_info.get('nickname')),
        ('사내번호', basic_fields.get('internal_number'), page_info.get('internal_number')),
        ('전화번호', basic_fields.get('phone_number'), page_info.get('phone_number')),
        ('근무처', basic_fields.get('workplace'), page_info.get('workplace')),
        ('담당업무', basic_fields.get('task'), page_info.get('task')),
        ('사원번호', basic_fields.get('employee_number'), page_info.get('employee_number'))
    ]
    
    for field_name, input_val, page_val in basic_comparisons:
        match = input_val == page_val
        comparisons.append({
            'field': field_name,
            'input': input_val or '없음',
            'page': page_val or '없음',
            'match': match
        })
    
    # 생일 비교 (포맷 차이 고려)
    input_birthday = basic_fields.get('birthday', '').replace(' ', '')
    page_birthday = page_info.get('birthday', '')
    birthday_match = input_birthday == page_birthday
    comparisons.append({
        'field': '생일',
        'input': basic_fields.get('birthday', '없음'),
        'page': page_birthday or '없음',
        'match': birthday_match
    })
    
    # 다국어명 비교 - 페이지의 실제 값과 입력값을 연결해서 비교
    multilingual_fields = user_info.get('multilingual_fields', {})
    page_multilingual = page_info.get('multilingual', {})
    
    # 페이지에서 찾은 모든 다국어를 기준으로 비교
    lang_page_mapping = {
        'en': ('영어명', 'english_last', 'english_first'),
        'ko': ('한국어명', 'korean_last', 'korean_first'),
        'ja': ('일본어명', 'japanese_last', 'japanese_first'),
        'zh_TW': ('번체중국어명', 'traditional_chinese_last', 'traditional_chinese_first'),
        'zh_CN': ('간체중국어명', 'simplified_chinese_last', 'simplified_chinese_first')
    }
    
    for page_lang_key, page_lang_text in page_multilingual.items():
        if page_lang_key in lang_page_mapping:
            lang_name, last_key, first_key = lang_page_mapping[page_lang_key]
            
            # 페이지 값 (실제 값)
            page_name = page_lang_text
            
            # 입력 값을 연결해서 생성
            input_last = multilingual_fields.get(last_key, '')
            input_first = multilingual_fields.get(first_key, '')
            
            if input_last and input_first:
                # 영어는 공백을 포함하여 연결, 다른 언어는 공백 없이 연결
                if page_lang_key == 'en':
                    input_combined = f"{input_last} {input_first}"  # 영어: 공백 포함
                    input_display = f"{input_last} {input_first}"
                else:
                    input_combined = input_last + input_first  # 다른 언어: 공백 없음
                    input_display = f"{input_last} {input_first}"
                
                match = input_combined == page_name
            else:
                match = False
                input_display = '없음'
            
            comparisons.append({
                'field': lang_name,
                'input': input_display,
                'page': page_name,
                'match': match
            })
    
    # 이메일 관련 비교
    email_fields = user_info.get('email_fields', {})
    
    # 보조 이메일 비교 (부분 비교)
    input_sub_email = email_fields.get('sub_email')
    page_sub_email = page_info.get('sub_email')
    sub_email_match = input_sub_email and page_sub_email and input_sub_email in page_sub_email
    
    comparisons.append({
        'field': '보조이메일',
        'input': input_sub_email or '없음',
        'page': page_sub_email or '없음',
        'match': sub_email_match
    })
    
    # 개인 이메일 비교 (부분 비교)
    input_private_email = email_fields.get('private_email')
    page_private_email = page_info.get('private_email')
    private_email_match = input_private_email and page_private_email and input_private_email in page_private_email
    
    comparisons.append({
        'field': '개인이메일',
        'input': input_private_email or '없음',
        'page': page_private_email or '없음',
        'match': private_email_match
    })
    
    # 결과 테이블 출력
    print_comparison_table(comparisons)
    
    # 전체 일치 여부 반환
    return all(comp['match'] for comp in comparisons)


def validate_user_info(page, app_state=None):
    """사용자 정보를 검증하는 함수"""
    if not app_state or not hasattr(app_state, 'user_info') or not app_state.user_info:
        print("❌ user_info가 없습니다.")
        return False
    
    # 페이지에서 정보 추출
    page_info = extract_page_user_info(page)
    
    # 정보 비교
    return compare_user_info(app_state.user_info, page_info)


# =====================
# 메인 플로우 함수
# =====================
def retrieve_user(page, app_state=None):
    """구성원 정보 조회 플로우를 순차적으로 실행"""
    print("\n구성원 조회 자동화 시작")
    user_id = app_state.global_user_id if app_state and hasattr(app_state, 'global_user_id') else None
    if not user_id:
        raise ValueError("app_state.global_user_id가 필요합니다.")
    
    if not access_user_detail(page, user_id):
        print("구성원 조회 자동화 실패 - access_user_detail\n")
        return False
    
    # 사용자 정보 검증 실행
    result = validate_user_info(page, app_state)
    if result:
        print("구성원 조회 자동화 완료\n")
    else:
        print("구성원 조회 자동화 실패 - validate_user_info\n")
    return result
    
