import json, glob

def get_metric(data, audit_name):
    audit = data.get('audits', {}).get(audit_name, {})
    val = audit.get('displayValue') or audit.get('numericValue')
    return str(val) if val is not None else 'N/A'

for report in glob.glob('lighthouse-reports/final-*.json'):
    try:
        with open(report, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cats = data.get('categories', {})
            perf = cats.get('performance', {}).get('score', 0)
            seo = cats.get('seo', {}).get('score', 0)
            a11y = cats.get('accessibility', {}).get('score', 0)
            bp = cats.get('best-practices', {}).get('score', 0)
            
            lcp = get_metric(data, 'largest-contentful-paint')
            fcp = get_metric(data, 'first-contentful-paint')
            tbt = get_metric(data, 'total-blocking-time')
            cls = get_metric(data, 'cumulative-layout-shift')

            print(f"--- {report} ---")
            print(f"Perf: {perf*100 if perf else 0:.0f} | SEO: {seo*100 if seo else 0:.0f} | A11y: {a11y*100 if a11y else 0:.0f} | BP: {bp*100 if bp else 0:.0f}")
            print(f"LCP: {lcp} | FCP: {fcp} | TBT: {tbt} | CLS: {cls}")
            if data.get('runtimeError'):
                print(f"Error: {data['runtimeError']['code']}")
            print()
    except Exception as e:
        print(f"Failed to parse {report}: {e}")
