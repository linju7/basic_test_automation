import pytest
from automation.core.auth import login

@pytest.fixture(scope="session")
def logged_in_page(browser):
    page = browser.new_page()
    login(page)
    yield page
    page.close()

class AppState:
    def __init__(self):
        self.global_user_id = None
        self.group_name = None
        self.org_name = None
        self.contact_name = None
        self.position_name = None
        self.level_name = None
        self.usertype_name = None
        self.status_name = None

        self.user_info = None
        self.group_info = None
        self.org_info = None
        self.contact_info = None
    

app_state = AppState()