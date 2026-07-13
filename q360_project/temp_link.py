import json, glob
for report in glob.glob('lighthouse-reports/*.report.json'):
    with open(report, 'r', encoding='utf-8') as f:
        data = json.load(f)
        link_audit = data.get('audits', {}).get('link-name', {})
        if link_audit.get('score') != 1 and 'details' in link_audit and 'items' in link_audit['details']:
            print(f'\n--- {report} ---')
            for item in link_audit['details']['items']:
                node = item.get('node', {})
                print(f"Selector: {node.get('selector')}")
                print(f"Snippet: {node.get('snippet')}")
