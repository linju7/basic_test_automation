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
        if account_type == "id":
            # 환경별로 REAL_ID, STAGE_ID, ALPHA_ID 등에서 불러옴
            env_key = f"{cls.ENVIRONMENT.upper()}_ID"
        elif account_type == "password":
            # 모든 환경에서 PASSWORD로 고정
            env_key = "PASSWORD"
        else:
            raise ValueError("account_type은 'id' 또는 'password'만 허용됩니다.")
        value = os.getenv(env_key)
        if not value:
            raise ValueError(f"환경변수 {env_key}가 설정되어 있지 않습니다")
        return value


# 전역 설정 인스턴스
settings = Settings()