from playwright.sync_api import Page
from automation.core.safe_fill import safe_fill
from automation.config.settings import settings

# =====================
# 셀렉터 상수 (Group Retrieve Page)
# =====================
BTN_SEARCH = 'button.btn_search'
INPUT_SEARCH = '#group_search_input'
GROUP_NAME_CELL = 'strong.ellipsis_element'


def access_group_detail(page: Page, group_name: str):
    """그룹 검색 후 상세 페이지로 진입"""
    page.goto(settings.GROUP_URLS[settings.ENVIRONMENT])
    page.wait_for_selector(BTN_SEARCH, timeout=10000)
    page.locator(BTN_SEARCH).click()
    page.wait_for_selector(INPUT_SEARCH, timeout=10000)
    safe_fill(page, INPUT_SEARCH, group_name)
    page.wait_for_timeout(2000)
    page.locator(INPUT_SEARCH).press('Enter')
    page.wait_for_timeout(2000)
    # 검색 결과에서 그룹명 클릭
    page.wait_for_selector(GROUP_NAME_CELL, timeout=10000)
    page.locator(GROUP_NAME_CELL).first.click()
    page.wait_for_timeout(3000)
    return True


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
    title_text = "📋 그룹 정보 비교"
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


def extract_page_group_info(page):
    """페이지에서 그룹 정보를 추출한다."""
    page_info = {}
    
    # 그룹명 추출 (두 가지 위치에서 시도)
    group_name_selectors = [
        '.detail_item:has(i.hd:text-is("그룹명")) strong',  # 상세 정보 영역
        '.name_box h4.name'  # 상단 이름 영역
    ]
    
    for selector in group_name_selectors:
        name_elem = page.locator(selector)
        if name_elem.count() > 0:
            group_name = name_elem.text_content().strip()
            # 페이지 값을 있는 그대로 저장 (수정됨 텍스트 포함)
            page_info['group_name'] = group_name
            break
    
    # 설명 추출
    description_elem = page.locator('.detail_item:has(i.hd:text-is("설명")) p')
    if description_elem.count() > 0:
        page_info['description'] = description_elem.text_content().strip()
    
    # 메일링리스트 추출
    mailing_elem = page.locator('.detail_item:has(i.hd:text-is("메일링리스트")) a')
    if mailing_elem.count() > 0:
        mailing_full = mailing_elem.text_content().strip()
        # "dl_08011601@jp2-adv01.wdomain3.com"에서 "dl_08011601" 부분 추출
        if '@' in mailing_full:
            mailing_id = mailing_full.split('@')[0]
            page_info['mailing_id'] = mailing_id
    
    return page_info


def compare_group_info(group_info, page_info):
    """group_info와 페이지에서 추출한 정보를 비교한다."""
    if not group_info or not page_info:
        print("❌ 비교할 정보가 없습니다.")
        return False
    
    comparisons = []
    
    # 그룹명 비교
    input_group_name = group_info.get('group_name', '')
    page_group_name = page_info.get('group_name', '')
    group_name_match = input_group_name == page_group_name
    
    comparisons.append({
        'field': '그룹명',
        'input': input_group_name or '없음',
        'page': page_group_name or '없음',
        'match': group_name_match
    })
    
    # 설명 비교
    input_description = group_info.get('description', '')
    page_description = page_info.get('description', '')
    description_match = input_description == page_description
    
    comparisons.append({
        'field': '설명',
        'input': input_description or '없음',
        'page': page_description or '없음',
        'match': description_match
    })
    
    # 메일링리스트 비교
    input_mailing_id = group_info.get('mailing_id', '')
    page_mailing_id = page_info.get('mailing_id', '')
    mailing_match = input_mailing_id == page_mailing_id
    
    comparisons.append({
        'field': '메일링리스트',
        'input': input_mailing_id or '없음',
        'page': page_mailing_id or '없음',
        'match': mailing_match
    })
    
    # 결과 테이블 출력
    print_comparison_table(comparisons)
    
    # 전체 일치 여부 반환
    return all(comp['match'] for comp in comparisons)


def validate_group_info(page, app_state=None):
    """그룹 정보를 검증하는 함수"""
    if not app_state or not hasattr(app_state, 'group_info') or not app_state.group_info:
        print("❌ group_info가 없습니다.")
        return False
    
    # 페이지에서 정보 추출
    page_info = extract_page_group_info(page)
    
    # 정보 비교
    return compare_group_info(app_state.group_info, page_info)


# =====================
# 메인 플로우 함수
# =====================
def retrieve_group(page, app_state=None):
    """그룹 정보 조회 플로우를 순차적으로 실행"""
    group_name = app_state.group_name if app_state and hasattr(app_state, 'group_name') else None
    if not group_name:
        raise ValueError("app_state.group_name이 필요합니다.")

    if not access_group_detail(page, group_name):
        return False
    
    if not validate_group_info(page, app_state):
        return False
    
    return True