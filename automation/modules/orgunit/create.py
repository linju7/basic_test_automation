from automation.config.settings import settings
from datetime import datetime
from automation.core.safe_fill import safe_fill

# =====================
# 셀렉터 상수 (OrgUnit Create Page)
# =====================
BTN_ORG_ADD = 'button.btn_save:text-is("조직 추가")'
LAYER_ORG_ADD = 'div.ly_member_add h3.tit:text("조직 추가")'
INPUT_ORG_NAME = 'input.lw_input[placeholder="조직명"]'
INPUT_ENGLISH = 'input.lw_input[placeholder="English"]'
INPUT_KOREAN = 'input.lw_input[placeholder="Korean"]'
INPUT_CHINESE_TWN = 'input.lw_input[placeholder="Chinese (TWN)"]'
INPUT_JAPANESE = 'input.lw_input[placeholder="Japanese"]'
INPUT_CHINESE_CHN = 'input.lw_input[placeholder="Chinese (CHN)"]'
INPUT_DESCRIPTION = 'input.lw_input[placeholder="설명"]'
BTN_ADD = 'div.ly_member_add button.lw_btn_point:text-is("추가")'



def open_org_add_layer(page):
    """조직 추가 레이어 열기"""
    page.wait_for_selector(BTN_ORG_ADD, timeout=5000)
    page.locator(BTN_ORG_ADD).click()
    page.wait_for_selector(LAYER_ORG_ADD, timeout=5000)
    return True

def fill_org_info(page, app_state=None):
    """조직 정보 입력 폼을 채우기"""
    # 유니크한 값 세팅을 위해 현재 시간값 사용
    timestamp = datetime.now().strftime("%m%d%H%M")
    org_name = f"자동화조직_{timestamp}"
    
    safe_fill(page, INPUT_ORG_NAME, org_name)
    if app_state is not None:
        app_state.org_name = org_name
    
    # 다국어 필드 입력
    safe_fill(page, INPUT_ENGLISH, "AutoOrg_EN")
    safe_fill(page, INPUT_KOREAN, "자동화조직_KR")
    safe_fill(page, INPUT_CHINESE_TWN, "自動組織_TWN")
    safe_fill(page, INPUT_JAPANESE, "自動組織_JP")
    safe_fill(page, INPUT_CHINESE_CHN, "自动组织_CHN")
    safe_fill(page, INPUT_DESCRIPTION, "자동화로 생성된 조직입니다.")
    
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
def create_orgunit(page, app_state=None):
    """조직 추가 플로우를 순차적으로 실행"""
    print("\n조직 추가 자동화 시작")
    page.goto(settings.ORG_URLS[settings.ENVIRONMENT])
    if not open_org_add_layer(page):
        print("조직 추가 자동화 실패 - open_org_add_layer\n")
        return False
    if not fill_org_info(page, app_state):
        print("조직 추가 자동화 실패 - fill_org_info\n")
        return False
    if not click_add_button(page):
        print("조직 추가 자동화 실패 - click_add_button\n")
        return False
    print("조직 추가 자동화 완료\n")
    return True
