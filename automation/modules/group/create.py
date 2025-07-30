from automation.config.settings import settings
from datetime import datetime

# 주요 셀렉터 상수
BTN_GROUP_ADD = 'button.lw_btn_drop:text-is("그룹 추가")'
DROPDOWN_GROUP = 'div.ly_context[style*="display: block"] a:text-is("그룹")'
LAYER_GROUP_ADD = 'div.ly_member_add h3.tit:text("그룹 추가")'
INPUT_GROUP_NAME = 'input.lw_input[placeholder="그룹명"]'
INPUT_MASTER = 'div.field i.hd:has-text("마스터") ~ div input.lw_input[placeholder="이름 또는 ID 검색"]'
BTN_ADD = 'div.ly_member_add button.lw_btn_point:text-is("추가")'


def open_group_add_dropdown(page):
    """그룹 추가 드롭다운 버튼을 클릭한다."""
    page.wait_for_selector(BTN_GROUP_ADD, timeout=5000)
    btn = page.locator(BTN_GROUP_ADD)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_selector(DROPDOWN_GROUP, timeout=3000)
        return True
    print("[실패] 그룹 추가 드롭다운 버튼을 찾을 수 없음")
    return False


def click_group_in_dropdown(page):
    """드롭다운에서 '그룹' 항목을 클릭한다."""
    group_menu = page.locator(DROPDOWN_GROUP)
    if group_menu.count() > 0:
        group_menu.first.click()
        return True
    print("[실패] 드롭다운에서 '그룹' 항목을 찾을 수 없음")
    return False


def wait_group_add_layer(page):
    """그룹 추가 레이어가 나타날 때까지 대기한다."""
    try:
        page.wait_for_selector(LAYER_GROUP_ADD, timeout=5000)
    except Exception:
        print("[실패] 그룹 추가 레이어가 뜨지 않음")
        raise


def fill_group_name(page, group_name):
    """그룹명 입력란에 값을 채운다."""
    input_box = page.locator(INPUT_GROUP_NAME)
    if input_box.count() > 0:
        input_box.fill(group_name)
        return True
    print("[실패] 그룹명 입력란을 찾을 수 없음")
    return False


def fill_master(page):
    """마스터 입력란에 계정 ID를 채운다."""
    master_id = settings.get_account('id')
    master_input = page.locator(INPUT_MASTER)
    if master_input.count() > 0:
        master_input.fill(master_id)
        page.wait_for_timeout(2000)
        master_input.press('Enter')
        page.wait_for_timeout(1000)
        return True
    print(f"[실패] 마스터 입력란을 찾을 수 없음 (master_id: {master_id})")
    return False


def click_add_button(page):
    """'추가' 버튼을 클릭한다."""
    add_btn = page.locator(BTN_ADD)
    if add_btn.count() > 0:
        add_btn.first.click()
        return True
    print("[실패] '추가' 버튼을 찾을 수 없음")
    return False


def create_group(page, app_state=None):
    """그룹 추가 플로우를 순차적으로 실행한다. 성공 시 True, 실패 시 False 반환."""
    page.goto(settings.GROUP_URLS[settings.ENVIRONMENT])
    if not open_group_add_dropdown(page):
        return False
    if not click_group_in_dropdown(page):
        return False
    try:
        wait_group_add_layer(page)
    except Exception:
        return False
    timestamp = datetime.now().strftime("%m%d%H%M")
    group_name = f"자동화_{timestamp}"
    if not fill_group_name(page, group_name):
        return False
    if not fill_master(page):
        return False
    if not click_add_button(page):
        return False
    return True
