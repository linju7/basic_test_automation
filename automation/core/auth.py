"""
로그인 기능
"""
from playwright.sync_api import Page
from automation.config.settings import settings


class AuthManager:
    """로그인 클래스"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def input_id(self, username):
          self.page.goto(settings.get_base_url())
          self.page.fill("input[id='user_id']", username)
          self.page.click("button[class='btn_submit']")
          self.page.wait_for_load_state("networkidle")

    def input_password(self, password):
        self.page.fill("input[id='user_pwd']", password)
        self.page.click("button[class='btn_submit']")
        self.page.wait_for_load_state("networkidle")

    def login(self):
        username = settings.get_account("id")
        password = settings.get_account("password")
        self.input_id(username)
        self.input_password(password)
