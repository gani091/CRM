# WeSeed CRM 데모체험 전환 분석 데이터 구축 PRD & 화면 고도화 프로젝트

> **개발 및 백엔드 연동 가이드**  
> 본 프로젝트는 **WeSeed CRM의 데모 체험 신청자 데이터를 체계적으로 수집하고, `demo_id`와 `company_id`(유료 회원사)간 전환 매칭 구조를 구축**하기 위한 프론트엔드 prototype 및 데이터 스펙 문서입니다.

---

## 📌 주요 요구사항 및 구현 배경

1. **기획 배경**
   - 기존 `무료체험 → 14일 Free Trial` 단순 전환 요구사항에서, **가입 전환율 향상 및 아웃바운드 영업 유용성 확보**를 위해 사용자 행동 분석 및 이용 로그 리포트 기반 프로세스로 고도화 변경.
   - [Figma 기획안 디자인 바로가기](https://www.figma.com/design/KfHz9ymW8fHXRg3KlKDz2k/Weseed-CRM-%EA%B3%A0%EB%8F%84%ED%99%94?node-id=161-667&t=bMttaqBvTXKZks4K-4)

2. **최신 변경사항 (요청 반영)**
   - **데모 신청 폼 필드 정돈**: 불필요한 `도입 예정 시기`, `데모 신청 경력(신규/재방문)` 2개 필드 삭제 (신청 경력은 시스템 자동 로그로 대체).
   - **P0 핵심 기능 구축 (데모 내 직접 회원가입 & 데이터 연동)**:
     - CRM 데모 계정 진입 시 **가상 데이터 안내 팝업(이미지 1)** 노출 및 `[⚡ 회원가입하고 데이터 승계받기]` CTA 제공.
     - CRM 상단 프로필 드롭다운(이미지 2) 내 **`[결제하기]`** 버튼으로 3단계 회원가입 폼 바로 연결.
     - 홈페이지 요금제 회원가입 폼(이미지 3 & 4: 약관동의 → 휴대폰 인증 → 정보입력)을 데모 CRM 내부 팝업으로 연동.
     - 데모 신청 시 작성했던 정보(`회사명`, `담당자명`, `휴대전화`, `이메일`, `업종`)가 **자동으로 Pre-fill(사전 입력)**되어 사용자 회원가입 절차 최적화.
     - 회원가입 완료 시 `demo_id` ↔ `company_id` 매칭이 완료되어 기존 데모 데이터가 신규 유료 회원사 계정으로 승계.

---

## 📋 신청 추가 필드 및 코드값 정의표

| 항목명 | 수집 방식 | 필수 여부 | DB 타입 / 코드값 |
| :--- | :--- | :--- | :--- |
| **업종** | 직접 텍스트 입력 | 선택 | `VARCHAR(100)` (예: IT/SaaS, 제조업, 유통 등) |
| **데모체험 목적** | 단일 선택 (라디오) | 선택 | `PURPOSE_EVALUATE` (실제 CRM 도입 검토)<br>`PURPOSE_CHECK_FEATURES` (기능 확인)<br>`PURPOSE_TEST_FIT` (사내 업무 적용 테스트)<br>`PURPOSE_COMPARE_CRM` (타 CRM과 비교)<br>`PURPOSE_ETC` (기타 + 직접 입력) |
| **관심 기능** | 다중 선택 (체크박스/최대 3개) | 선택 | `FEAT_CUSTOMER` (고객·고객사 관리)<br>`FEAT_OPPORTUNITY` (영업기회 관리)<br>`FEAT_ACTIVITY` (영업활동 관리)<br>`FEAT_SCHEDULE` (일정 관리)<br>`FEAT_QUOTE_CONTRACT` (견적·계약 관리)<br>`FEAT_REVENUE` (매출 관리)<br>`FEAT_ANALYTICS` (통계·분석)<br>`FEAT_ETC` (기타 + 직접 입력) |

---

## 🗄️ 백엔드 DB & API 데이터 스펙

### 1. `POST /api/v1/demo-requests` (JSON Payload 예시)

```json
{
  "company_name": "위시드 테크",
  "user_count": "21-50명",
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
  "current_system": "엑셀 / 수기 / 개인 메모",
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
    user_count VARCHAR(30) NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    job_title VARCHAR(50) NOT NULL,
    industry VARCHAR(100),
    demo_purpose VARCHAR(100),
    interested_features JSONB,
    current_system VARCHAR(100),
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

- **P0 (최우선)**: 전환 기준 정립, `demo_id` 연결 구조, **데모체험 CRM 내 직접 회원가입 & Pre-fill 데이터 연동**, 데모↔회원사 매칭, 신청 추가 필드, 핵심 Activation 수집.
- **P1 (차순위)**: 신규 Event 로그, CS 정형 데이터, 실사용 비교 이벤트.
- **P2 (향후 고도화)**: 분석 대시보드 UI, AI 분석 엔진, 세그먼트 화면.