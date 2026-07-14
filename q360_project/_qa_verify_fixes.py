# -*- coding: utf-8 -*-
"""TƏCİLİ DÜZƏLİŞ 1+2 doğrulaması. 2 müvəqqəti user yaradılıb silinir. (müvəqqəti fayl)"""
import os, django, secrets
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

ENGINE = []
ENGINE += [f'/workflow/{n}' for n in ['workflows/', 'designer/', 'versions/', 'history/', 'logs/', 'monitoring/']]
ENGINE += [f'/approval/{n}' for n in ['rules/', 'chains/', 'history/', 'queue/', 'delegations/']]
ENGINE += [f'/access-control/{n}' for n in ['roles/', 'permissions/', 'policies/', 'groups/', 'access-requests/', 'access-history/']]
ENGINE += [f'/policy-engine/{n}' for n in ['policies/', 'rules/', 'simulator/', 'versions/', 'logs/']]
ENGINE += [f'/feature-flags/{n}' for n in ['flags/', 'environments/', 'rollouts/', 'experiments/', 'history/']]

BUG500 = [
    '/pfile/employees/create/', '/pfile/employees/import/', '/pfile/documents/',
    '/pfile/contracts/', '/pfile/assets/', '/pfile/emergency-contacts/',
    '/okr/check-ins/',
    '/recruitment/referrals/',
    '/engagement/anonymous-feedback/',
    '/support/tickets/1/', '/support/1/',
]

su = User.objects.filter(is_superuser=True, is_active=True).order_by('id').first()
created_su = False
if su is None:
    su = User.objects.create_superuser(username='qa_fix_su', email='qa_fix_su@example.com',
                                       password=secrets.token_urlsafe(24))
    created_su = True

ru = User.objects.create_user(username='qa_fix_regular', email='qa_fix_regular@example.com',
                              password=secrets.token_urlsafe(24))
ru.is_staff = False; ru.is_superuser = False; ru.save()
print(f"USERS|superuser={su.username}(created={created_su})|regular={ru.username}(staff={ru.is_staff},super={ru.is_superuser})")

try:
    csu = Client(); csu.force_login(su)
    cru = Client(); cru.force_login(ru)

    print("\n### ENGINE idareetme sehifeleri: superuser (gozlenilen 200) | adi user (gozlenilen 403)")
    su_ok = ru_ok = 0
    for url in ENGINE:
        try:
            ss = csu.get(url).status_code
        except Exception as e:
            ss = f"EXC:{type(e).__name__}:{str(e)[:80]}"
        try:
            sr = cru.get(url).status_code
        except Exception as e:
            sr = f"EXC:{type(e).__name__}:{str(e)[:80]}"
        su_ok += (ss == 200); ru_ok += (sr == 403)
        flag = "OK" if (ss == 200 and sr == 403) else "!!!"
        print(f"ENG|{url}|SU={ss}|REG={sr}|{flag}")
    print(f"ENGINE YEKUN: superuser 200 = {su_ok}/26 | adi user 403 = {ru_ok}/26")

    print("\n### Batch 19/22/23/26/27 (evveller 500) — superuser (gozlenilen 200/302)")
    b_ok = 0
    for url in BUG500:
        try:
            rs = csu.get(url); ss = rs.status_code
            loc = rs.get('Location', '') if ss in (301, 302) else ''
        except Exception as e:
            ss = f"EXC:{type(e).__name__}:{str(e)[:120]}"; loc = ''
        ok = ss in (200, 301, 302)
        b_ok += ok
        print(f"BUG|{url}|{ss}|{loc}|{'OK' if ok else '!!!'}")
    print(f"BUG500 YEKUN: 500-suz (200/302) = {b_ok}/{len(BUG500)}")
finally:
    ru.delete(); print("\nCLEANUP|qa_fix_regular silindi")
    if created_su:
        su.delete(); print("CLEANUP|qa_fix_su silindi")
print("DONE")
