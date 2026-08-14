# WeSeed CRM 데모체험 전환 분석 데이터 구축 PRD & 화면 고도화 프로젝트

> **개발 및 백엔드 연동 가이드**  
> 본 프로젝트는 **WeSeed CRM의 데모 체험 신청자 데이터를 체계적으로 수집하고, `demo_id`와 `company_id`(유료 회원사)간 전환 매칭 구조를 구축**하기 위한 프론트엔드 prototype 및 데이터 스펙 문서입니다.

---

## 📌 P0 데모 → 회원사 전환 구조 Specification

### 1. demo_id 생성 시점
- 사용자가 홈페이지의 **TO-BE 데모 신청 폼**을 제출하는 즉시 `demo_id` (예: `DEMO-2026-8942`)가 시스템에서 자동 생성됩니다.
- 데모 계정 발급 후 CRM 대시보드의 guest 프로필 메뉴에서 `demo_id`, 데모 계정, 만료일, 가입 상태를 조회합니다.

### 2. company_id 생성 시점
- 데모 CRM 우측 상단의 `[회원가입하기]` 클릭 후 **Step 03 회원사 정보 입력** 완료 시점에 `company_id` (예: `COMP-2026-9901`)가 생성됩니다.

### 3. 최종 전환 기준 (핵심 정의)
> **⚠️ 회원가입 완료 ≠ 최종 전환**
> 
> **✨ 회원가입 완료 + 결제 완료 = 최종 전환 (CONVERTED)**

- **회원가입만 완료하고 결제를 하지 않은 경우**:
  `payment_status = PENDING`, `conversion_status = PAYMENT_PENDING` (결제 대기)로 처리되며 최종 전환율 통계에 포함되지 않습니다.
- **결제가 완료된 시점**:
  `payment_status = PAID`, `conversion_status = CONVERTED` (전환 완료)로 최종 산출됩니다.

### 4. Funnel 상태값 정의표

| 상태 코드 (Dev Mode) | 사용자 노출 명칭 | 정의 및 세부 상태 설명 |
| :--- | :--- | :--- |
| `DEMO_ACTIVE` | 데모 이용 중 | 데모 체험계정이 활성화되어 CRM 사용 중인 상태 |
| `SIGNUP_STARTED` | 회원가입 진행 중 | 데모 CRM 내에서 회원가입 Wizard 02단계(휴대폰 인증) 이상 진입 |
| `SIGNUP_COMPLETED` | 회원가입 완료 | Step 03 회원사 정보 입력이 완료되어 `company_id` 생성됨 |
| `PAYMENT_PENDING` | 결제 대기 | 회원가입 완료 후 Step 04 결제 단계 미완료/이탈 상태 |
| `CONVERTED` | 전환 완료 | `company_id` 생성 + 결제 완료 (`PAID`) 시 최종 전환 |
| `DEMO_EXPIRED` | 데모 만료 | 14일 데모 기간 만료 |

---

## 🔗 데모 ↔ 회원사 연결 방식 및 매칭 규칙

1. **직접 회원가입 연결 (`DIRECT_SIGNUP`)**:
   - 데모 CRM 내부 4단계 Wizard를 통해 사용자가 직접 가입 및 결제 시 `demo_id`와 `company_id`가 자동 매칭됩니다.
2. **관리자 수동 연결 (`SYSADMIN_MANUAL`)**:
   - 기존 영업 절차를 통해 회원사가 생성된 경우, `SYSADMIN 데모체험관리` 상세 화면의 `[회원사 후보 찾기]` 모달을 통해 수동 매칭합니다.
   - **매칭 우선순위**:
     - 1순위: 이메일 + 휴대전화 모두 동일 (`EMAIL_AND_PHONE`)
     - 2순위: 이메일 동일 (`EMAIL`)
     - 3순위: 휴대전화 동일 (`PHONE`)
     - ※ 회사명 또는 담당자명 단독 매칭은 오매칭 방지를 위해 지원하지 않습니다.

---

## 🎯 P0 핵심 Activation 정의

데모 계정 사용자의 핵심 기능 경험도를 측정하기 위한 4대 Activation 로그:

1. `DEMO_LOGIN`: 데모 최초 로그인
2. `CUSTOMER_CREATE`: 고객/고객사 등록
3. `OPPORTUNITY_CREATE`: 영업기회 등록
4. `ACTIVITY_CREATE`: 영업활동 등록

각 이벤트는 `이벤트 코드`, `완료 여부`, `최초 발생일시`, `발생 횟수`를 로그 데이터로 관리 및 개발자 모드에서 실시간 조회 가능합니다.

---

## 🛠 SYSADMIN 화면 변경사항 및 양방향 조회

### 1. SYSADMIN 데모체험관리 (`viewSysDemo`)
- **상단 Segmented Control**: `[ AS-IS ] [ TO-BE ] [ 나란히 비교 ]` 지원 (기본값: TO-BE).
- **TO-BE 목록 컬럼**: `Demo ID` (파란색 Link), `서비스구분`, `회사명`, `예상인원`, `담당자명`, `전화번호`, `회사이메일`, `등록일`, `데모상태`, `전환상태` (Badge), `회원사ID` (파란색 Link).
- **상세 화면 (3개 섹션)**:
  - `Section 1. 기본 정보`: Demo ID (Read-only), 회사명, 담당자명, 이메일, 전화번호, 계정만료일 등 (`P0` Badge)
  - `Section 2. 데모 신청 정보`: 업종, 데모체험 목적, 관심 기능 Tag UI, 관리방식, 유입경로 등 (`NEW` Badge)
  - `Section 3. 회원사 전환 정보`: 전환상태, 회원가입일, 결제상태, 결제일, 회원사 ID, 전환경로 및 **Visual Relationship Diagram**
  - **수동 매칭 기능**: 미전환 데모에 대해 `[ 회원사 후보 찾기 ]` 팝업 제공.

### 2. SYSADMIN 회원사관리 (`viewSysCompany`)
- 회원사 상세 화면 결제정보 탭 내 **`데모체험 연동`** 섹션 추가.
- 표시 항목: `Demo ID` (파란색 Link), `데모 계정`, `전환 상태`, `데모 신청일`, `회원가입일`, `결제 완료일`.

### 3. 양방향 Drill-down
- 데모 상세의 `COMP-2026-9901` 클릭 → `SYSADMIN > 회원사관리`의 해당 회원사 상세로 즉시 이동.
- 회원사 상세의 `DEMO-2026-8942` 클릭 → `SYSADMIN > 데모체험관리`의 해당 데모 상세로 즉시 이동.

---

## 📋 신청 추가 필드 및 코드값 정의표

| 항목명 | 수집 방식 | 필수 여부 | DB 타입 / 코드값 |
| :--- | :--- | :--- | :--- |
| **예상 사용 인원** | 숫자 직접 입력 | 필수 | `INTEGER`, 1 이상 |
| **신청경로** | 단일 선택 (셀렉트) | 선택 | `GOOGLE_ADS`, `NAVER_SEARCH_ADS`, `WESEED_WEB`, `REFERRAL`, `SALES_GUIDE`, `ETC` |
| **업종** | 직접 텍스트 입력 | 선택 | `VARCHAR(100)` (예: IT/SaaS, 제조업, 유통 등) |
| **데모체험 목적** | 단일 선택 (라디오) | 선택 | `PURPOSE_EVALUATE` (실제 CRM 도입 검토)<br>`PURPOSE_CHECK_FEATURES` (기능 확인)<br>`PURPOSE_TEST_FIT` (사내 업무 적용 테스트)<br>`PURPOSE_COMPARE_CRM` (타 CRM과 비교)<br>`PURPOSE_ETC` (기타 + 직접 입력) |
| **관심 기능** | 다중 선택 (체크박스/최대 3개) | 선택 | `FEAT_CUSTOMER` (고객·고객사 관리)<br>`FEAT_OPPORTUNITY` (영업기회 관리)<br>`FEAT_ACTIVITY` (영업활동 관리)<br>`FEAT_SCHEDULE` (일정 관리)<br>`FEAT_QUOTE_CONTRACT` (견적·계약 관리)<br>`FEAT_REVENUE` (매출 관리)<br>`FEAT_ANALYTICS` (통계·분석)<br>`FEAT_ETC` (기타 + 직접 입력) |

---

## 🗄️ 백엔드 DB & API 데이터 스펙

### 1. `POST /api/v1/demo-requests` (JSON Payload 예시)

```json
{
  "company_name": "위시드 테크",
  "user_count": 20,
  "user_name": "김영업",
  "email": "lead@weseed.io",
  "phone": "010-1234-5678",
  "job_title": "영업 이사",
  "industry": "IT/SaaS 소프트웨어",
  "demo_purpose": "실제 CRM 도입을 검토하고 있어요",
  "interested_features": [
    "고객·고객사 관리",
    "영업기회 관리",
    "통계·분석"
  ],
  "application_source": "구글 광고",
  "privacy_agree": true,
  "system_metadata": {
    "created_at": "2026-08-12T11:45:00.000Z",
    "acquisition_channel": "검색 엔진 (SEO/SA)",
    "form_duration_sec": 42
  }
}
```

### 2. PostgreSQL DDL (`demo_requests`)

```sql
CREATE TABLE demo_requests (
    demo_id VARCHAR(50) PRIMARY KEY DEFAULT 'DEMO-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(CAST(FLOOR(RANDOM()*10000) AS TEXT), 4, '0'),
    company_name VARCHAR(100) NOT NULL,
    user_count INTEGER NOT NULL CHECK (user_count >= 1),
    user_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    job_title VARCHAR(50) NOT NULL,
    industry VARCHAR(100),
    demo_purpose VARCHAR(100),
    interested_features JSONB,
    application_source VARCHAR(50),
    privacy_agree BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    acquisition_channel VARCHAR(100),
    form_duration_sec INT DEFAULT 0,
    
    CONSTRAINT idx_demo_match_keys UNIQUE (email, phone)
);

CREATE INDEX idx_demo_created ON demo_requests (created_at DESC);
CREATE INDEX idx_demo_email ON demo_requests (email);
CREATE INDEX idx_demo_phone ON demo_requests (phone);
```

---

## 🚀 MVP 개발 우선순위

- **P0 (최우선)**: 전환 기준 정립, `demo_id` 연결 구조, **데모체험 CRM 내 직접 회원가입 & Pre-fill 데이터 연동**, 데모↔회원사 매칭, 신청 추가 필드, 핵심 Activation 수집, SYSADMIN 데모/회원사 관리 연동.
- **P1 (차순위)**: 신규 Event 로그, CS 정형 데이터, 실사용 비교 이벤트.
- **P2 (향후 고도화)**: 분석 대시보드 UI, AI 분석 엔진, 세그먼트 화면.


---

## 2026-08-14 P0 최종 확정안

- 데모 신청: **기존 문의폼 항목 유지** + `업종(input)`, `데모체험 목적(select/single)`, `관심 있는 기능(select/multi)`, `신청경로(select/single)` 추가.
- 데모 CRM: 무료체험 기간을 **상단 띠 배너**로 노출. `이용요금 확인`은 위시드 요금 페이지를 새 창으로 열고, `회원가입하기`는 회원가입 흐름으로 진입한다. 데모 안에서 가입한 경우 `demo_id ↔ company_id`를 즉시 연결한다.
- SYSADMIN 데모체험관리: **기본 정보는 계정만료일을 제외하고 read-only**, 신규 수집값은 **추가 정보**로 분리하여 CS 수정 가능. 마지막 **회원사 정보**에서 회원사 ID·회원가입일·결제일을 확인하고, 미연동 건은 **회원사 후보 찾기**로 관리자 확정 연결.
- SYSADMIN 회원사관리: 회원사 정보 하단에 **추가정보 / 데모정보**를 노출. 데모 연동 시 추가정보를 최초 승계하며, 이후 CS가 회원사 기준으로 수정할 수 있다.
- 전환 기준은 기존 P0 원칙대로 **회원가입 완료 + 결제 완료**이며, 데모↔회원사 식별 연결과 유료 전환 집계는 분리한다.
