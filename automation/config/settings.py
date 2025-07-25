"""
Works Mobile 자동화 설정
"""
import os


class Settings:
    """설정 클래스"""
    
    # 현재 환경 설정
    ENVIRONMENT = os.getenv("TEST_ENV", "alpha")
    
    # 환경별 기본 URL
    BASE_URLS = {
        "alpha": "https://alpha-contact.worksmobile.com",
        "stage": "https://stage.contact.worksmobile.com",
        "real": "https://contact.worksmobile.com"
    }
    
    # 환경별 구성원 페이지 URL
    USERS_URLS = {
        "alpha": "https://alpha-admin.worksmobile.com/member/users",
        "stage": "https://stage-admin.worksmobile.com/member/users", 
        "real": "https://admin.worksmobile.com/member/users"
    }
    
    @classmethod
    def get_base_url(cls) -> str:
        return cls.BASE_URLS[cls.ENVIRONMENT]
    
    @classmethod
    def get_users_url(cls) -> str:
        return cls.USERS_URLS[cls.ENVIRONMENT]
    
    @classmethod
    def get_account(cls, account_type: str) -> str:
        value = os.getenv(account_type.upper())
        if not value:
            raise ValueError(f"Environment variable {account_type.upper()} not found")
        return value


# 전역 설정 인스턴스
settings = Settings()