from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')


def sub_once(pattern, replacement, label, flags=re.S):
    global html
    html2, count = re.subn(pattern, replacement, html, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f'{label}: expected 1 match, found {count}')
    html = html2

# 0) AS-IS tab label = actual current demo form
html = html.replace('📌 AS-IS <span class="badge-mini asis">기존 문의 폼</span>', '📌 AS-IS <span class="badge-mini asis">현재 데모 폼</span>', 1)

# 1) AS-IS: synchronize to the real demo form shown in the reference image.
asis_block = r'''<div id="viewAsIs" class="view-section">
      <section class="hero-section" style="max-width:760px;margin:0 auto 30px;text-align:center;">
        <div class="hero-category">위시드 CRM 데모체험</div>
        <h1 class="hero-title" style="line-height:1.35;">입력하신 이메일 주소로<br>데모 체험 계정을 발송합니다</h1>
        <p style="margin-top:16px;color:#64748B;font-size:16px;">데모 계정은 발급일로부터 14일간 사용 가능합니다.</p>
      </section>

      <form class="form-card" id="asisRequestForm" style="max-width: 600px; margin: 0 auto;" onsubmit="handleAsIsSubmit(event)">
        <div style="display:flex;flex-direction:column;gap:20px;">
          <div class="field-group">
            <label class="field-label" for="asis_company_name">회사명 <span class="required">*</span><span class="dev-field-tag">company_name</span></label>
            <input type="text" id="asis_company_name" class="form-input" placeholder="회사 또는 단체명을 입력해주세요" required>
          </div>
          <div class="field-group">
            <label class="field-label" for="asis_user_count">예상 사용 인원 <span class="required">*</span><span class="dev-field-tag">user_count</span></label>
            <input type="number" id="asis_user_count" class="form-input" min="1" placeholder="예상 사용 인원을 입력해주세요" required>
          </div>
          <div class="field-group">
            <label class="field-label" for="asis_contact_name">담당자 이름 <span class="required">*</span><span class="dev-field-tag">contact_name</span></label>
            <input type="text" id="asis_contact_name" class="form-input" placeholder="담당자 이름을 입력해 주세요" required>
          </div>
          <div class="field-group">
            <label class="field-label" for="asis_email">회사 이메일 <span class="required">*</span><span class="dev-field-tag">email</span></label>
            <input type="email" id="asis_email" class="form-input" placeholder="이메일을 입력해 주세요" required>
          </div>
          <div class="field-group">
            <label class="field-label" for="asis_phone">휴대전화 <span class="required">*</span><span class="dev-field-tag">phone</span></label>
            <input type="tel" id="asis_phone" class="form-input" value="010-5029-1483" readonly aria-readonly="true">
          </div>
          <div class="field-group">
            <label class="field-label" for="asis_job_title">직책 <span class="required">*</span><span class="dev-field-tag">job_title</span></label>
            <input type="text" id="asis_job_title" class="form-input" placeholder="담당하고 계시는 직책을 입력해 주세요" required>
          </div>

          <div class="recaptcha-wrapper">
            <div class="recaptcha-box">
              <div class="recaptcha-left" onclick="toggleRecaptcha('asis')">
                <div class="recaptcha-check" id="recaptchaCheckAsIs"></div>
                <span class="recaptcha-label">로봇이 아닙니다.</span>
              </div>
              <div class="recaptcha-right"><div style="font-size:24px;line-height:1">↻</div><div class="recaptcha-terms">reCAPTCHA<br>약관 · 개인정보</div></div>
            </div>
          </div>

          <button type="submit" class="btn-submit" style="background:#3B82F6;">데모 체험하기</button>
        </div>
      </form>
    </div>
'''
sub_once(
    r'<div id="viewAsIs" class="view-section">.*?(?=\n\s*<!-- ==============================================\n\s*VIEW 1: TO-BE)',
    asis_block,
    'replace AS-IS demo form'
)

# 2) TO-BE basic information: same six fields/order as real demo form.
tobe_basic = r'''        <!-- SECTION 1: 기본 정보 (필수) -->
        <div class="section-header">
          <div class="section-title">기본 정보 <span class="dev-field-tag">SYS_SECTION_1_REQUIRED</span></div>
          <span class="section-badge required-badge">필수 입력</span>
        </div>

        <div class="grid-2">
          <div class="field-group">
            <label class="field-label" for="company_name">회사명 <span class="required">*</span><span class="dev-field-tag">company_name: String(100)</span></label>
            <input type="text" id="company_name" name="company_name" class="form-input" placeholder="회사 또는 단체명을 입력해주세요" required oninput="updateDevInspector()" value="위시드 테크">
          </div>
          <div class="field-group">
            <label class="field-label" for="user_count">예상 사용 인원 <span class="required">*</span><span class="dev-field-tag">user_count: Integer</span></label>
            <input type="number" id="user_count" name="user_count" class="form-input" min="1" step="1" inputmode="numeric" placeholder="예상 사용 인원을 입력해주세요" required oninput="updateDevInspector()" value="20">
          </div>
          <div class="field-group">
            <label class="field-label" for="contact_name">담당자 이름 <span class="required">*</span><span class="dev-field-tag">contact_name: String(50)</span></label>
            <input type="text" id="contact_name" name="contact_name" class="form-input" placeholder="담당자 이름을 입력해 주세요" required oninput="updateDevInspector()" value="김위시드">
          </div>
          <div class="field-group">
            <label class="field-label" for="email">회사 이메일 <span class="required">*</span><span class="dev-field-tag">email: String(100) [MATCH_KEY]</span></label>
            <input type="email" id="email" name="email" class="form-input" placeholder="이메일을 입력해 주세요" required oninput="updateDevInspector()" value="sales@weseed.co.kr">
          </div>
          <div class="field-group">
            <label class="field-label" for="phone">휴대전화 <span class="required">*</span><span class="dev-field-tag">phone: String(20) [MATCH_KEY]</span></label>
            <input type="tel" id="phone" name="phone" class="form-input" value="010-5029-1483" readonly aria-readonly="true">
          </div>
          <div class="field-group">
            <label class="field-label" for="job_title">직책 <span class="required">*</span><span class="dev-field-tag">job_title: String(50)</span></label>
            <input type="text" id="job_title" name="job_title" class="form-input" placeholder="담당하고 계시는 직책을 입력해 주세요" required oninput="updateDevInspector()" value="영업 이사">
          </div>
        </div>

        <div class="divider"></div>

        <!-- SECTION 2:'''
sub_once(
    r'        <!-- SECTION 1: 기본 정보 \(필수\) -->.*?        <div class="divider"></div>\n\n        <!-- SECTION 2:',
    tobe_basic,
    'replace TO-BE basic fields'
)

# Current real demo screen has reCAPTCHA but no separate visible privacy checkbox.
sub_once(
    r'\n\s*<!-- 약관 동의 -->\s*<div class="policy-box">.*?</div>\s*\n\s*<!-- reCAPTCHA -->',
    '\n\n        <!-- reCAPTCHA -->',
    'remove visible privacy checkbox'
)

# Remove legacy inquiry fields from new demo record (they are not real demo application fields).
html = html.replace("            inquiry_category: document.getElementById('inquiry_category')?.value || '기능 문의',\n", '', 1)
html = html.replace("            inquiry_content: document.getElementById('inquiry_content')?.value || '',\n", '', 1)
html = html.replace("            privacy_agree: document.getElementById('privacy_agree')?.checked !== false,\n", '', 1)

# 3) SYSADMIN > 데모체험관리 조회 기본 정보 = same six fields + editable account expiry.
admin_basic = r'''            <div class="admin-section-head"><h3>기본 정보</h3><span style="font-size:10px;color:#7b8798">계정만료일만 수정 가능</span></div>
            <div class="admin-form-grid">
              <div class="admin-field"><label class="required">회사명</label><input id="dt_company_name" readonly></div>
              <div class="admin-field"><label class="required">예상 사용 인원</label><input id="dt_user_count" readonly></div>
              <div class="admin-field"><label class="required">담당자 이름</label><input id="dt_contact_name" readonly></div>
              <div class="admin-field"><label class="required">회사 이메일</label><input id="dt_email" readonly></div>
              <div class="admin-field"><label class="required">휴대전화</label><input id="dt_phone" readonly></div>
              <div class="admin-field"><label class="required">직책</label><input id="dt_job_title" readonly></div>
              <div class="admin-field"><label>계정만료일</label><input id="dt_expiry_date" type="text"></div>
            </div>

            <div class="admin-section-divider"></div>'''
sub_once(
    r'            <div class="admin-section-head"><h3>기본 정보</h3><span style="font-size:10px;color:#7b8798">계정만료일만 수정 가능</span></div>\s*<div class="admin-form-grid">.*?<div class="admin-field full"><label>문의 내용</label><textarea id="dt_inquiry_content" readonly></textarea></div>\s*</div>\s*\n\s*<div class="admin-section-divider"></div>',
    admin_basic,
    'sync SYSADMIN demo basic fields'
)

# Remove no-longer-rendered value assignments.
html = html.replace("      setValue('dt_inquiry_category', curDemo.inquiry_category || '기능 문의');\n", '', 1)
html = html.replace("      setValue('dt_privacy', curDemo.privacy_agree === false ? '미동의' : '동의');\n", '', 1)
html = html.replace("      setValue('dt_inquiry_content', curDemo.inquiry_content || curDemo.note || '-');\n", '', 1)

# Keep read-only detail ordering aligned with the screen reference.
old_order = "      setValue('dt_contact_name', curDemo.contact_name);\n      setValue('dt_phone', curDemo.phone);\n      setValue('dt_job_title', curDemo.job_title);\n      setValue('dt_email', curDemo.email);"
new_order = "      setValue('dt_contact_name', curDemo.contact_name);\n      setValue('dt_email', curDemo.email);\n      setValue('dt_phone', curDemo.phone);\n      setValue('dt_job_title', curDemo.job_title);"
if old_order in html:
    html = html.replace(old_order, new_order, 1)

# AS-IS is now the real demo request, not an inquiry form.
html = html.replace("      showToast('📩 AS-IS 기존 방식 문의하기 접수가 완료되었습니다.', 'info');", "      showToast('📩 데모 체험 신청이 완료되었습니다. 입력한 이메일로 계정이 발송됩니다.', 'info');", 1)

# 4) SYSADMIN > 회원사관리조회 > 데모정보: remove duplicated expiry/signup/payment fields.
old_demo_info = '''<div class="member-section"><h3>데모정보 ${linkedDemo ? '<span class="badge-status green">연동 완료</span>' : '<span class="badge-status gray">미연동</span>'}</h3>${linkedDemo ? `<div class="company-pay-grid"><div class="admin-field"><label>Demo ID</label><input value="${linkedDemo.demo_id}" readonly onclick="navigateToDemoDetail('${linkedDemo.demo_id}')" style="color:#2563eb;cursor:pointer;font-weight:700"></div><div class="admin-field"><label>데모계정</label><input value="${linkedDemo.demo_account || ''}" readonly></div><div class="admin-field"><label>데모 신청일</label><input value="${linkedDemo.created_at || ''}" readonly></div><div class="admin-field"><label>계정만료일</label><input value="${linkedDemo.expiry_date || ''}" readonly></div><div class="admin-field"><label>회원가입일</label><input value="${linkedDemo.timestamps?.signup_completed_at || ''}" readonly></div><div class="admin-field"><label>결제일</label><input value="${linkedDemo.timestamps?.paid_at || ''}" readonly></div></div>` : '<div style="font-size:11px;color:#718096">연동된 데모체험 정보가 없습니다.</div>'}</div>'''
new_demo_info = '''<div class="member-section"><h3>데모정보 ${linkedDemo ? '<span class="badge-status green">연동 완료</span>' : '<span class="badge-status gray">미연동</span>'}</h3>${linkedDemo ? `<div class="company-pay-grid"><div class="admin-field"><label>Demo ID</label><input value="${linkedDemo.demo_id}" readonly onclick="navigateToDemoDetail('${linkedDemo.demo_id}')" style="color:#2563eb;cursor:pointer;font-weight:700"></div><div class="admin-field"><label>데모계정</label><input value="${linkedDemo.demo_account || ''}" readonly></div><div class="admin-field"><label>데모 신청일</label><input value="${linkedDemo.created_at || ''}" readonly></div></div>` : '<div style="font-size:11px;color:#718096">연동된 데모체험 정보가 없습니다.</div>'}</div>'''
if old_demo_info not in html:
    raise RuntimeError('company demo information block not found')
html = html.replace(old_demo_info, new_demo_info, 1)

# Guardrails: removed fields must not remain in the three target UIs.
for forbidden in ['id="inquiry_category"', 'id="inquiry_content"', 'id="dt_inquiry_category"', 'id="dt_privacy"', 'id="dt_inquiry_content"']:
    if forbidden in html:
        raise RuntimeError(f'legacy target field still present: {forbidden}')

# Member company Demo Information must have only the three non-duplicated demo fields.
if '<label>계정만료일</label><input value="${linkedDemo.expiry_date' in html:
    raise RuntimeError('duplicated expiry remains in member company demo info')
if '<label>회원가입일</label><input value="${linkedDemo.timestamps?.signup_completed_at' in html:
    raise RuntimeError('duplicated signup date remains in member company demo info')
if '<label>결제일</label><input value="${linkedDemo.timestamps?.paid_at' in html:
    raise RuntimeError('duplicated payment date remains in member company demo info')

path.write_text(html, encoding='utf-8')
