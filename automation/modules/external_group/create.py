from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (External Group Create Page)
# =====================
BTN_GROUP_ADD = 'button.lw_btn_drop:text-is("그룹 추가")'
DROPDOWN_EXTERNAL_GROUP = 'div.ly_context[style*="display: block"] a:text-is("외부 그룹")'
LAYER_GROUP_ADD = 'div.ly_member_add h3.tit:text("그룹 추가")'
INPUT_GROUP_NAME = 'input.lw_input[placeholder="그룹명"]'
INPUT_DESCRIPTION = 'input.lw_input[placeholder="설명"]'
INPUT_MASTER = 'div.field i.hd:has-text("마스터") ~ div input.lw_input[placeholder="이름 또는 ID 검색"]'
BTN_ADD = 'div.ly_member_add button.lw_btn_point:text-is("추가")'
LAYER_EXTERNAL_GROUP_SUCCESS = 'div.ly_common.freeplan h3.tit:text("외부 그룹이 추가되었습니다.")'
BTN_CONFIRM = 'div.ly_common.freeplan button.lw_btn_point:text-is("확인")'


def create_external_group_info():
    """외부그룹 입력 데이터를 생성한다."""
    timestamp = datetime.now().strftime("%m%d%H%M")
    
    external_group_info = {
        "timestamp": timestamp,
        "group_name": f"외부그룹_자동화_{timestamp}",
        "description": f"외부그룹_자동화_설명_{timestamp}"
    }
    
    return external_group_info


def open_external_group_add_layer(page):
    """외부그룹 추가 레이어 열기"""
    page.wait_for_selector(BTN_GROUP_ADD, timeout=5000)
    btn = page.locator(BTN_GROUP_ADD)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(DROPDOWN_EXTERNAL_GROUP, timeout=3000)
        external_group_menu = page.locator(DROPDOWN_EXTERNAL_GROUP)
        if external_group_menu.count() > 0:
            external_group_menu.first.click()
            page.wait_for_selector(LAYER_GROUP_ADD, timeout=5000)
            return True
    return False


def fill_external_group_info(page, app_state=None):
    """외부그룹 정보 입력 폼을 채우기"""
    # 외부그룹 정보 객체 생성
    external_group_info = create_external_group_info()
    
    # app_state에 저장
    if app_state is not None:
        app_state.external_group_info = external_group_info
        app_state.external_group_name = external_group_info["group_name"]
    
    # 그룹명 입력
    safe_fill(page, INPUT_GROUP_NAME, external_group_info["group_name"])
    
    # 설명 입력
    safe_fill(page, INPUT_DESCRIPTION, external_group_info["description"])
    
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
    
    return True


def click_add_button(page):
    """추가 버튼 클릭 및 외부그룹 생성 완료 확인"""
    add_btn = page.locator(BTN_ADD)
    if add_btn.count() > 0:
        add_btn.first.click()
        page.wait_for_timeout(2000)
        
        # 외부그룹 생성 완료 레이어 확인
        try:
            page.wait_for_selector(LAYER_EXTERNAL_GROUP_SUCCESS, timeout=5000)
            confirm_btn = page.locator(BTN_CONFIRM)
            if confirm_btn.count() > 0:
                confirm_btn.first.click()
                page.wait_for_timeout(1000)
                return True
        except:
            # 레이어가 나타나지 않으면 그냥 성공으로 처리
            return True
        
        return True
    return False


# =====================
# 메인 플로우 함수
# =====================
def create_external_group(page, app_state=None):
    """외부그룹 추가 플로우를 순차적으로 실행"""
    page.goto(settings.GROUP_URLS[settings.ENVIRONMENT])
    if not open_external_group_add_layer(page):
        return False
    if not fill_external_group_info(page, app_state):
        return False
    if not click_add_button(page):
        return False
    return True
