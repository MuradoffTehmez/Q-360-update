import re

# Fix accounts/dashboard.html
with open('templates/accounts/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

# Welcome banner contrast
dash = dash.replace('class="text-white/90 text-lg mt-2"', 'class="text-white font-medium text-lg mt-2"')

# Active Tasks subtext contrast
dash = dash.replace('class="text-sm text-gray-600 dark:text-gray-400 flex items-center"', 'class="text-sm text-slate-300 flex items-center"')

# Progress bar padding in stat cards
# Find <div class="mt-4"> that precedes the progress bar
dash = re.sub(r'<div class="mt-4">\s*<div class="w-full bg-gray-200 rounded-full h-2">', 
              r'<div class="mt-4 px-2">\n            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">', dash)

# Empty state for Avg score
avg_score_block = """<div class="mt-4 px-2">
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div class="bg-gradient-to-r from-teal-400 to-green-500 h-2 rounded-full" style="width: 78%"></div>
            </div>
        </div>"""
new_avg_score_block = """<div class="mt-4 px-2">
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                {% if average_score and average_score != 'N/A' and average_score != 0 %}
                <div class="bg-gradient-to-r from-teal-400 to-green-500 h-2 rounded-full" style="width: 78%"></div>
                {% else %}
                <div class="bg-gray-400 dark:bg-gray-500 h-2 rounded-full" style="width: 100%"></div>
                {% endif %}
            </div>
        </div>"""
dash = dash.replace(avg_score_block, new_avg_score_block)

# Fix dark mode colors in stat cards background if any
dash = re.sub(r'bg-gray-200 rounded-full h-2', r'bg-gray-200 dark:bg-gray-700 rounded-full h-2', dash)

with open('templates/accounts/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash)

# Fix sidebar.html
with open('templates/base/sidebar.html', 'r', encoding='utf-8') as f:
    side = f.read()

# Make span wrap and leading tight
side = re.sub(r'<span class="relative z-10">', r'<span class="relative z-10 flex-1 whitespace-normal leading-tight">', side)

with open('templates/base/sidebar.html', 'w', encoding='utf-8') as f:
    f.write(side)

print("UI fixes applied successfully.")
