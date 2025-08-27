# 📋 Basic Test Automation

## 🏗️ 파일 구조

```
basic_test_automation/
├── automation/                
│   ├── config/                # 설정 관련
│   │   ├── settings.py        # 환경별 URL/계정 설정
│   ├── core/                  # 핵심 유틸리티
│   │   ├── auth.py           # 로그인 처리
│   │   └── safe_fill.py      # 안전한 입력 처리
│   ├── modules/              # 기능별 자동화 코드 
│   │   ├── contact/          # 외부 연락처
│   │   ├── group/            # 그룹 
│   │   ├── level/            # 직급 
│   │   ├── orgunit/          # 조직 
│   │   ├── position/         # 직책 
│   │   ├── status/           # 상태 
│   │   ├── user/             # 구성원
│   │   └── usertype/         # 사용자 유형
│   └── pages/                # 페이지 객체 모델
│       ├── contact_page.py
│       ├── group_page.py
│       ├── orgunit_page.py
│       └── user_page.py
├── tests/                   # 테스트 케이스
│   ├── conftest.py          # pytest 설정 및 픽스처
│   ├── test_contact.py      # 연락처 테스트
│   ├── test_group.py        # 그룹 테스트
│   ├── test_level.py        # 직급 테스트
│   ├── test_orgunit.py      # 조직 테스트
│   ├── test_position.py     # 직책 테스트
│   ├── test_status.py       # 상태 테스트
│   ├── test_user.py         # 구성원 테스트
│   └── test_usertype.py     # 사용자 유형 테스트
├── docker-compose.yml        # Docker 컨테이너 설정
├── Dockerfile               # Docker 이미지 설정
├── pytest.ini              # pytest 설정
└── requirements.txt         # Python 의존성
```

## 🎨 작성 패턴

#### 1. 자동화 함수
```python
def some_function():
    """각 단계별 함수는 성공 시 True를 반환한다."""
    ...
    자동화 코드 1...
    자동화 코드 2...
    ...
    return True
```

#### 2. 메인 플로우 함수 
```python
def main_flow_function(page, app_state=None):
    """메인 플로우 함수에서는 각 단계를 순차대로 호출만 한다."""
    if not step_1(page):
        return False  # False가 있으면 진행하지 않고 테스트 중지
    if not step_2(page):
        return False
    if not step_3(page, app_state):
        return False
    return True
```

### 🔄 상태 관리 (AppState)
```python
# conftest.py의 AppState 클래스
class AppState:
    def __init__(self):
        self.global_user_id = None      # 생성된 사용자 ID
        self.contact_name = None        # 생성된 연락처 이름
        self.group_name = None          # 생성된 그룹 이름
        # ... 기타 상태 정보
```

- 생성 단계에서 `app_state`에 정보를 저장
- 수정/삭제 단계에서 저장된 정보를 활용하여 대상을 찾음

## ⚙️ 자동화 수행 계정 조건

### 📋 
1. **관리자 권한**: 부관리자 권한 이상 (일부 기능 접근 불가할 수 있음)
2. **사용 언어**: 한국어로 설정 (요소 선택 시 한국어 기준으로 접근 중)
3. **외부 대화 권한**: ON 상태로 설정 (OFF인 경우, 외부연락처 자동화에 문제 발생 가능성 있음)