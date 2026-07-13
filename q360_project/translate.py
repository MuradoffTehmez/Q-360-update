import os
import re

po_path = 'locale/az/LC_MESSAGES/django.po'

if not os.path.exists(po_path):
    print("PO file not found")
    exit(1)

with open(po_path, 'r', encoding='utf-8') as f:
    content = f.read()

translations = {
    "Home": "Ana Səhifə",
    "Skills": "Bacarıqlar",
    "Welcome": "Xoş gəldiniz",
    "Pending": "Gözləmədə olan",
    "Completed": "Tamamlanan",
    "Campaigns": "Kampaniyalar",
    "Avg Score": "Ortalama Bal",
    "My Active Tasks": "Aktiv Tapşırıqlarım",
    "My Assignments": "Tapşırıqlarım",
    "View All": "Hamısına Bax",
    "Analytics Dashboard": "Analitik Panel",
    "Key Performance Indicators": "Əsas Performans Göstəriciləri (KPI)",
    "Here's what's happening today": "Bu gün olan yeniliklər",
    "Pending Evaluations": "Gözləyən Qiymətləndirmələr",
    "Awaiting your response": "Cavabınız gözlənilir",
    "Upcoming Trainings": "Qarşıdan Gələn Təlimlər",
    "Due within 7 days": "7 gün ərzində",
    "Skills Pending Approval": "Təsdiq Gözləyən Bacarıqlar",
    "Requires your approval": "Təsdiqiniz tələb olunur",
    "Active Development Goals": "Aktiv İnkişaf Hədəfləri",
    "In progress": "Davam edir",
    "Print": "Çap et",
    "Dashboard": "Panel",
    "360° Performance Evaluation System": "360° Performans Qiymətləndirmə Sistemi",
    "Evaluations": "Qiymətləndirmələr",
    "360° Feedback": "360° Rəylər",
    "Analytics": "Analitika",
    "Training": "Təlim",
    "Engagement": "Cəlb olunma",
    "Pulse Surveys": "Nəbz Sorğuları",
    "Recognition": "Tanınma",
    "Leaderboard": "Liderlər lövhəsi",
    "Reports": "Hesabatlar"
}

def replace_msgstr(match):
    msgid = match.group(1)
    # The actual msgstr could be empty or have something
    msgstr_match = match.group(2)
    
    # Clean the msgid (handle newlines if any, but simplistic approach here)
    clean_msgid = msgid.replace('\\n', '').strip()
    
    if clean_msgid in translations:
        return f'msgid "{msgid}"\nmsgstr "{translations[clean_msgid]}"'
    return match.group(0)

# Regex to find msgid "..." followed by msgstr "..."
# Handling simple single line msgid and msgstr
content = re.sub(r'msgid\s+"(.*?)"\nmsgstr\s+"(.*?)"', replace_msgstr, content)

with open(po_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Translations applied successfully.")
