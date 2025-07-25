"""
로그인 기능
"""
from playwright.sync_api import Page
from automation.config.settings import settings


class AuthManager:
    """로그인 클래스"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def login(self):
        """Works Mobile 로그인"""
        # 기본 URL로 이동
        self.page.goto(settings.get_base_url())
        
        # 환경변수에서 계정 정보 가져오기
        username = settings.get_account("id")
        password = settings.get_account("password")
        
        # 로그인 폼 입력
        self.page.fill("input[id='user_id']", username)
        
        # 로그인 버튼 클릭
        self.page.click("button[class='btn_submit']")
        
        # 로그인 완료 대기
        self.page.wait_for_load_state("networkidle")
