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
    
    
    # 서비스에 표시될 때는 다국어로 표시되므로, 한국어명 저장 
    value = f"자동화조직_KR_{timestamp}"
    if app_state is not None:
        app_state.org_name = value

    # 다국어 필드 입력
    safe_fill(page, INPUT_ENGLISH, f"AutoOrg_EN_{timestamp}")
    safe_fill(page, INPUT_KOREAN, value)
    safe_fill(page, INPUT_CHINESE_TWN, f"自動組織_TWN_{timestamp}")
    safe_fill(page, INPUT_JAPANESE, f"自動組織_JP_{timestamp}")
    safe_fill(page, INPUT_CHINESE_CHN, f"自动组织_CHN_{timestamp}")
    safe_fill(page, INPUT_DESCRIPTION, f"자동화로 생성된 조직입니다.{timestamp}")
    
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
