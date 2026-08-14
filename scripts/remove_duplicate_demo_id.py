from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

old = '''<div class="member-section"><h3>데모정보 ${linkedDemo ? '<span class="badge-status green">연동 완료</span>' : '<span class="badge-status gray">미연동</span>'}</h3>${linkedDemo ? `<div class="company-pay-grid"><div class="admin-field"><label>Demo ID</label><input value="${linkedDemo.demo_id}" readonly onclick="navigateToDemoDetail('${linkedDemo.demo_id}')" style="color:#2563eb;cursor:pointer;font-weight:700"></div><div class="admin-field"><label>데모계정</label><input value="${linkedDemo.demo_account || ''}" readonly></div><div class="admin-field"><label>데모 신청일</label><input value="${linkedDemo.created_at || ''}" readonly></div></div>` : '<div style="font-size:11px;color:#718096">연동된 데모체험 정보가 없습니다.</div>'}</div>'''

new = '''<div class="member-section"><h3>데모정보 ${linkedDemo ? '<span class="badge-status green">연동 완료</span>' : '<span class="badge-status gray">미연동</span>'}</h3>${linkedDemo ? `<div class="company-pay-grid"><div class="admin-field"><label>데모계정</label><input value="${linkedDemo.demo_account || linkedDemo.demo_id || ''}" readonly onclick="navigateToDemoDetail('${linkedDemo.demo_id}')" style="color:#2563eb;cursor:pointer;font-weight:700"></div><div class="admin-field"><label>데모 신청일</label><input value="${linkedDemo.created_at || ''}" readonly></div></div>` : '<div style="font-size:11px;color:#718096">연동된 데모체험 정보가 없습니다.</div>'}</div>'''

if old not in html:
    raise RuntimeError('target member company demo info block not found')

html = html.replace(old, new, 1)

# Guardrail: member-company demo info should no longer render a standalone Demo ID field.
if '<label>Demo ID</label><input value="${linkedDemo.demo_id}"' in html:
    raise RuntimeError('duplicate Demo ID field still remains')

path.write_text(html, encoding='utf-8')
