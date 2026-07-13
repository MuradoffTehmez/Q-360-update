import re

with open('templates/accounts/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix text-gray-800 in task cards and headings
content = re.sub(r'text-gray-800', 'text-gray-900 dark:text-white', content)
content = re.sub(r'text-gray-600', 'text-gray-600 dark:text-gray-400', content)

# Remove height: 100% from .task-card in style tag
content = content.replace('height: 100%;\n}', '/* height: 100%; removed */\n}')

# Fix Welcome Banner balance (increase padding, better centering)
content = content.replace('class="dashboard-header"', 'class="dashboard-header py-8 px-6 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl mb-8 shadow-lg relative overflow-hidden"')

# Reduce padding in task cards to fix empty space
content = content.replace('padding: 1.5rem;', 'padding: 1.25rem;')

# Add spacing above tables
content = content.replace('<!-- My Assignments -->', '<div class="mt-8 mb-4"></div>\n<!-- My Assignments -->')
content = content.replace('<!-- Quick Actions -->', '<div class="mt-8 mb-4"></div>\n<!-- Quick Actions -->')
content = content.replace('<!-- Recent Activity -->', '<div class="mt-8 mb-4"></div>\n<!-- Recent Activity -->')

with open('templates/accounts/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Dashboard updated successfully')
