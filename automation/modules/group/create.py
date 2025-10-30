from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (Group Create Page)
# =====================
BTN_GROUP_ADD = 'button.lw_btn_drop:text-is("그룹 추가")'
DROPDOWN_GROUP = 'div.ly_context[style*="display: block"] a:text-is("그룹")'
LAYER_GROUP_ADD = 'div.ly_member_add h3.tit:text("그룹 추가")'
INPUT_GROUP_NAME = 'input.lw_input[placeholder="그룹명"]'
INPUT_DESCRIPTION = 'input.lw_input[placeholder="설명"]'
INPUT_MASTER = 'div.field i.hd:has-text("마스터") ~ div input.lw_input[placeholder="이름 또는 ID 검색"]'
INPUT_MAILING_LIST = 'input.lw_input.w_limit[placeholder="ID"]'
BTN_ADD = 'div.ly_member_add button.lw_btn_point:text-is("추가")'


def create_group_info():
    """그룹 입력 데이터를 생성한다."""
    timestamp = datetime.now().strftime("%m%d%H%M")
    
    group_info = {
        "timestamp": timestamp,
        "group_name": f"자동화_{timestamp}",
        "description": f"자동화_설명_{timestamp}",
        "mailing_id": f"dl_{timestamp}"
    }
    
    return group_info


def open_group_add_layer(page):
    """그룹 추가 레이어 열기"""
    page.wait_for_selector(BTN_GROUP_ADD, timeout=5000)
    btn = page.locator(BTN_GROUP_ADD)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(DROPDOWN_GROUP, timeout=3000)
        group_menu = page.locator(DROPDOWN_GROUP)
        if group_menu.count() > 0:
            group_menu.first.click()
            page.wait_for_selector(LAYER_GROUP_ADD, timeout=5000)
            return True
    return False


def fill_group_info(page, app_state=None):
    """그룹 정보 입력 폼을 채우기"""
    # 그룹 정보 객체 생성
    group_info = create_group_info()
    
    # app_state에 저장
    if app_state is not None:
        app_state.group_info = group_info
        app_state.group_name = group_info["group_name"]
    
    # 그룹명 입력
    safe_fill(page, INPUT_GROUP_NAME, group_info["group_name"])
    
    # 설명 입력
    safe_fill(page, INPUT_DESCRIPTION, group_info["description"])
    
    # 마스터 입력
    if app_state and hasattr(app_state, 'global_user_id') and app_state.global_user_id:
        master_id = app_state.global_user_id
    else:
        master_id = "automation" + settings.get_account('domain')
    
    master_input = page.locator(INPUT_MASTER)
    if master_input.count() > 0:
        safe_fill(page, INPUT_MASTER, master_id)
        page.wait_for_timeout(2000)
        master_input.press('Enter')
        page.wait_for_timeout(1000)
    
    # 메일링 리스트 ID 입력
    input_box = page.locator(INPUT_MAILING_LIST)
    if input_box.count() > 0:
        safe_fill(page, INPUT_MAILING_LIST, '')
        safe_fill(page, INPUT_MAILING_LIST, group_info["mailing_id"])
    
    return True


def click_add_button(page):
    """추가 버튼 클릭"""
    add_btn = page.locator(BTN_ADD)
    if add_btn.count() > 0:
        add_btn.first.click()
        page.wait_for_timeout(2000)
        return True
    return False


# =====================
# 메인 플로우 함수
# =====================
def create_group(page, app_state=None):
    """그룹 추가 플로우를 순차적으로 실행"""
    print("\n그룹 추가 자동화 시작")
    page.goto(settings.GROUP_URLS[settings.ENVIRONMENT])
    if not open_group_add_layer(page):
        print("그룹 추가 자동화 실패 - open_group_add_layer\n")
        return False
    if not fill_group_info(page, app_state):
        print("그룹 추가 자동화 실패 - fill_group_info\n")
        return False
    if not click_add_button(page):
        print("그룹 추가 자동화 실패 - click_add_button\n")
        return False
    print("그룹 추가 자동화 완료\n")
    return True
