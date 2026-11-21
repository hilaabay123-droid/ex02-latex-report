import re, subprocess
s = open('references.bib', encoding='utf-8').read()
ents = re.findall(r'@\w+\{([^,]+),(.*?)\n\}', s, re.S)
want = ['gustafsson2021','patel2025','coresight2023','appriss2024','nrf2024','alhassawi2025','peng2023','google2023tryon','il_amend13_2024','gdpr2016','ppa_pets2025','shopify_dev_build','truefit_web']
for k, body in ents:
    if k not in want: continue
    doi = re.search(r'doi\s*=\s*\{([^}]+)\}', body)
    url = re.search(r'url\s*=\s*\{([^}]+)\}', body)
    u = ('https://doi.org/' + doi.group(1)) if doi else (url.group(1) if url else None)
    if not u: print(k, 'NO LINK'); continue
    r = subprocess.run(['curl','-sIL','-o','NUL','-w','%{http_code}','-m','25','-A','Mozilla/5.0',u],capture_output=True,text=True)
    code = r.stdout.strip()
    if code in ('403','405','000','404'):
        r = subprocess.run(['curl','-sL','-o','NUL','-w','%{http_code}','-m','25','-A','Mozilla/5.0',u],capture_output=True,text=True); code2=r.stdout.strip()
    else: code2=''
    print(k, code, code2, u[:80])
