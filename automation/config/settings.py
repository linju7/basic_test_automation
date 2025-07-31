"""
Works Mobile 자동화 설정
"""
import os

class Settings:
    """환경별 URL 및 계정 정보를 관리하는 설정 클래스"""

    ENVIRONMENT = os.getenv("TEST_ENV", "real")
    BASE_URLS = {
        "alpha": "https://alpha-contact.worksmobile.com",
        "stage": "https://stage.contact.worksmobile.com",
        "real": "https://contact.worksmobile.com"
    }
    USERS_URLS = {
        "alpha": "https://alpha-admin.worksmobile.com/member/users",
        "stage": "https://stage-admin.worksmobile.com/member/users",
        "real": "https://admin.worksmobile.com/member/users"
    }

    GROUP_URLS = {
        "alpha": "https://alpha-admin.worksmobile.com/member/groups",
        "stage": "https://stage-admin.worksmobile.com/member/groups",
        "real": "https://admin.worksmobile.com/member/groups"
    }

    ORG_URLS = {
        "alpha": "https://alpha-admin.worksmobile.com/member/org-units",
        "stage": "https://stage-admin.worksmobile.com/member/org-units",
        "real" : "https://admin.worksmobile.com/member/org-units"
    }

    CONTACT_URLS = {
        "alpha": "https://alpha-contact.worksmobile.com/v2/p/shared/contact",
        "stage": "https://stage.contact.worksmobile.com/v2/p/shared/contact",
        "real" : "https://contact.worksmobile.com/v2/p/shared/contact"
    }

    POSITION_URLS = {
        "alpha": "https://alpha-admin.worksmobile.com/member/job/positions",
        "stage": "https://stage-admin.worksmobile.com/member/job/positions",
        "real" : "https://admin.worksmobile.com/member/job/positions"
    }

    LEVEL_URLS = {
        "alpha": "https://alpha-admin.worksmobile.com/member/job/levels",
        "stage": "https://stage-admin.worksmobile.com/member/job/levels",
        "real" : "https://admin.worksmobile.com/member/job/levels"
    }

    USERTYPE_URLS = {
        "alpha": "https://alpha-admin.worksmobile.com/member/job/user-types",
        "stage": "https://stage-admin.worksmobile.com/member/job/user-types",
        "real" : "https://admin.worksmobile.com/member/job/user-types"
    }

    STATUS_URLS = {
        "alpha": "https://alpha-admin.worksmobile.com/member/status",
        "stage": "https://stage-admin.worksmobile.com/member/status",
        "real" : "https://admin.worksmobile.com/member/status"
    }

    @classmethod
    def get_base_url(cls) -> str:
        """현재 환경에 맞는 기본 URL 반환"""
        return cls.BASE_URLS[cls.ENVIRONMENT]

    @classmethod
    def get_users_url(cls) -> str:
        """현재 환경에 맞는 구성원 페이지 URL 반환"""
        return cls.USERS_URLS[cls.ENVIRONMENT]

    @classmethod
    def get_account(cls, account_type: str) -> str:
        """환경 변수에서 계정 정보(id, password) 반환"""
        if account_type == "id":
            env_key = f"{cls.ENVIRONMENT.upper()}_ID"
        elif account_type == "password":
            env_key = "PASSWORD"
        else:
            raise ValueError("account_type은 'id' 또는 'password'만 허용됩니다.")
        value = os.getenv(env_key)
        if not value:
            raise ValueError(f"필수 환경변수 '{env_key}'가 설정되어 있지 않습니다.")
        return value

settings = Settings()