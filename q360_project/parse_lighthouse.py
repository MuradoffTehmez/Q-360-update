import json
import sys
import glob
import os

def parse_report(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Categories
    categories = data.get('categories', {})
    
    def get_score(cat):
        score = categories.get(cat, {}).get('score')
        return score * 100 if score is not None else 0

    perf_score = get_score('performance')
    seo_score = get_score('seo')
    acc_score = get_score('accessibility')
    bp_score = get_score('best-practices')

    # Audits
    audits = data.get('audits', {})
    
    # Key Metrics
    metrics = {
        'FCP': audits.get('first-contentful-paint', {}).get('displayValue', 'N/A'),
        'LCP': audits.get('largest-contentful-paint', {}).get('displayValue', 'N/A'),
        'TBT': audits.get('total-blocking-time', {}).get('displayValue', 'N/A'),
        'CLS': audits.get('cumulative-layout-shift', {}).get('displayValue', 'N/A'),
        'Speed Index': audits.get('speed-index', {}).get('displayValue', 'N/A')
    }

    # Opportunities & Diagnostics (Score < 0.9 or has savings)
    issues = []
    for audit_id, audit in audits.items():
        # Check if it's an opportunity or diagnostic that needs attention
        score = audit.get('score')
        if score is not None and score < 0.9 and audit.get('details') and audit.get('details').get('type') in ['opportunity', 'table']:
            title = audit.get('title')
            savings = audit.get('details', {}).get('overallSavingsMs', 0)
            if savings > 0 or score < 0.9:
                items = audit.get('details', {}).get('items', [])
                issues.append({
                    'id': audit_id,
                    'title': title,
                    'score': score,
                    'savings_ms': savings,
                    'items_count': len(items)
                })

    return {
        'file': os.path.basename(filepath),
        'scores': {
            'Performance': perf_score,
            'SEO': seo_score,
            'Accessibility': acc_score,
            'Best Practices': bp_score
        },
        'metrics': metrics,
        'issues': sorted(issues, key=lambda x: x['savings_ms'], reverse=True)
    }

if __name__ == '__main__':
    reports = glob.glob('lighthouse-reports/*.json')
    if not reports:
        print("No JSON reports found.")
        sys.exit(0)

    results = []
    for report in reports:
        results.append(parse_report(report))

    with open('summary_utf8.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print("Saved to summary_utf8.json")
