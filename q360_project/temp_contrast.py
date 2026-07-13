import json, glob

for report in glob.glob('lighthouse-reports/*.report.json'):
    with open(report, 'r', encoding='utf-8') as f:
        data = json.load(f)
        contrast_audit = data.get('audits', {}).get('color-contrast', {})
        if contrast_audit.get('score') != 1 and 'details' in contrast_audit and 'items' in contrast_audit['details']:
            print(f'\n--- {report} ---')
            for item in contrast_audit['details']['items']:
                node = item.get('node', {})
                print(f"Selector: {node.get('selector')}")
                print(f"Snippet: {node.get('snippet')}")
                print(f"Contrast Ratio: {item.get('contrastRatio')}")
