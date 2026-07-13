import re

with open('templates/base/sidebar.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

acc_idx = None
new_lines = []

for line in lines:
    # Check if this line has @click="activeAccordion = ... 'acc_X'
    m = re.search(r"@click=\"activeAccordion === 'acc_(\d+)' \? null : 'acc_\1'\"", line)
    if not m:
        m = re.search(r"@click=\"activeAccordion = activeAccordion === 'acc_(\d+)' \? null : 'acc_\1'\"", line)
    
    if m:
        acc_idx = m.group(1)
    
    if acc_idx is not None:
        if ":class=\"{'rotate-180': open}\"" in line:
            line = line.replace(":class=\"{'rotate-180': open}\"", f":class=\"{{'rotate-180': activeAccordion === 'acc_{acc_idx}'}}\"")
        if 'x-show="open"' in line:
            line = line.replace('x-show="open"', f'x-show="activeAccordion === \'acc_{acc_idx}\'"')
            
    new_lines.append(line)

with open('templates/base/sidebar.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Sidebar accordion fixed completely.")
