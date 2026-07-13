import json, glob
for report in glob.glob('lighthouse-reports/*.report.json'):
    with open(report, 'r', encoding='utf-8') as f:
        data = json.load(f)
        button_audit = data.get('audits', {}).get('button-name', {})
        if button_audit.get('score') != 1 and 'details' in button_audit and 'items' in button_audit['details']:
            print(f'\n--- {report} ---')
            for item in button_audit['details']['items']:
                node = item.get('node', {})
                print(f"Selector: {node.get('selector')}")
                print(f"Snippet: {node.get('snippet')}")
