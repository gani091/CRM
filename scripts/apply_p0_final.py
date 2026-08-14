from pathlib import Path
import re

INDEX = Path('index.html')
DASH = Path('index2.html')
README = Path('README.md')

html = INDEX.read_text(encoding='utf-8')
dash = DASH.read_text(encoding='utf-8')


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected 1 match, found {count}')
    return text.replace(old, new, 1)


def regex_once(text, pattern, replacement, label, flags=re.S):
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f'{label}: expected 1 regex match, found {count}')
    return new_text

# -----------------------------------------------------------------------------
# 1) Homepage demo request form: keep inquiry fields + add 4 decided fields.
#    Purpose = single select, interested features = multi-select dropdown.
# -----------------------------------------------------------------------------
html = replace_once(
    html,
    '''        <div class="grid-2">\n          <!-- 회사명 -->''',
    '''        <div class="grid-2">\n          <!-- 문의 내용 구분: 기존 문의폼 유지 -->\n          <div class="field-group" style="grid-column: 1 / -1;">\n            <label class="field-label" for="inquiry_category">\n              문의 내용 구분 <span class="required">*</span>\n              <span class="dev-field-tag">inquiry_category: Enum</span>\n            </label>\n            <select id="inquiry_category" name="inquiry_category" class="form-select" required onchange="updateDevInspector()">\n              <option value="기능 문의" selected>기능 문의</option>\n              <option value="요금 및 도입 문의">요금 및 도입 문의</option>\n              <option value="기술 지원">기술 지원</option>\n              <option value="기타 문의">기타 문의</option>\n            </select>\n          </div>\n\n          <!-- 회사명 -->''',
    'insert inquiry category'
)

html = replace_once(
    html,
    '''          <!-- 직책 -->\n          <div class="field-group">\n            <label class="field-label" for="job_title">\n              직책 <span class="required">*</span>\n              <span class="dev-field-tag">job_title: String(50)</span>\n            </label>\n            <input type="text" id="job_title" name="job_title" class="form-input" placeholder="담당하고 계시는 직책을 입력해 주세요" required oninput="updateDevInspector()" value="영업 이사">\n          </div>\n        </div>''',
    '''          <!-- 직책 -->\n          <div class="field-group">\n            <label class="field-label" for="job_title">\n              직책 <span class="required">*</span>\n              <span class="dev-field-tag">job_title: String(50)</span>\n            </label>\n            <input type="text" id="job_title" name="job_title" class="form-input" placeholder="담당하고 계시는 직책을 입력해 주세요" required oninput="updateDevInspector()" value="영업 이사">\n          </div>\n\n          <!-- 문의 내용: 기존 문의폼 유지 -->\n          <div class="field-group" style="grid-column: 1 / -1;">\n            <label class="field-label" for="inquiry_content">\n              문의 내용 <span class="required">*</span>\n              <span class="sub-info"><span id="inquiryCharCount">0</span> / 2000</span>\n              <span class="dev-field-tag">inquiry_content: String(2000)</span>\n            </label>\n            <textarea id="inquiry_content" name="inquiry_content" class="form-textarea" maxlength="2000" placeholder="문의내용을 입력하세요." required oninput="document.getElementById('inquiryCharCount').innerText=this.value.length; updateDevInspector();"></textarea>\n          </div>\n        </div>''',
    'insert inquiry content'
)

html = html.replace('데모체험 분석 데이터 수집', '추가 정보', 1)
html = html.replace('맞춤 설정 (선택)', '선택 입력', 1)

html = regex_once(
    html,
    r'''          <!-- 2\. 데모체험 목적 \(단일선택 라디오\) -->.*?          <!-- 3\. 관심 기능 항목 \(복수선택, 최대 3개\) -->.*?          <!-- 4\. 신청경로 -->''',
    '''          <!-- 2. 데모체험 목적 (단일 선택 Select Box) -->\n          <div class="field-group">\n            <label class="field-label" for="demo_purpose">\n              데모체험 목적\n              <span class="dev-field-tag">demo_purpose: Enum</span>\n            </label>\n            <select id="demo_purpose" name="demo_purpose" class="form-select" onchange="updateDevInspector()">\n              <option value="">데모체험 목적을 선택해주세요</option>\n              <option value="실제 CRM 도입을 검토하고 있어요" selected>실제 CRM 도입을 검토하고 있어요</option>\n              <option value="위시드 CRM의 기능을 확인하고 싶어요">위시드 CRM의 기능을 확인하고 싶어요</option>\n              <option value="사내 업무 적용을 테스트하고 싶어요">사내 업무 적용을 테스트하고 싶어요</option>\n              <option value="다른 CRM과 비교하고 있어요">다른 CRM과 비교하고 있어요</option>\n              <option value="기타">기타</option>\n            </select>\n          </div>\n\n          <!-- 3. 관심 있는 기능 (복수 선택 Select Box) -->\n          <div class="field-group">\n            <label class="field-label">\n              관심 있는 기능\n              <span class="dev-field-tag">interested_features: Array[Enum]</span>\n            </label>\n            <details class="feature-multiselect" id="featureMultiSelect">\n              <summary><span id="featureMultiSelectLabel">관심 있는 기능을 선택해주세요</span><span class="feature-multiselect-arrow">⌄</span></summary>\n              <div class="feature-multiselect-menu">\n                <label><input type="checkbox" name="interested_features" value="고객·고객사 관리" checked onchange="updateFeatureMultiSelectLabel();updateDevInspector()"> 고객·고객사 관리</label>\n                <label><input type="checkbox" name="interested_features" value="영업기회 관리" checked onchange="updateFeatureMultiSelectLabel();updateDevInspector()"> 영업기회 관리</label>\n                <label><input type="checkbox" name="interested_features" value="영업활동 관리" onchange="updateFeatureMultiSelectLabel();updateDevInspector()"> 영업활동 관리</label>\n                <label><input type="checkbox" name="interested_features" value="일정 관리" onchange="updateFeatureMultiSelectLabel();updateDevInspector()"> 일정 관리</label>\n                <label><input type="checkbox" name="interested_features" value="견적·계약 관리" onchange="updateFeatureMultiSelectLabel();updateDevInspector()"> 견적·계약 관리</label>\n                <label><input type="checkbox" name="interested_features" value="매출 관리" onchange="updateFeatureMultiSelectLabel();updateDevInspector()"> 매출 관리</label>\n                <label><input type="checkbox" name="interested_features" value="통계·분석" checked onchange="updateFeatureMultiSelectLabel();updateDevInspector()"> 통계·분석</label>\n                <label><input type="checkbox" name="interested_features" value="기타" onchange="updateFeatureMultiSelectLabel();updateDevInspector()"> 기타</label>\n              </div>\n            </details>\n            <p class="field-help">여러 기능을 선택할 수 있습니다.</p>\n          </div>\n\n          <!-- 4. 신청경로 -->''',
    'replace purpose and feature controls'
)

# Add CSS for select-box style multi selector and visible admin sections.
html = replace_once(
    html,
    '''    /* RADIO OPTIONS */''',
    '''    /* FINAL P0 MULTI-SELECT */\n    .feature-multiselect { position: relative; width: 100%; }\n    .feature-multiselect summary { list-style:none; height:48px; border:1px solid var(--border-color); border-radius:var(--radius-sm); background:#fff; padding:0 16px; display:flex; align-items:center; justify-content:space-between; cursor:pointer; font-size:15px; color:var(--text-main); box-shadow:var(--shadow-input); }\n    .feature-multiselect summary::-webkit-details-marker { display:none; }\n    .feature-multiselect[open] summary { border-color:var(--border-focus); box-shadow:0 0 0 3px rgba(37,99,235,.12); }\n    .feature-multiselect-menu { position:absolute; z-index:30; left:0; right:0; top:54px; max-height:260px; overflow:auto; padding:8px; background:#fff; border:1px solid #d7dee8; border-radius:8px; box-shadow:0 12px 28px rgba(15,23,42,.14); }\n    .feature-multiselect-menu label { display:flex; align-items:center; gap:9px; min-height:38px; padding:7px 9px; border-radius:6px; cursor:pointer; font-size:14px; }\n    .feature-multiselect-menu label:hover { background:#f8fafc; }\n    .feature-multiselect-menu input { width:17px; height:17px; accent-color:#2563eb; }\n    .feature-multiselect-arrow { color:#64748b; }\n    .field-help { font-size:12px; color:#94a3b8; margin-top:2px; }\n    .admin-section-divider { height:1px; background:#e5e9ef; margin:22px 0; }\n    .admin-section-head { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:14px; }\n    .admin-section-head h3 { margin:0; }\n    .admin-editable-note { font-size:10px; color:#2563eb; background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:3px 8px; font-weight:700; }\n    .admin-multi-select { min-height:96px !important; height:96px !important; padding:6px 8px !important; }\n    .admin-help { margin-top:5px; font-size:10px; color:#8492a6; }\n    .member-section { margin-top:20px; padding-top:18px; border-top:1px solid #e4e8ee; }\n    .member-section h3 { display:flex; align-items:center; justify-content:space-between; gap:10px; }\n\n    /* RADIO OPTIONS */''',
    'insert p0 css'
)

# New demo state fields and form extraction.
html = replace_once(
    html,
    '''            demo_id: generatedDemoId,\n            company_name: userSubmittedCompany,''',
    '''            demo_id: generatedDemoId,\n            inquiry_category: document.getElementById('inquiry_category')?.value || '기능 문의',\n            inquiry_content: document.getElementById('inquiry_content')?.value || '',\n            privacy_agree: document.getElementById('privacy_agree')?.checked !== false,\n            company_name: userSubmittedCompany,''',
    'add inquiry values to new demo'
)
html = replace_once(
    html,
    '''            demo_purpose: document.querySelector('input[name="demo_purpose"]:checked')?.value || "실제 CRM 도입 검토",''',
    '''            demo_purpose: document.getElementById('demo_purpose')?.value || "실제 CRM 도입 검토",''',
    'read purpose select'
)
html = replace_once(
    html,
    '''      updateFeatureCounter();\n    });''',
    '''      updateFeatureCounter();\n      updateFeatureMultiSelectLabel();\n    });''',
    'initialize multi select label'
)

# Add helper before existing radio/checkbox handlers.
html = replace_once(
    html,
    '''    // FORM RADIO AND CHECKBOX HANDLERS''',
    '''    function updateFeatureMultiSelectLabel() {\n      const label = document.getElementById('featureMultiSelectLabel');\n      if (!label) return;\n      const values = Array.from(document.querySelectorAll('input[name="interested_features"]:checked')).map(el => el.value);\n      label.textContent = values.length ? (values.length <= 2 ? values.join(', ') : `${values[0]}, ${values[1]} 외 ${values.length - 2}개`) : '관심 있는 기능을 선택해주세요';\n    }\n\n    // FORM RADIO AND CHECKBOX HANDLERS''',
    'insert multiselect helper'
)

# -----------------------------------------------------------------------------
# 2) SYSADMIN demo detail. Existing inquiry fields readonly except expiry.
#    Added fields editable by CS. Member info is a visible final section.
# -----------------------------------------------------------------------------
new_render_demo = r'''    function renderSysDemoShell() {
      const mount = document.getElementById('sysDemoMount');
      if (!mount) return;
      if (appState.sysDemoPage === 'detail') {
        const demo = getSelectedDemo();
        mount.innerHTML = `<div class="admin-detail-screen">
          <div class="admin-detail-toolbar">
            <div class="admin-detail-title"><span>👥</span><span>WeSeed-데모체험관리 조회</span><span class="link-id">${demo?.demo_id || ''}</span></div>
            <div class="admin-detail-actions"><button class="admin-action-btn light" onclick="showSysDemoList()">목록</button><button class="admin-action-btn trash" title="삭제" onclick="deleteCurrentDemo()">♲</button><button class="admin-action-btn primary" onclick="saveSysDemoDetail()">저장</button></div>
          </div>
          <section class="admin-detail-card">
            <div class="admin-section-head"><h3>기본 정보</h3><span style="font-size:10px;color:#7b8798">계정만료일만 수정 가능</span></div>
            <div class="admin-form-grid">
              <div class="admin-field"><label>문의 내용 구분</label><input id="dt_inquiry_category" readonly></div>
              <div class="admin-field"><label class="required">회사명</label><input id="dt_company_name" readonly></div>
              <div class="admin-field"><label class="required">예상 사용 인원</label><input id="dt_user_count" readonly></div>
              <div class="admin-field"><label class="required">담당자명</label><input id="dt_contact_name" readonly></div>
              <div class="admin-field"><label class="required">휴대전화</label><input id="dt_phone" readonly></div>
              <div class="admin-field"><label class="required">직책</label><input id="dt_job_title" readonly></div>
              <div class="admin-field"><label class="required">회사 이메일</label><input id="dt_email" readonly></div>
              <div class="admin-field"><label>개인정보 동의</label><input id="dt_privacy" readonly></div>
              <div class="admin-field"><label>계정만료일</label><input id="dt_expiry_date" type="text"></div>
              <div class="admin-field full"><label>문의 내용</label><textarea id="dt_inquiry_content" readonly></textarea></div>
            </div>

            <div class="admin-section-divider"></div>
            <div class="admin-section-head"><h3>추가 정보</h3><span class="admin-editable-note">CS 수정 가능</span></div>
            <div class="admin-form-grid">
              <div class="admin-field"><label>업종</label><input id="dt_industry" placeholder="업종 입력"></div>
              <div class="admin-field"><label>데모체험 목적</label><select id="dt_demo_purpose"><option value="">선택</option><option>실제 CRM 도입을 검토하고 있어요</option><option>위시드 CRM의 기능을 확인하고 싶어요</option><option>사내 업무 적용을 테스트하고 싶어요</option><option>다른 CRM과 비교하고 있어요</option><option>기타</option></select></div>
              <div class="admin-field"><label>신청경로</label><select id="dt_application_source"><option value="">선택</option><option>구글 광고</option><option>네이버 검색/광고</option><option>위시드 홈페이지</option><option>지인 추천</option><option>영업 담당자 안내</option><option>기타</option></select></div>
              <div class="admin-field"><label>관심 있는 기능</label><select id="dt_interested_features" class="admin-multi-select" multiple><option>고객·고객사 관리</option><option>영업기회 관리</option><option>영업활동 관리</option><option>일정 관리</option><option>견적·계약 관리</option><option>매출 관리</option><option>통계·분석</option><option>기타</option></select><div class="admin-help">Ctrl/⌘ 없이 항목을 클릭해 여러 개 선택할 수 있는 운영 UI로 구현 권장</div></div>
            </div>

            <div class="admin-section-divider"></div>
            <div class="admin-section-head"><h3>회원사 정보</h3><span id="dt_link_badge" class="badge-status gray">미연동</span></div>
            <div class="admin-form-grid">
              <div class="admin-field"><label>회원사 ID</label><input id="dt_company_id" readonly placeholder="연동된 회원사 없음"></div>
              <div class="admin-field"><label>회원가입일</label><input id="dt_signup_at" readonly></div>
              <div class="admin-field"><label>결제일</label><input id="dt_paid_at" readonly></div>
              <div class="admin-field"><label>연동 방식</label><input id="dt_linked_by" readonly></div>
              <div class="admin-field full" id="dt_candidate_action"><button type="button" class="admin-action-btn light" onclick="openCandidateMatchModal()">🔍 회원사 후보 찾기</button><span style="margin-left:10px;color:#718096;font-size:10px">데모 종료 후 별도 가입한 회원사는 후보 검색 후 관리자가 확정합니다.</span></div>
            </div>
          </section>
          <details class="p0-audit"><summary>개발 검증용 전환 상태 · Activation 로그</summary><div class="p0-audit-body" id="conversionDetailsContainer"></div></details>
        </div>`;
        updateSysDetailView();
        return;
      }
      mount.innerHTML = `<div class="admin-console">${adminTopbarMarkup()}<div class="admin-layout">${adminSidebarMarkup('WeSeed-데모체험관리')}<main class="admin-main">
        <div class="admin-page-heading"><h2 class="admin-page-title"><span>👥</span>WeSeed-데모체험관리</h2><div class="admin-list-tools"><span class="admin-result-count">검색 결과 1,287 건</span><div class="admin-search-wrap"><input id="sysDemoSearchInput" placeholder="텍스트를 검색하세요" oninput="filterDemoList(this.value)"><button title="상세검색">☷</button><button onclick="filterDemoList(document.getElementById('sysDemoSearchInput').value)" title="검색">⌕</button></div><button class="admin-icon-btn" onclick="deleteCheckedDemos()" title="삭제">♲</button></div></div>
        <table class="admin-data-table"><thead><tr><th class="check-col"><input id="sysDemoCheckAll" type="checkbox" onchange="toggleAllDemoChecks(this.checked)"></th><th style="width:9%">서비스구분</th><th style="width:12%">회사명</th><th style="width:11%">예상사용인원</th><th style="width:8%">담당자명</th><th style="width:16%">전화번호</th><th style="width:22%">회사이메일</th><th style="width:7%">직책</th><th style="width:13%">등록일시</th></tr></thead><tbody id="sysDemoTbody"></tbody></table>
        <div class="admin-list-footer"><select class="admin-page-size"><option>10</option></select><div class="admin-pagination"><button class="active">1</button><button>2</button><button>3</button><button>4</button><button>5</button><button>6</button><button>7</button><button>8</button><button>…</button><button>129</button><button>›</button></div></div>
      </main></div></div>`;
      renderSysDemoList();
    }
'''
html = regex_once(
    html,
    r'''    function renderSysDemoShell\(\) \{.*?\n    \}\n\n    function renderSysCompanyShell''',
    new_render_demo + '\n    function renderSysCompanyShell',
    'replace sysdemo renderer'
)

new_save_demo = r'''    function saveSysDemoDetail() {
      const demo = getSelectedDemo();
      if (!demo) return;
      demo.expiry_date = document.getElementById('dt_expiry_date')?.value || demo.expiry_date;
      demo.industry = document.getElementById('dt_industry')?.value || '';
      demo.demo_purpose = document.getElementById('dt_demo_purpose')?.value || '';
      demo.application_source = document.getElementById('dt_application_source')?.value || '';
      demo.interested_features = Array.from(document.getElementById('dt_interested_features')?.selectedOptions || []).map(option => option.value);
      showToast('추가 정보와 계정만료일이 저장되었습니다.','success');
      updateSysDetailView();
    }
'''
html = regex_once(
    html,
    r'''    function saveSysDemoDetail\(\) \{.*?\n    \}\n\n    function updateSysDetailView''',
    new_save_demo + '\n    function updateSysDetailView',
    'replace demo save'
)

new_update_demo = r'''    function updateSysDetailView() {
      const curDemo = getSelectedDemo();
      if (!curDemo) return;
      const setValue = (id, value) => { const el = document.getElementById(id); if (el) el.value = value ?? ''; };
      setValue('dt_inquiry_category', curDemo.inquiry_category || '기능 문의');
      setValue('dt_company_name', curDemo.company_name);
      setValue('dt_user_count', curDemo.user_count);
      setValue('dt_contact_name', curDemo.contact_name);
      setValue('dt_phone', curDemo.phone);
      setValue('dt_job_title', curDemo.job_title);
      setValue('dt_email', curDemo.email);
      setValue('dt_privacy', curDemo.privacy_agree === false ? '미동의' : '동의');
      setValue('dt_expiry_date', String(curDemo.expiry_date || '').replaceAll('-','.'));
      setValue('dt_inquiry_content', curDemo.inquiry_content || curDemo.note || '-');
      setValue('dt_industry', curDemo.industry || '');
      setValue('dt_demo_purpose', normalizePurposeLabel(curDemo.demo_purpose));
      setValue('dt_application_source', curDemo.application_source || '');
      const multi = document.getElementById('dt_interested_features');
      if (multi) Array.from(multi.options).forEach(option => { option.selected = (curDemo.interested_features || []).includes(option.value); });
      setValue('dt_company_id', curDemo.company_id || '');
      setValue('dt_signup_at', curDemo.timestamps?.signup_completed_at || '');
      setValue('dt_paid_at', curDemo.timestamps?.paid_at || '');
      setValue('dt_linked_by', curDemo.linked_by === 'DIRECT_SIGNUP' ? '데모 내 회원가입 자동연동' : (curDemo.linked_by === 'SYSADMIN_MANUAL' ? '관리자 후보매칭' : ''));
      const badge = document.getElementById('dt_link_badge');
      if (badge) { badge.className = `badge-status ${curDemo.company_id ? 'green' : 'gray'}`; badge.textContent = curDemo.company_id ? '연동 완료' : '미연동'; }
      const candidate = document.getElementById('dt_candidate_action');
      if (candidate) candidate.style.display = curDemo.company_id ? 'none' : 'block';
      renderDemoP0Details(curDemo);
    }

    function normalizePurposeLabel(value) {
      const text = String(value || '');
      if (text.includes('실제 CRM 도입')) return '실제 CRM 도입을 검토하고 있어요';
      if (text.includes('기능 확인') || text.includes('기능을 확인')) return '위시드 CRM의 기능을 확인하고 싶어요';
      if (text.includes('업무 적용')) return '사내 업무 적용을 테스트하고 싶어요';
      if (text.includes('비교')) return '다른 CRM과 비교하고 있어요';
      return text;
    }
'''
html = regex_once(
    html,
    r'''    function updateSysDetailView\(\) \{.*?\n    \}\n\n    function renderDemoP0Details''',
    new_update_demo + '\n    function renderDemoP0Details',
    'replace demo detail updater'
)

# -----------------------------------------------------------------------------
# 3) Member company detail. Initial sync from linked demo, then editable by CS.
# -----------------------------------------------------------------------------
html = replace_once(
    html,
    '''      selectedDemoId: 'DEMO-2026-8942',\n      demoList: [''',
    '''      selectedDemoId: 'DEMO-2026-8942',\n      selectedCompanyId: 'COMP-2026-RAPHAB',\n      companyExtraInfo: {},\n      demoList: [''',
    'add member extra store'
)

new_render_company = r'''    function renderSysCompanyShell() {
      const mount = document.getElementById('sysCompanyMount');
      if (!mount) return;
      const linkedDemo = appState.demoList.find(d => d.company_id === appState.selectedCompanyId) || appState.demoList.find(d => d.company_id === 'COMP-2026-RAPHAB') || appState.demoList.find(d => d.company_id);
      const isReferenceCompany = appState.selectedCompanyId === 'COMP-2026-RAPHAB';
      const companyName = isReferenceCompany ? '(주)라파비' : (linkedDemo?.company_name || '(주)라파비');
      const representative = isReferenceCompany ? '조상수' : (linkedDemo?.contact_name || '조상수');
      const companyIndustry = isReferenceCompany ? '제조' : (linkedDemo?.industry || '-');
      const extra = ensureCompanyExtraInfo(linkedDemo);
      const featureOptions = ['고객·고객사 관리','영업기회 관리','영업활동 관리','일정 관리','견적·계약 관리','매출 관리','통계·분석','기타'];
      const featureMarkup = featureOptions.map(v => `<option ${extra.interested_features.includes(v) ? 'selected' : ''}>${v}</option>`).join('');
      const purposeOptions = ['', '실제 CRM 도입을 검토하고 있어요','위시드 CRM의 기능을 확인하고 싶어요','사내 업무 적용을 테스트하고 싶어요','다른 CRM과 비교하고 있어요','기타'];
      const purposeMarkup = purposeOptions.map(v => `<option value="${v}" ${normalizePurposeLabel(extra.demo_purpose) === v ? 'selected' : ''}>${v || '선택'}</option>`).join('');
      const sourceOptions = ['', '구글 광고','네이버 검색/광고','위시드 홈페이지','지인 추천','영업 담당자 안내','기타'];
      const sourceMarkup = sourceOptions.map(v => `<option value="${v}" ${extra.application_source === v ? 'selected' : ''}>${v || '선택'}</option>`).join('');
      mount.innerHTML = `<div class="admin-console company-console">${adminTopbarMarkup()}<div class="admin-layout">${adminSidebarMarkup('회원사관리')}<main class="company-workspace">
        <section class="company-summary"><div class="company-toolbar"><button class="admin-action-btn light" onclick="showToast('회원사 목록으로 이동합니다.','info')">‹&nbsp; 목록</button><div class="company-toolbar-actions"><button class="admin-icon-btn" title="더보기">•••</button><button class="admin-action-btn light">결제하기</button><button class="admin-action-btn primary" onclick="saveSysCompanyDetail()">저장</button></div></div><h3 style="font-size:12px;margin:0 0 9px">회원사관리조회</h3><div class="company-basic-title">기본 정보</div>
          <div class="company-info-row"><label class="required">회원사명</label><strong id="comp_name_val">${companyName}</strong></div><div class="company-info-row"><label class="required">법인명</label><strong>${companyName}</strong></div><div class="company-info-row"><label class="required">대표자</label><strong>${representative}</strong></div><div class="company-info-row"><label class="required">사업자번호</label><strong>878-87-03003</strong></div><div class="company-info-row"><label class="required">업태</label><strong>살균조명</strong></div><div class="company-info-row"><label class="required">업종</label><strong>${companyIndustry}</strong></div><div class="company-info-row"><label class="required">우편번호</label><strong>50834</strong></div><div class="company-info-row"><label class="required">주소</label><strong>경남 김해시 인제로 197</strong></div><div class="company-info-row"><label class="required">상세주소</label><strong>프라임임생명공학관 7층 IJCS-1호</strong></div><div class="company-info-row"><label class="required">담당자</label><strong>${representative}</strong></div><div class="company-info-row"><label>SMS발신번호</label><strong></strong></div>
        </section>
        <section class="company-payment"><div class="company-tabs"><button class="active">결제정보</button><button>부가서비스 정보</button><button>사용자정보</button></div><div class="company-payment-card"><h3>회원사 정보</h3><div class="company-pay-grid">
          <div class="admin-field"><label class="required">회원사상태</label><select><option>승인</option></select></div><div class="admin-field"><label>서비스만료일</label><input value="2027.05.18"></div><div class="admin-field"><label class="required">결제구분</label><select><option>매월</option></select></div><div class="admin-field"><label class="required">인원(신청/사용)</label><div style="display:grid;grid-template-columns:1fr 1fr;gap:7px"><input value="3"><input value="3" readonly></div></div><div class="admin-field"><label>월결제금액</label><input value="60,000" readonly></div><div class="admin-field"><label>가입비</label><input value="200,000"></div><div class="admin-field"><label>1인당 월 결제금액</label><input value="20,000"></div>
        </div>
        <div class="member-section"><h3>추가정보 <span class="admin-editable-note">CS 수정 가능</span></h3><div class="company-pay-grid">
          <div class="admin-field"><label>업종</label><input id="comp_extra_industry" value="${extra.industry || ''}"></div>
          <div class="admin-field"><label>데모체험 목적</label><select id="comp_extra_purpose">${purposeMarkup}</select></div>
          <div class="admin-field"><label>신청경로</label><select id="comp_extra_source">${sourceMarkup}</select></div>
          <div class="admin-field"><label>관심 있는 기능</label><select id="comp_extra_features" class="admin-multi-select" multiple>${featureMarkup}</select></div>
        </div><div class="admin-help">데모 연동 시 최초 1회 데모의 추가정보를 가져오며, 이후 CS가 회원사 기준으로 수정할 수 있습니다.</div></div>
        <div class="member-section"><h3>데모정보 ${linkedDemo ? '<span class="badge-status green">연동 완료</span>' : '<span class="badge-status gray">미연동</span>'}</h3>${linkedDemo ? `<div class="company-pay-grid"><div class="admin-field"><label>Demo ID</label><input value="${linkedDemo.demo_id}" readonly onclick="navigateToDemoDetail('${linkedDemo.demo_id}')" style="color:#2563eb;cursor:pointer;font-weight:700"></div><div class="admin-field"><label>데모계정</label><input value="${linkedDemo.demo_account || ''}" readonly></div><div class="admin-field"><label>데모 신청일</label><input value="${linkedDemo.created_at || ''}" readonly></div><div class="admin-field"><label>계정만료일</label><input value="${linkedDemo.expiry_date || ''}" readonly></div><div class="admin-field"><label>회원가입일</label><input value="${linkedDemo.timestamps?.signup_completed_at || ''}" readonly></div><div class="admin-field"><label>결제일</label><input value="${linkedDemo.timestamps?.paid_at || ''}" readonly></div></div>` : '<div style="font-size:11px;color:#718096">연동된 데모체험 정보가 없습니다.</div>'}</div>
        </div></section>
      </main></div></div>`;
    }

    function ensureCompanyExtraInfo(linkedDemo) {
      const companyId = appState.selectedCompanyId || linkedDemo?.company_id || 'UNLINKED';
      if (!appState.companyExtraInfo[companyId]) {
        appState.companyExtraInfo[companyId] = {
          industry: linkedDemo?.industry || '',
          demo_purpose: linkedDemo?.demo_purpose || '',
          interested_features: [...(linkedDemo?.interested_features || [])],
          application_source: linkedDemo?.application_source || ''
        };
      }
      return appState.companyExtraInfo[companyId];
    }

    function syncDemoExtraToCompany(demo) {
      if (!demo?.company_id) return;
      if (!appState.companyExtraInfo[demo.company_id]) {
        appState.companyExtraInfo[demo.company_id] = {
          industry: demo.industry || '',
          demo_purpose: demo.demo_purpose || '',
          interested_features: [...(demo.interested_features || [])],
          application_source: demo.application_source || ''
        };
      }
    }

    function saveSysCompanyDetail() {
      const linkedDemo = appState.demoList.find(d => d.company_id === appState.selectedCompanyId);
      const extra = ensureCompanyExtraInfo(linkedDemo);
      extra.industry = document.getElementById('comp_extra_industry')?.value || '';
      extra.demo_purpose = document.getElementById('comp_extra_purpose')?.value || '';
      extra.application_source = document.getElementById('comp_extra_source')?.value || '';
      extra.interested_features = Array.from(document.getElementById('comp_extra_features')?.selectedOptions || []).map(option => option.value);
      showToast('회원사 추가정보가 저장되었습니다.','success');
    }
'''
html = regex_once(
    html,
    r'''    function renderSysCompanyShell\(\) \{.*?\n    \}\n\n    // DOM CONTENT LOADED INITIALIZATION''',
    new_render_company + '\n    // DOM CONTENT LOADED INITIALIZATION',
    'replace member company renderer'
)

# Sync demo extra info whenever a direct or manual company link is established.
html = replace_once(
    html,
    '''        if (curDemo.timestamps) curDemo.timestamps.signup_completed_at = nowStr;\n      }\n      showToast('회원사 정보 입력 완료! 요금 결제 단계로 이동합니다.', 'info');''',
    '''        if (curDemo.timestamps) curDemo.timestamps.signup_completed_at = nowStr;\n        syncDemoExtraToCompany(curDemo);\n      }\n      showToast('회원사 정보 입력 완료! 데모 계정과 회원사 ID가 즉시 연동되었습니다.', 'success');''',
    'sync direct signup'
)
html = replace_once(
    html,
    '''      showToast(`회원사 연결이 완료되었습니다.\\n(${curDemo.demo_id} ↔ ${pendingCandidateCompId})`, 'success');''',
    '''      syncDemoExtraToCompany(curDemo);\n      showToast(`회원사 연결이 완료되었습니다.\\n(${curDemo.demo_id} ↔ ${pendingCandidateCompId})`, 'success');''',
    'sync manual match'
)

# -----------------------------------------------------------------------------
# 4) Demo CRM top trial strip banner (blue active / red deadline), price/new tab,
#    signup -> same prototype signup entry and immediate demo linkage.
# -----------------------------------------------------------------------------
dash = replace_once(
    dash,
    '''    .topbar{height:49px;background:#fff;border-bottom:1px solid #e5e7eb;display:flex;align-items:center;position:fixed;inset:0 0 auto 0;z-index:3}''',
    '''    .trial-banner{height:54px;position:fixed;inset:0 0 auto 0;z-index:5;display:flex;align-items:center;padding:0 22px;gap:12px;border-bottom:1px solid #bfd3ff;background:#eaf1ff;color:#2458a6}.trial-banner.urgent{background:#fff0f0;border-color:#ffc7c7;color:#bf3434}.trial-dot{width:9px;height:9px;border-radius:50%;background:#2668ec;flex:0 0 auto}.trial-banner.urgent .trial-dot{background:#dc3f3f}.trial-badge{padding:5px 10px;border-radius:5px;background:#2868f6;color:#fff;font-size:12px;font-weight:800}.trial-banner.urgent .trial-badge{background:#dc3f3f}.trial-message{font-size:13px;font-weight:600;flex:1}.trial-actions{display:flex;gap:10px;align-items:center}.trial-price,.trial-signup{height:34px;border-radius:6px;padding:0 16px;font-size:12px;font-weight:800;cursor:pointer}.trial-price{background:#fff;border:1px solid #2868f6;color:#2868f6}.trial-signup{border:0;background:#2868f6;color:#fff}.trial-banner.urgent .trial-price{border-color:#e33e3e;color:#d43737}.trial-banner.urgent .trial-signup{background:#d83b3b}.trial-close{width:30px;height:30px;border:0;background:transparent;font-size:23px;color:inherit;cursor:pointer}.topbar{height:49px;background:#fff;border-bottom:1px solid #e5e7eb;display:flex;align-items:center;position:fixed;inset:54px 0 auto 0;z-index:3}''',
    'banner css topbar offset'
)
dash = dash.replace('.sidebar{position:fixed;left:0;top:49px;', '.sidebar{position:fixed;left:0;top:103px;', 1)
dash = dash.replace('.content{margin-left:211px;padding:78px 0 40px}', '.content{margin-left:211px;padding:132px 0 40px}', 1)

dash = replace_once(
    dash,
    '''<body>\n  <header class="topbar">''',
    '''<body>\n  <section class="trial-banner" id="trialBanner" aria-label="무료체험 기간 안내">\n    <span class="trial-dot"></span><span class="trial-badge">무료체험</span><span class="trial-message" id="trialMessage">무료체험 기간을 확인하고 있습니다.</span>\n    <div class="trial-actions"><button class="trial-price" id="trialPriceButton" type="button">이용요금 확인</button><button class="trial-signup" id="trialSignupButton" type="button">회원가입하기</button><button class="trial-close" id="trialCloseButton" type="button" aria-label="무료체험 안내 닫기">×</button></div>\n  </section>\n  <header class="topbar">''',
    'insert trial banner'
)

# Remove duplicate top header signup CTA: signup is now consistently in the strip banner.
dash = dash.replace('<div class="top-actions"><button class="top-signup" id="guestSignupButton" type="button">회원가입하기</button>', '<div class="top-actions">', 1)

dash = replace_once(
    dash,
    '''      const signupButton = document.getElementById('guestSignupButton');\n      if (session.conversion_status === 'CONVERTED') {\n        status.textContent = `가입 완료 (${session.company_id})`;\n        signupButton.textContent = '정식 회원사 이용 중';\n        signupButton.disabled = true;\n      } else if (session.conversion_status === 'PAYMENT_PENDING') {\n        status.textContent = '결제 대기';\n        signupButton.textContent = '가입 계속하기';\n        signupButton.disabled = false;\n      } else {\n        status.textContent = '미가입';\n        signupButton.textContent = '회원가입하기';\n        signupButton.disabled = false;\n      }''',
    '''      const signupButton = document.getElementById('trialSignupButton');\n      if (session.conversion_status === 'CONVERTED') {\n        status.textContent = `가입 완료 (${session.company_id})`;\n        signupButton.textContent = '가입 완료';\n        signupButton.disabled = true;\n      } else if (session.conversion_status === 'PAYMENT_PENDING') {\n        status.textContent = '결제 대기';\n        signupButton.textContent = '가입 계속하기';\n        signupButton.disabled = false;\n      } else {\n        status.textContent = '미가입';\n        signupButton.textContent = '회원가입하기';\n        signupButton.disabled = false;\n      }\n      updateTrialBanner(session);''',
    'sync trial cta'
)

dash = replace_once(
    dash,
    '''    function toggleGuestMenu(event) {''',
    '''    function updateTrialBanner(session = getGuestSession()) {\n      const banner = document.getElementById('trialBanner');\n      const message = document.getElementById('trialMessage');\n      if (!banner || !message || !session) return;\n      const today = new Date();\n      today.setHours(0,0,0,0);\n      const expiry = new Date(String(session.expiry_date || '').replaceAll('.', '-'));\n      expiry.setHours(0,0,0,0);\n      const days = Number.isNaN(expiry.getTime()) ? 14 : Math.ceil((expiry - today) / 86400000);\n      const urgent = days <= 0;\n      banner.classList.toggle('urgent', urgent);\n      if (days < 0) message.textContent = '무료체험이 종료되었습니다. CRM 이용이 제한됩니다.';\n      else if (days === 0) message.textContent = '무료체험이 오늘 종료됩니다. 체험 종료 후 CRM 이용이 제한됩니다.';\n      else message.textContent = `무료체험이 ${days}일 후 종료됩니다. 주요 기능을 직접 사용해 보세요.`;\n    }\n\n    function toggleGuestMenu(event) {''',
    'add banner updater'
)

dash = replace_once(
    dash,
    '''    document.getElementById('guestProfileButton').addEventListener('click', toggleGuestMenu);\n    document.getElementById('guestSignupButton').addEventListener('click', startGuestSignup);''',
    '''    document.getElementById('guestProfileButton').addEventListener('click', toggleGuestMenu);\n    document.getElementById('trialSignupButton').addEventListener('click', startGuestSignup);\n    document.getElementById('trialPriceButton').addEventListener('click', () => window.open('https://weseed.co.kr/payment', '_blank', 'noopener,noreferrer'));\n    document.getElementById('trialCloseButton').addEventListener('click', () => { document.getElementById('trialBanner').style.display='none'; document.querySelector('.topbar').style.top='0'; document.querySelector('.sidebar').style.top='49px'; document.querySelector('.content').style.paddingTop='78px'; });\n    syncGuestMenu();''',
    'wire trial banner actions'
)

# -----------------------------------------------------------------------------
# README decision summary for design/development review.
# -----------------------------------------------------------------------------
readme = README.read_text(encoding='utf-8')
final_note = '''\n\n---\n\n## 2026-08-14 P0 최종 확정안\n\n- 데모 신청: **기존 문의폼 항목 유지** + `업종(input)`, `데모체험 목적(select/single)`, `관심 있는 기능(select/multi)`, `신청경로(select/single)` 추가.\n- 데모 CRM: 무료체험 기간을 **상단 띠 배너**로 노출. `이용요금 확인`은 위시드 요금 페이지를 새 창으로 열고, `회원가입하기`는 회원가입 흐름으로 진입한다. 데모 안에서 가입한 경우 `demo_id ↔ company_id`를 즉시 연결한다.\n- SYSADMIN 데모체험관리: **기본 정보는 계정만료일을 제외하고 read-only**, 신규 수집값은 **추가 정보**로 분리하여 CS 수정 가능. 마지막 **회원사 정보**에서 회원사 ID·회원가입일·결제일을 확인하고, 미연동 건은 **회원사 후보 찾기**로 관리자 확정 연결.\n- SYSADMIN 회원사관리: 회원사 정보 하단에 **추가정보 / 데모정보**를 노출. 데모 연동 시 추가정보를 최초 승계하며, 이후 CS가 회원사 기준으로 수정할 수 있다.\n- 전환 기준은 기존 P0 원칙대로 **회원가입 완료 + 결제 완료**이며, 데모↔회원사 식별 연결과 유료 전환 집계는 분리한다.\n'''
if '## 2026-08-14 P0 최종 확정안' not in readme:
    readme += final_note
README.write_text(readme, encoding='utf-8')

INDEX.write_text(html, encoding='utf-8')
DASH.write_text(dash, encoding='utf-8')
print('P0 final patch applied successfully.')
