import re

with open('templates/base/sidebar.html', 'r', encoding='utf-8') as f:
    side = f.read()

# Fix the accordion buttons which have format:
# <span class="flex items-center space-x-2">
#     <i class="..."></i>
#     <span>{% trans "..." %}</span>
# </span>
# <i class="fas fa-chevron-down..."></i>

side = re.sub(
    r'<span class="flex items-center space-x-2">\s*<i class="(.*?) w-4 (.*?)"></i>\s*<span>(.*?)</span>\s*</span>',
    r'<span class="flex items-center space-x-2 w-full">\n                        <i class="\1 \2 text-lg transition-all" :class="sidebarOpen ? \'w-4 mr-2\' : \'mx-auto w-full text-center\'"></i>\n                        <span x-show="sidebarOpen" class="whitespace-normal leading-tight">\3</span>\n                    </span>',
    side
)

side = re.sub(
    r'<i class="fas fa-chevron-down text-xs transition-transform duration-200 text-gray-500"\s*:class="\{\'rotate-180\': open\}"></i>',
    r'<i class="fas fa-chevron-down text-xs transition-transform duration-200 text-gray-500" x-show="sidebarOpen" :class="{\'rotate-180\': open}"></i>',
    side
)

with open('templates/base/sidebar.html', 'w', encoding='utf-8') as f:
    f.write(side)

print("Accordion buttons fixed.")
