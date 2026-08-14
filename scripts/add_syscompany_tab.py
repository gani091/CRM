from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

old_tab = '''        <button type="button" class="nav-tab-btn" id="tabSysDemoBtn" onclick="switchView('sysDemo')">
          🛠 SYSADMIN 전환 검증
        </button>'''
new_tab = '''        <button type="button" class="nav-tab-btn" id="tabSysDemoBtn" onclick="switchView('sysDemo')">
          🛠 SYSADMIN 데모체험관리
        </button>
        <button type="button" class="nav-tab-btn" id="tabSysCompanyBtn" onclick="switchView('sysCompany')">
          🏢 SYSADMIN 회원사관리조회
        </button>'''
if old_tab not in html:
    raise RuntimeError('SYSADMIN demo tab pattern not found')
html = html.replace(old_tab, new_tab, 1)

old_btns = "const btns = ['tabAsIsBtn', 'tabFormBtn', 'tabDashBtn', 'tabCompareBtn', 'tabSysDemoBtn'];"
new_btns = "const btns = ['tabAsIsBtn', 'tabFormBtn', 'tabDashBtn', 'tabCompareBtn', 'tabSysDemoBtn', 'tabSysCompanyBtn'];"
if old_btns not in html:
    raise RuntimeError('switchView button array pattern not found')
html = html.replace(old_btns, new_btns, 1)

old_branch = """      } else if (viewName === 'sysCompany') {
        if (document.getElementById('viewSysCompany')) document.getElementById('viewSysCompany').classList.add('active');
        if (document.getElementById('tabSysDemoBtn')) document.getElementById('tabSysDemoBtn').classList.add('active');
        if (mainContainer) mainContainer.classList.add('wide');
      }"""
new_branch = """      } else if (viewName === 'sysCompany') {
        if (document.getElementById('viewSysCompany')) document.getElementById('viewSysCompany').classList.add('active');
        if (document.getElementById('tabSysCompanyBtn')) document.getElementById('tabSysCompanyBtn').classList.add('active');
        if (mainContainer) mainContainer.classList.add('wide');
        renderSysCompanyShell();
      }"""
if old_branch not in html:
    raise RuntimeError('sysCompany switchView branch pattern not found')
html = html.replace(old_branch, new_branch, 1)

path.write_text(html, encoding='utf-8')
