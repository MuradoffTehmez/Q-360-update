import re

# Update base.html
with open('templates/base/base.html', 'r', encoding='utf-8') as f:
    base = f.read()

# Instead of hiding sidebar, we just adjust margin
base = base.replace(
    ":class=\"{ 'md:ml-64': sidebarOpen && $el.closest('[x-data]').sidebarOpen }\"",
    ":class=\"sidebarOpen ? 'md:ml-64' : 'md:ml-20'\""
)
with open('templates/base/base.html', 'w', encoding='utf-8') as f:
    f.write(base)

# Update sidebar.html
with open('templates/base/sidebar.html', 'r', encoding='utf-8') as f:
    side = f.read()

# Update <aside> to use dynamic width
side = side.replace(
    'class="w-64 bg-white dark:bg-gray-900 shadow-xl border-r border-gray-200 dark:border-gray-800 hidden md:block overflow-y-auto"',
    ':class="sidebarOpen ? \'w-64\' : \'w-20\'" class="bg-white dark:bg-gray-900 shadow-xl border-r border-gray-200 dark:border-gray-800 hidden md:block overflow-y-auto transition-all duration-300 z-40 fixed h-full"'
)
# Remove x-show="sidebarOpen" from aside so it doesn't disappear
side = side.replace('x-show="sidebarOpen" x-transition:enter', 'x-transition:enter')

# Hide user info and text when collapsed
side = side.replace('<div class="flex-1 min-w-0">', '<div class="flex-1 min-w-0" x-show="sidebarOpen">')
side = re.sub(
    r'<span class="relative z-10 flex-1 whitespace-normal leading-tight">(.*?)</span>',
    r'<span class="relative z-10 flex-1 whitespace-normal leading-tight" x-show="sidebarOpen">\1</span>',
    side
)

# Center icons when collapsed
side = re.sub(
    r'<i class="(.*?) w-6 text-center mr-3 relative z-10 flex-shrink-0 text-lg"></i>',
    r'<i class="\1 w-6 text-center relative z-10 flex-shrink-0 text-lg transition-all" :class="sidebarOpen ? \'mr-3\' : \'mx-auto text-xl\'"></i>',
    side
)

with open('templates/base/sidebar.html', 'w', encoding='utf-8') as f:
    f.write(side)

print("Mini sidebar implemented.")
