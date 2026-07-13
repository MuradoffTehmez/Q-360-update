import json, glob
for report in glob.glob('lighthouse-reports/*.report.json'):
    with open(report, 'r', encoding='utf-8') as f:
        data = json.load(f)
        select_audit = data.get('audits', {}).get('select-name', {})
        if select_audit.get('score') != 1 and 'details' in select_audit and 'items' in select_audit['details']:
            print(f'\n--- {report} ---')
            for item in select_audit['details']['items']:
                node = item.get('node', {})
                print(f"Selector: {node.get('selector')}")
                print(f"Snippet: {node.get('snippet')}")
